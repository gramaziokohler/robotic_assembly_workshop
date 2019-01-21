from ex20_load_compas_fab_robot import robot

from compas.geometry import Frame
from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends.ros import MoveItErrorCodes

robot.client = RosClient('127.0.0.1', 9090)

frame = Frame([0.3, 0.1, 0.5], [1, 0, 0], [0, 1, 0])
start_configuration = Configuration.from_revolute_values([0] * 6)
group = "manipulator" # or robot.main_group_name

def callback_result(response):
    if response.error_code == MoveItErrorCodes.SUCCESS:
        print(response.configuration)
    else:
        print(response.error_code.human_readable)

robot.inverse_kinematics(frame, start_configuration, callback_result, group)

robot.client.call_later(3, robot.client.close)
robot.client.call_later(5, robot.client.terminate)
robot.client.run_forever()