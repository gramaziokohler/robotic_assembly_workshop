import math
from ex21_load_compas_fab_robot import robot

from compas.geometry import Frame
from compas.utilities import await_callback

from compas_fab.robots import Configuration
from compas_fab.backends.ros import MoveItErrorCodes

goal_frame = Frame([0.20, 0.38, 0.32], [0, 1, 0], [0, 0, 1])

start_configuration = Configuration.from_revolute_values([-0.042, 4.295, -4.110, -3.327, 4.755, 0.])
group = "manipulator" # or robot.main_group_name

response = await_callback(robot.motion_plan_goal_frame, 
                          frame_WCF=goal_frame, 
                          start_configuration=start_configuration, 
                          tolerance_position=0.001, 
                          tolerance_angle=math.radians(1), 
                          group=group,
                          path_constraints=None, 
                          planner_id='RRT',
                          num_planning_attempts=20, 
                          allowed_planning_time=8.)

print(response.error_code.human_readable)
if response.error_code == MoveItErrorCodes.SUCCESS:
    print("Computed kinematic path with %d configurations." % len(response.configurations))
    print("Executing this path at full speed would take approx. %.3f seconds." % response.trajectory.joint_trajectory.points[-1].time_from_start.seconds())
    print(response.configurations)
    print(response.configurations)

robot.client.close()
robot.client.terminate()
