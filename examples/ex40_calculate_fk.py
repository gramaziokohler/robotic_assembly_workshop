from ex23_load_robot import robot

from compas_fab.robots import Configuration
from compas_fab.backends import RosClient

robot.client = RosClient()
robot.client.run()

configuration = Configuration.from_revolute_values([-2.238, -1.153, -2.174, 0.185, 0.667, 0.000])
group = "manipulator"  # or robot.main_group_name

response = robot.forward_kinematics(configuration, group)

print(response.frame_RCF)
print(response.fk_link_names)

robot.client.terminate()
