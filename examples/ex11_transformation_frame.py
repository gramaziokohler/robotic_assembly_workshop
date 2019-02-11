"""
Frames describe position and orientation, but can also represent (right-handed)
coordinate systems. This is an example to bring a frame defined in the Object
Coordinate Frame (OCF) into the Robot Coordinate Frame (RCF).
"""
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
# Frame defined in RCF
frame_RCF = RCF.represent_frame_in_local_coordinates(frame_WCF)
print("Frame at TCP", frame_RCF)

# **ADVANCED**
# Due to some problem in the robot's controller we cannot set the TCP of the
# robot. That's why, based on frame_RCF, we have to find the frame at the
# robot's flange T0CF

# Tool coordinate frame
TCF = Frame(Point(0., 0., 0.3), Vector(1, 0, 0.), Vector(0, 1, 0.))
# The transformation from TCF to T0CF
TC2T0 = Transformation.from_frame_to_frame(Frame.worldXY(), TCF)
frame_WCF_T0 = frame_WCF.transformed(TC2T0)
frame_RCF_T0 = RCF.represent_frame_in_local_coordinates(frame_WCF_T0)
print("Frame at T0", frame_RCF_T0)
