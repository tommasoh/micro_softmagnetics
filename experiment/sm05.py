"""SM05 bistable bit as a function: the magnet approaches along x, the bit deflects.

Physics, mesh, solver and time stepping are those of SM05_bistable_bit.ipynb.
Removed: plots and VTX field output. Units: mm, s, kg, mN, kPa, mT (see notebook).
Serial only (the displacement probe uses the local cell).
"""
from pathlib import Path

import numpy as np
import ufl
from dolfinx import fem, geometry, log
from dolfinx.fem import Constant, Function, dirichletbc, functionspace
from dolfinx.fem.petsc import NonlinearProblem
from dolfinx.io import XDMFFile
from dolfinx.nls.petsc import NewtonSolver
from basix.ufl import element, mixed_element
from mpi4py import MPI
from petsc4py import PETSc
from ufl import (Identity, conditional, cosh, det, dev, dot, eq, grad, inner, inv,
                 ln, outer, sqrt, tanh)

from magnet import potential

MESH = Path(__file__).resolve().parent.parent / "meshes" / "bistable_bit_v5"

# Measured per dynamic range (notebook comments): magnetic saturation MA/m, Young's modulus MPa
MATERIALS = {
    2: {"ms_MA_per_m": 0.00466688, "E_MPa": 19.955},
    18: {"ms_MA_per_m": 0.00180904, "E_MPa": 36.030},
    51: {"ms_MA_per_m": 0.0009868, "E_MPa": 53.835},
    100: {"ms_MA_per_m": 0.00054656, "E_MPa": 53.201},
}

SCALE = 1.6 + 2.016        # horizontal side of the water domain, mm
BIT_EDGE = 0.5 + 2.016     # used by the notebook to turn magnet travel into separation, mm
PROBE = [SCALE / 2, 0.5, 0.0]
SOLID, BOUNDARY, LEGS, INTERFACE = 49, 51, 52, 53   # mesh tags


