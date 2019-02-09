"""
Calculate the inverse kinematics of a robot based on the frame and a starting
configuration.
"""
from ex22_load_compas_fab_robot import robot

from compas.geometry import Frame
from compas_fab.backends import RosClient
from compas_fab.robots import Configuration

robot.client = RosClient('127.0.0.1', 9090)
robot.client.run()

frame = Frame([0.3, 0.1, 0.5], [1, 0, 0], [0, 1, 0])
start_configuration = Configuration.from_revolute_values([0] * 6)
group = "manipulator"  # or robot.main_group_name

response = robot.inverse_kinematics(frame,
                                    start_configuration,
                                    group,
                                    constraints=None,
                                    attempts=50)
print(response.configuration)

robot.client.close()
robot.client.terminate()
