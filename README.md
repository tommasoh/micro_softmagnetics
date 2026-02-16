# FEniCSx codes for soft-magnetic micro-actuators 

This repository contains example FEniCSx finite element simulation codes for applications of the large deformation coupled magneto-elasticity theory for soft-magnetorheological materials (Stewart and Anand, 2025; [codes here](https://github.com/ericstewart36/softmagnetics)) to modeling micro-scale magnetic actuators as in the experiments of Sun et al. (2025) (https://arxiv.org/abs/2510.07599v1).

Specifically, the repository contains all the relevant FEniCSx Jupyter notebooks and mesh files which were used for the numerical simulations in the revised version of the accompanying paper, "Magnetically Responsive Microprintable Soft Nanocomposites with Tunable Nanoparticle Loading," by Rachel M. Sun, Andrew Y. Chen, Yiming Ji, Daryl W. Yee, Eric M. Stewart, and Carlos M. Portela.

![](https://github.com/ericstewart36/micro_softmagnetics/blob/main/animations.gif)

# Citations
- R.M. Sun, A.Y. Chen, J. Yiming, D.W. Yee, and C.M. Portela, 2025. Magnetically Responsive Microprintable Soft Nanocomposites with Tunable Nanoparticle Loading. ArXiv pre-print,  https://arxiv.org/abs/2510.07599.
- E.M. Stewart and L. Anand, 2025. Magnetostriction of soft-magnetorheological elastomers. Journal of the Mechanics and Physics of Solids 194, 105934.

# Running the codes

A detailed guide for installing FEniCSx in a Docker container and running the notebooks using VSCode is provided both for [Mac](https://github.com/ericstewart36/finite_viscoelasticity/blob/main/FEniCSx_v08_Docker_install_mac.pdf) and [Windows](https://github.com/ericstewart36/finite_viscoelasticity/blob/main/FEniCSx_v08_Docker_install_windows.pdf). The installation process is essentially similar for the two operating systems, but the example screenshots in the instructions are from the relevant system.

These are our preferred methods for editing and running FEniCSx codes, although [many other options exist](https://fenicsproject.org/download/). Note that all codes were written for FEniCSx v0.8.0, so our instructions documents will direct you to install this specific version of FEniCSx.

