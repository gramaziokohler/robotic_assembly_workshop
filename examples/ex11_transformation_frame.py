from compas.geometry import Point
from compas.geometry import Frame
from compas.geometry import Transformation

point = (146.00, 150.00, 161.50)
xaxis = (0.9767, 0.0010, -0.214)
yaxis = (0.1002, 0.8818, 0.4609)

F = Frame(point, xaxis, yaxis)

# point in F's local coordinate system
pt_LCF = Point(0, 150, 0)

# transform point to be in the global coordinate system
T = Transformation.from_frame(F)
pt_WCF = pt_LCF.transformed(T)
print(pt_WCF)

# or alternatively use the frame's function
print(F.represent_in_global_coordinates(pt_LCF))

