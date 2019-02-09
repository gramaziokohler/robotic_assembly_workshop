from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Transformation

# Robot coordinate frame
RCF = Frame(Point(1., -1., 0.),
            Vector(0.707, -0.707, 0.),
            Vector(0.707, 0.707, 0.))

# Object coordinate frame
OCF = Frame(Point(3., -3., 0.),
            Vector(0.456, 0.890, 0.),
            Vector(-0.890, 0.456, 0.))

# Frame defined in OCF
frame_OCF = Frame([0.1, 0.1, 0.1], [1, 0, 0], [0, 1, 0])
# Frame expressed in WCF
frame_WCF = OCF.represent_frame_in_global_coordinates(frame_OCF)

# Tool center frame, defined in the T0CF
TCF = Frame(Point(0., 0., 0.3), Vector(1, 0, 0.), Vector(0, 1, 0.))
# The transformation from TCF to T0CF
TC2T0 = Transformation.from_frame_to_frame(Frame.worldXY(), TCF)
frame_WCF_T0 = frame_WCF.transformed(TC2T0)

# Frame defined in RCF
frame_RCF = RCF.represent_frame_in_local_coordinates(frame_WCF)
frame_RCF_T0 = RCF.represent_frame_in_local_coordinates(frame_WCF_T0)

print(frame_RCF_T0)

# =================================
# Example

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Transformation

F1 = Frame(Point(1., -1., 0.),
           Vector(0.707, -0.707, 0.),
           Vector(0.707, 0.707, 0.))

F2 = Frame(Point(3., -3., 0.),
           Vector(0.456, 0.890, 0.),
           Vector(-0.890, 0.456, 0.))

frame_WCF = Frame(Point(1.141, -1.000, 0.100),
                  Vector(0.707, -0.707, 0.000),
                  Vector(0.707, 0.707, 0.000))

# Represent frame_WCF in F1
frame_F1 = F1.represent_frame_in_local_coordinates(frame_WCF)

# If this frame was in F2, what would it global coordinates be?
frame_WCF_F2 = F2.represent_frame_in_global_coordinates(frame_F1)
print("frame_WCF_F2", frame_WCF_F2)

# Alternative solution
T1 = Transformation.from_frame_to_frame(F1, Frame.worldXY())
T2 = Transformation.from_frame(F2)
print("frame_WCF_F2", frame_WCF.transformed(T2 * T1))
