# Orientation specs
from compas.geometry import Frame
# from compas_ghpython import xdraw_frame

point = (0.0, 0.0, 63.0)
xaxis = (0.68, 0.68, 0.27)
yaxis = (-0.67, 0.73, -0.15)

F = Frame(point, xaxis, yaxis)
print(F)

print(F.quaternion)  # ABB
print(F.euler_angles(static=True, axes='xyz'))  # Staubli
print(F.euler_angles(static=False, axes='zyx'))  # KUKA
print(F.axis_angle_vector)  # UR