def simulate(E_MPa=19.955, ms_MA_per_m=0.00466688, chi=0.023, Br_mT=1480.0,
             start_gap_mm=10.0, approach_mm=10.0, ramp_s=5.0, t_end_s=None, eta=1.0e-2):
    """Move the magnet by approach_mm towards the bit in ramp_s seconds.

    start_gap_mm: magnet face to the edge of the water domain at t = 0.
    t_end_s: stop early (same steps as the full run), None = whole ramp.
    Returns arrays per converged step: t_s, travel_mm, separation_mm, disp_um, fx_mN,
    and completed = False if the solver gave up before t_end_s.
    The notebook csv stores 0.5 * fx_mN * 1e3 as its force column.
    """
    log.set_log_level(log.LogLevel.WARNING)
    with XDMFFile(MPI.COMM_WORLD, f"{MESH}.xdmf", "r") as f:
        domain = f.read_mesh(name="Grid", xpath="/Xdmf/Domain")
        cell_tags = f.read_meshtags(domain, name="Grid")
    tdim = domain.topology.dim
    domain.topology.create_connectivity(tdim, tdim - 1)
    domain.topology.create_connectivity(tdim - 1, tdim)
    with XDMFFile(MPI.COMM_WORLD, f"{MESH.parent}/facet_{MESH.name}.xdmf", "r") as f:
        facet_tags = f.read_meshtags(domain, name="Grid")

    ds = ufl.Measure("dS", domain=domain, subdomain_data=facet_tags, metadata={"quadrature_degree": 2})
    dx = ufl.Measure("dx", domain=domain, subdomain_data=cell_tags, metadata={"quadrature_degree": 2})
    n2 = ufl.FacetNormal(domain)
    n = ufl.as_vector([n2[0], n2[1], 0.0])

    # Piecewise-constant material fields: DG0 dof i <-> cell tag i, as in the notebook
    Vmat = functionspace(domain, ("DG", 0))

    def mat(solid, water):
        prop = Function(Vmat)
        prop.x.array[:] = np.where(cell_tags.values == SOLID, solid, water)
        return prop

    G = mat(E_MPa * 1e3 / 3, 0.001)        # shear modulus, kPa
    K = mat(E_MPa * 1e6 / 3, 0.001)        # bulk modulus, kPa (nearly incompressible)
    rho = mat(1.0e-6, 0.0)                 # kg/mm^3
    mu0 = Constant(domain, 1.256e-6 * 1.0e9)
    chi_f = mat(chi, 1.0e-16)
    ms = mat(ms_MA_per_m, 10.0)
    is_solid = mat(1, 0)                   # Maxwell stress deforms this domain
    is_water = mat(0, 1)                   # non-magnetizable

    # Newmark with alpha = 0 (notebook): averaged fields are the new fields
    gamma, beta = 0.5, 0.25
    ramp = Constant(domain, PETSc.ScalarType(0.0))
    dt = ramp_s / 200
    dk = Constant(domain, PETSc.ScalarType(dt))

    U2 = element("Lagrange", domain.basix_cell(), 2, shape=(2,))
    P0 = element("DG", domain.basix_cell(), 0)
    P2 = element("Lagrange", domain.basix_cell(), 2)
    ME = functionspace(domain, mixed_element([U2, P0, P2]))
    V2 = functionspace(domain, U2)
    w, w_old = Function(ME), Function(ME)
    u, p, phi = ufl.split(w)
    u_old, _, _ = ufl.split(w_old)
    u_t, p_t, phi_t = ufl.TestFunctions(ME)
    v_old, a_old = Function(V2), Function(V2)

    def F_calc(u):
        Fu = Identity(2) + grad(u)
        return ufl.as_tensor([[Fu[0, 0], Fu[0, 1], 0], [Fu[1, 0], Fu[1, 1], 0], [0, 0, 1]])

    def grad3(y):                          # plane strain gradient of a scalar
        g = grad(y)
        return ufl.as_vector([g[0], g[1], 0.0])

    def grad3_vec(v):                      # plane strain gradient of a vector
        g = grad(v)
        return ufl.as_tensor([[g[0, 0], g[0, 1], 0], [g[1, 0], g[1, 1], 0], [0, 0, 0]])

    def h_calc(u, phi):
        return inv(F_calc(u).T) * -grad3(phi)

    def norm(v):
        return sqrt(dot(v, v) + 1.0e-16)

    def maxwell(h):
        return mu0 * (outer(h, h) - 0.5 * dot(h, h) * Identity(3))

    def piola(u, p, phi):
        Fu = F_calc(u)
        J = det(Fu)
        Fbar = J ** (-1 / 3) * Fu
        T_eq = G / J * dev(Fbar * Fbar.T) - p * Identity(3)
        h = h_calc(u, phi)
        hn = norm(h)
        T_para = (-mu0 * ms**2 / chi_f * ln(cosh(chi_f / ms * hn)) * Identity(3)
                  + mu0 * ms / hn * tanh(chi_f / ms * hn) * outer(h, h))
        T_mag = maxwell(h) + conditional(eq(is_water, 1), 0 * Identity(3), T_para)
        return J * (T_eq + conditional(eq(is_solid, 1), T_mag, 0 * Identity(3))) * inv(Fu.T)

    def b_R_calc(u, phi):
        Fu = F_calc(u)
        h = h_calc(u, phi)
        hn = norm(h)
        b_para = mu0 * ms / hn * tanh(chi_f / ms * hn) * h
        b = mu0 * h + conditional(eq(is_water, 1), ufl.as_vector([0, 0, 0]), b_para)
        return det(Fu) * inv(Fu) * b

    a_new = (u - u_old - dk * v_old) / beta / dk**2 - (1 - 2 * beta) / 2 / beta * a_old
    v_new = v_old + dk * ((1 - gamma) * a_old + gamma * a_new)
    Fu, J = F_calc(u), det(F_calc(u))

    # Maxwell traction from the water side on the solid-water interface
    T_out = maxwell(h_calc(u, phi))
    trac = (is_water("+") * dot(J("-") * T_out("+") * inv(Fu.T)("-"), n("-"))
            + is_water("-") * dot(J("+") * T_out("-") * inv(Fu.T)("+"), n("+")))

    res = (inner(piola(u, p, phi), grad3_vec(u_t)) * dx
           - inner(trac, ufl.avg(ufl.as_vector([u_t[0], u_t[1], 0.0]))) * ds(INTERFACE)
           + inner(rho * a_new, u_t) * dx
           + inner(eta * v_new, u_t) * dx(SOLID)
           + inner((J - 1) + p / K, p_t) * dx
           + inner(b_R_calc(u, phi), grad3(phi_t)) * dx)
    fx_form = fem.form(dot(trac, ufl.as_vector([1.0, 0.0, 0.0])) * ds(INTERFACE))

    # Magnet on the boundary: phi of the moving magnet, Br = mu0 * M
    Vphi, _ = ME.sub(2).collapse()
    phi_bc = Function(Vphi)
    M = Br_mT / float(mu0)
    x0 = SCALE + start_gap_mm + 6.35 / 2   # magnet centre at t = 0

    def set_magnet():
        cx = x0 - approach_mm * float(ramp)
        phi_bc.interpolate(lambda x: potential(x[0], x[1], cx, 0.675, M))

    def dofs(sub, tag):
        return fem.locate_dofs_topological(sub, facet_tags.dim, facet_tags.find(tag))

    bcs = [dirichletbc(0.0, dofs(ME.sub(0).sub(i), tag), ME.sub(0).sub(i))
           for tag in (BOUNDARY, LEGS) for i in (0, 1)]
    bcs.append(dirichletbc(phi_bc, dofs((ME.sub(2), Vphi), BOUNDARY), ME.sub(2)))

    def build_solver():
        problem = NonlinearProblem(res, w, bcs, ufl.derivative(res, w, ufl.TrialFunction(ME)))
        solver = NewtonSolver(MPI.COMM_WORLD, problem)
        solver.convergence_criterion = "incremental"
        solver.rtol = solver.atol = 1e-6
        solver.max_it = 25
        solver.error_on_nonconvergence = False
        ksp = solver.krylov_solver
        opts, pre = PETSc.Options(), ksp.getOptionsPrefix()
        opts[f"{pre}ksp_type"] = "preonly"
        opts[f"{pre}pc_type"] = "lu"
        opts[f"{pre}pc_factor_mat_solver_type"] = "mumps"
        opts[f"{pre}ksp_max_it"] = 30
        ksp.setFromOptions()
        return solver

    tree = geometry.bb_tree(domain, tdim)
    probe = np.array(PROBE)
    probe_cell = geometry.compute_colliding_cells(
        domain, geometry.compute_collisions_points(tree, probe), probe).array[0]

    v_expr = fem.Expression(v_new, V2.element.interpolation_points())
    a_expr = fem.Expression(a_new, V2.element.interpolation_points())
    v_tmp, a_tmp = Function(V2), Function(V2)

    t_stop = ramp_s if t_end_s is None else min(t_end_s, ramp_s)
    rows, t, fails = [], 0.0, 0
    solver = build_solver()
    while round(t + dt, 9) <= t_stop:
        t += dt
        ramp.value = t / ramp_s
        set_magnet()
        iters, converged = solver.solve(w)
        w.x.scatter_forward()

        if not converged:               # back up, cut dt by 10, give up after 6 in a row
            fails += 1
            if fails > 5:
                break
            t -= dt
            dt /= 10
            dk.value = dt
            w.x.array[:] = w_old.x.array
            solver = build_solver()
            continue
        fails = 0

        disp = w.sub(0).sub(0).eval(PROBE, probe_cell)[0]
        fx = domain.comm.gather(fem.assemble_scalar(fx_form))[0]
        rows.append((t, approach_mm * float(ramp), disp, fx))

        v_tmp.interpolate(v_expr)
        a_tmp.interpolate(a_expr)
        w_old.x.array[:] = w.x.array
        v_old.x.array[:] = v_tmp.x.array
        a_old.x.array[:] = a_tmp.x.array

        # adaptive step: grow if easy, shrink if hard, at most ramp_s / 100
        if iters <= 4:
            dt *= 1.5
        elif iters >= 7:
            dt *= 0.5
        dt = min(dt, ramp_s / 100)
        dk.value = dt

    t_s, travel, disp, fx = np.array(rows).T
    return {
        "t_s": t_s,
        "travel_mm": travel,
        "separation_mm": start_gap_mm - travel + (SCALE - BIT_EDGE) - disp,
        "disp_um": disp * 1e3,
        "fx_mN": fx,
        "completed": fails <= 5,
    }
