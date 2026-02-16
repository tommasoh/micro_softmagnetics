// Gmsh project created on Fri Jan 16 10:37:25 2026
SetFactory("OpenCASCADE");
lc = 0.25;
lm = 0.05;
lf = 0.025;
scale = 2.0;
Narms = Floor(1/lf);
Mesh.MeshSizeFromCurvature = 50;
//+
Point(1) = {-2.0, 0, 0, lc};
//+
Point(2) = {2.0, 0, 0, lc};
//+
Point(3) = {2.0, scale, 0, lc};
//+
Point(4) = {-2.0, scale, 0, lc};
//+
Point(5) = {-0.1, 0, 0, lm};
//+
Point(6) = {0.1, 0, 0, lm};
//+
Point(7) = {0.1, 0.5, 0, lf};
//+
Point(8) = {-0.1, 0.5, 0, lf};
//+
Point(9) = {0.1, 0.5-0.03451, 0, lf};
//+
Point(10) = {1.0, 0.690+0.2, 0, lf};
//+
Circle(1) = {1.0, 0.690+0.2, 0, 0.2, 0, 2*Pi};
//+
Point(12) = {0.1+0.966, 0.5+0.259, 0, lf};
//+
Point(13) = {0.1+0.966, 0.5-0.03451+0.259, 0, lf};
//+
Point(14) = {-0.1, 0.5-0.03451, 0, lf};
//+
Line(2) = {1, 5};
//+
Line(3) = {5, 6};
//+
Line(4) = {5, 14};
//+
Line(5) = {14, 8};
//+
Line(6) = {8, 7};
//+
Line(7) = {7, 9};
//+
Line(8) = {9, 6};
//+
Line(9) = {6, 2};
//+
Line(10) = {7, 12};
//+
Line(11) = {12, 13};
//+
Line(12) = {13, 9};
//+
BooleanFragments{ Curve{1}; Delete; }{ Curve{10}; Delete; }
BooleanFragments{ Curve{12}; Delete; }{ Curve{14}; Delete; }
//+
Delete{ Curve{11}; Curve{16}; Curve{17}; }
//+
Symmetry {1, 0, 0, 0} {
  Duplicata { Curve{13}; Curve{20}; Curve{19}; }
}
//+
Line(26) = {2, 3};
//+
Line(27) = {3, 4};
//+
Line(28) = {4, 1};
//+
Curve Loop(1) = {13, 19, 20};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {15, 19, 18, -7};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {6, 7, 8, -3, 4, 5};
//+
Plane Surface(3) = {3};
//+
Line(29) = {22, 8};
//+
Line(30) = {14, 23};
//+
Curve Loop(4) = {29, -5, 30, -23};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {21, 23, 22};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {27, 28, 2, 4, 30, 22, 21, 29, 6, 15, -13, -20, 18, 8, 9, 26};
//+
Plane Surface(6) = {6};
//+
Physical Curve(31) = {2, 3, 28, 27, 26, 9};
//+
Physical Curve(32) = {21, 22, 23, 13, 20, 19};
//+
Physical Surface(33) = {5};
//+
Physical Surface(34) = {1};
//+
Physical Surface(35) = {6};
//+
Physical Surface(36) = {3, 2, 4};
//+ 
Transfinite Curve {15,18,29,30} = Narms;