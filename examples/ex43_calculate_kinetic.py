from ex20_load_compas_fab_robot import robot

import math
from compas.geometry import Frame
from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends.ros import MoveItErrorCodes

client = RosClient('127.0.0.1', 9090)
robot.client = client

goal_frame = Frame([0.20, 0.38, 0.32], [0, 1, 0], [0, 0, 1])

start_configuration = Configuration.from_revolute_values([-0.042, 4.295, -4.110, -3.327, 4.755, 0.])
group = "manipulator" # or robot.main_group_name
tolerance_position = 0.001
tolerance_angle = math.radians(1)
path_constraints = None

def callback_result(response):
   if response.error_code == MoveItErrorCodes.SUCCESS:
       print(response.configurations)
   else:
       print(response.error_code.human_readable)

robot.motion_plan_goal_frame(goal_frame, start_configuration, tolerance_position, tolerance_angle, callback_result, group, path_constraints, num_planning_attempts=10, allowed_planning_time=10.)

client.call_later(12, client.close)
client.call_later(14, client.terminate)
client.run_forever()
