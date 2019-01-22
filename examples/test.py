from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends.ros import MoveItErrorCodes
from compas_fab.backends.ros import Constraints
from compas_fab.backends.ros import JointConstraint


pc = Constraints(name="hh")
print("pc", pc)
names = ['gantry_joint', 'rob11_joint_cart', 'rob11_joint_cart_zaxis']
tol = 0.01
for name in names:
    pos = 124.
    pc.joint_constraints.append(JointConstraint(name, pos, tol, tol, 1.))
print(pc)

print(Constraints())