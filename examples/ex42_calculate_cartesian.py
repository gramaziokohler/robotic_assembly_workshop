from ex21_load_compas_fab_robot import robot

from compas.geometry import Frame
from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends.ros import MoveItErrorCodes

client = RosClient('127.0.0.1', 9090)
robot.client = client

frames = []
frames.append(Frame([0.30, 0.10, 0.50], [1, 0, 0], [0, 1, 0]))
frames.append(Frame([0.20, 0.38, 0.32], [0, 1, 0], [0, 0, 1]))

start_configuration = Configuration.from_revolute_values([-0.042, 4.295, -4.110, -3.327, 4.755, 0.])
group = "manipulator" # or robot.main_group_name
max_step = 0.01
avoid_collisions = True

def callback_result(response):
   if response.error_code == MoveItErrorCodes.SUCCESS:
       print(response.configurations)
   else:
       print(response.error_code.human_readable)

robot.compute_cartesian_path(frames, start_configuration, max_step, avoid_collisions, callback_result, group)

client.call_later(3, client.close)
client.call_later(5, client.terminate)
client.run_forever()
