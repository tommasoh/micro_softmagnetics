// Gmsh project created on Fri Jan  2 11:14:35 2026
SetFactory("OpenCASCADE");
//+
Mesh.RecombineAll = 0;     // Prevent quads
Mesh.Recombine3DAll = 0;   // Prevent hexes
Mesh.Algorithm = 6;        // 2D triangle meshing (e.g., frontal-Delaunay)
Mesh.Algorithm3D = 1;      // 3D tetrahedral meshing (Delaunay)
Mesh.ElementOrder = 1;     // Linear elements
//+
A  = 0.325/2; // amplitude of a cosine ribbon
L  = 0.325;    // length of a cosine ribbon
lam = 2*L; 
N  = 25; // Number of points on spline interpolation
lr = 0.05; // mesh size for ribbon
lm = 0.05; // mid-size mesh
lc = 0.2; // coarse mesh size
t = 0.006;  // ribbon thickness
//+
x0 = 0.50+0.36+A-t; // center x coord
y0 = 0; // center y coord
//+
// Cosine points
For i In {0:N-1}
  y = y0 + L * i/(N-1);
  x = x0 + A * Cos(2*Pi*(y-y0)/lam);
  Point(i+1) = {x, y, 0, lr};
EndFor
Spline(1) = {1:N};
//+
Translate {t, 0, 0} {
  Duplicata { Curve{1}; }
}
//+
Point(28) = {0, -0.5, 0, lc};
//+
Point(29) = {0, 2*L+0.5+0.5, 0, lc};
//+
Point(30) = {3.0, -0.5, 0, lc};
//+
Point(31) = {3.0, 2*L+0.5+0.5, 0, lc};
//+
Point(32) = {0.5, L, 0, lm};
//+
Point(33) = {0.5, L+0.5, 0, lm};
//+
Point(34) = {1.94, L, 0, lm};
//+
Point(35) = {1.94, L+0.5, 0, lm};
//+
Translate {0.24, 0, 0} {
  Duplicata { Curve{1}; Curve{2}; }
}
//+
Translate {0.48, 0, 0} {
  Duplicata { Curve{1}; Curve{2}; Curve{3}; Curve{4}; }
}
//+
Symmetry {0, 1, 0, -(L+0.25)} {
  Duplicata { Curve{1}; Curve{2}; Curve{3}; Curve{4}; Curve{5}; Curve{6}; Curve{7}; Curve{8}; }
}
// structured-ish boundary mesh spacing
Transfinite Curve {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16} = 2*N;
// Transfinite Curve {20,41} = 2;
// Transfinite Curve {2,4} = 30;
// Transfinite Curve {3} = N;
//+
//+
Line(17) = {28, 30};
//+
Line(18) = {30, 31};
//+
Line(19) = {31, 29};
//+
Line(20) = {29, 28};
//+
Line(21) = {32, 25};
//+
Line(22) = {25, 27};
//+
Line(23) = {27, 41};
//+
Line(24) = {41, 43};
//+
Line(25) = {43, 53};
//+
Line(26) = {53, 55};
//+
Line(27) = {55, 57};
//+
Line(28) = {57, 59};
//+
Line(29) = {59, 34};
//+
Line(30) = {34, 35};
//+
Line(31) = {35, 91};
//+
Line(32) = {91, 89};
//+
Line(33) = {89, 87};
//+
Line(34) = {87, 85};
//+
Line(35) = {85, 83};
//+
Line(36) = {83, 81};
//+
Line(37) = {81, 79};
//+
Line(38) = {79, 77};
//+
Line(39) = {77, 33};
//+
Line(40) = {33, 32};
//+
Line(41) = {76, 78};
//+
Line(42) = {80, 82};
//+
Line(43) = {84, 86};
//+
Line(44) = {88, 90};
//+
Line(45) = {1, 26};
//+
Line(46) = {40, 42};
//+
Line(47) = {52, 54};
//+
Line(48) = {56, 58};
//+
Curve Loop(1) = {19, 20, 17, 18};
//+
Curve Loop(2) = {39, 40, 21, -1, 45, 2, 23, -3, 46, 4, 25, -5, 47, 6, 27, -7, 48, 8, 29, 30, 31, -16, -44, 15, 33, -14, -43, 13, 35, -12, -42, 11, 37, -10, -41, 9};
//+
Plane Surface(1) = {1, 2};
//+
Curve Loop(3) = {41, 10, 38, -9};
//+
Curve Loop(4) = {42, 12, 36, -11};
//+
Curve Loop(5) = {41, 10, 38, -9};
//+
Plane Surface(2) = {5};
//+
Curve Loop(6) = {42, 12, 36, -11};
//+
Plane Surface(3) = {6};
//+
Curve Loop(7) = {43, 14, 34, -13};
//+
Plane Surface(4) = {7};
//+
Curve Loop(8) = {44, 16, 32, -15};
//+
Plane Surface(5) = {8};
//+
Curve Loop(9) = {45, 2, -22, -1};
//+
Plane Surface(6) = {9};
//+
Curve Loop(10) = {46, 4, -24, -3};
//+
Plane Surface(7) = {10};
//+
Curve Loop(11) = {47, 6, -26, -5};
//+
Plane Surface(8) = {11};
//+
Curve Loop(12) = {48, 8, -28, -7};
//+
Plane Surface(9) = {12};
//+
Curve Loop(13) = {30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 21, 22, 23, 24, 25, 26, 27, 28, 29};
//+
Plane Surface(10) = {13};
//+
Physical Surface(49) = {3, 2, 4, 5, 10, 6, 7, 8, 9};
//+
Physical Surface(50) = {1};
//+
Physical Curve(51) = {19, 20, 17, 18};
//+
Physical Curve(52) = {41, 42, 43, 44, 45, 46, 47, 48};
//+
Physical Curve(53) = {9, 39, 40, 21, 1, 2, 23, 3, 4, 25, 5, 6, 27, 7, 8, 29, 30, 31, 16, 15, 33, 14, 13, 35, 12, 11, 37, 10};
