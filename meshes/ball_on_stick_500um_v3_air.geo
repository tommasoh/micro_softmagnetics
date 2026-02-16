SetFactory("OpenCASCADE");
//+
Point(1) = {0, -1.5, 0, 1.0};
//+
Point(2) = {02.48335, 0, 0, 0.01};
//+
Point(3) = {02.51665, 0, 0, 0.01};
//+
Point(4) = {5, -1.5, 0, 1.0};
//+
Point(5) = {2.5, 1.249444939, 0, 0.01};
//+
Point(6) = {5, 3.5, 0, 1.0};
//+
Point(7) = {0, 3.5, 0, 1.0};
//+
Point(8) = {2.48335, 1, 0, 0.01};
//+
Point(9) = {2.51665, 1, 0, 0.01};
//+
Point(10) = {2.5, 1.499444939, 0, 0.01};
//+
// //+ Air
// Physical Surface(12) = {3};
// //+ Ball
// Physical Surface(13) = {1};
// //+ Stick
// Physical Surface(14) = {2};
// //+
MeshSize {2, 3, 5, 8, 9, 10} = .02;
MeshSize {1, 4, 6, 7} = .25;
Mesh.MeshSizeFromCurvature = 50;
// //+ domain edge
// Physical Curve(16) = {8, 9, 1, 6, 7, 10};
// //+ ball edge
// Physical Curve(17) = { 3, 4, 11};
//+
Line(1) = {1, 4};
//+
Line(2) = {4, 6};
//+
Line(3) = {6, 7};
//+
Line(4) = {7, 1};
//+
Line(5) = {2, 3};
//+
Line(6) = {2, 8};
//+
Line(7) = {9, 3};
//+
Circle(8) = {8, 5, 10};
//+
Circle(9) = {10, 5, 9};
//+
Circle(10) = {9, 5, 8};
//+
Curve Loop(1) = {3, 4, 1, 2};
//+
Curve Loop(2) = {9, 7, -5, 6, 8};
//+
Plane Surface(1) = {1, 2};
//+
Curve Loop(3) = {8, 9, 10};
//+
Plane Surface(2) = {3};
//+
Curve Loop(4) = {7, -5, 6, -10};
//+
Plane Surface(3) = {4};
//+ Air
Physical Surface(11) = {1};
//+ Ball
Physical Surface(12) = {2};
//+ Stick
Physical Surface(13) = {3};
//+ Edge
Physical Curve(14) = {3, 4, 1, 2};
//+ ball edge
Physical Curve(15) = {8, 9, 10};
//+ fixed beam edge
Physical Curve(16) = {5};
