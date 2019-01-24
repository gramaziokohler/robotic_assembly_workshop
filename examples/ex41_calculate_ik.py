from ex21_load_compas_fab_robot import robot

from compas.geometry import Frame
from compas.utilities import await_callback

from compas_fab.robots import Configuration
from compas_fab.backends.ros import MoveItErrorCodes

frame = Frame([0.3, 0.1, 0.5], [1, 0, 0], [0, 1, 0])
start_configuration = Configuration.from_revolute_values([0] * 6)
group = "manipulator" # or robot.main_group_name

response = await_callback(robot.inverse_kinematics, 
                          frame_WCF=frame,
                          start_configuration=start_configuration,
                          group=group,
                          constraints=None,
                          attempts=50)

print(response.error_code.human_readable)
if response.error_code == MoveItErrorCodes.SUCCESS:
    print(response.configuration)

robot.client.close()
robot.client.terminate()
