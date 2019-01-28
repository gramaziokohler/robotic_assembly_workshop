from ex22_load_compas_fab_robot import robot

from compas.geometry import Frame
from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends.ros import MoveItErrorCodes

robot.client = RosClient('127.0.0.1', 9090)
robot.client.run()

configuration = Configuration.from_revolute_values([-2.238, -1.153, -2.174, 0.185, 0.667, 0.000])
group = "manipulator"  # or robot.main_group_name

response = robot.forward_kinematics(configuration, group)

print(response.frame_RCF)
print(response.fk_link_names)

robot.client.terminate()
