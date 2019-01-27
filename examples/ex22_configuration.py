from compas.robots import Joint

print(Joint.REVOLUTE)
print(Joint.PRISMATIC)
print(Joint.FIXED)


from math import pi
from compas_fab.robots import Configuration

values = [0] * 6
types = [Joint.REVOLUTE] * 6
config = Configuration(values, types)

config = Configuration([pi/2, 3., 0.1], [Joint.REVOLUTE, Joint.PRISMATIC, Joint.PLANAR])

config = Configuration.from_revolute_values([pi/2, 0., 0., pi/2, pi, 0])

config = Configuration.from_prismatic_and_revolute_values([8.312], [pi/2, 0., 0., 0., 2*pi, 0.8])