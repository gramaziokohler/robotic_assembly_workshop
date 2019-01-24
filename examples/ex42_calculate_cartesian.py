from ex21_load_compas_fab_robot import robot

from compas.geometry import Frame
from compas.utilities import await_callback

from compas_fab.robots import Configuration
from compas_fab.backends.ros import MoveItErrorCodes

frames = []
frames.append(Frame([0.30, 0.10, 0.50], [1, 0, 0], [0, 1, 0]))
frames.append(Frame([0.20, 0.38, 0.32], [0, 1, 0], [0, 0, 1]))

start_configuration = Configuration.from_revolute_values([-0.042, 4.295, -4.110, -3.327, 4.755, 0.])
group = "manipulator" # or robot.main_group_name

response = await_callback(robot.compute_cartesian_path, 
                          frames_WCF=frames, 
                          start_configuration=start_configuration, 
                          max_step=0.01, 
                          avoid_collisions=True, 
                          group=group, 
                          path_constraints=None)

print(response.error_code.human_readable)
if response.error_code == MoveItErrorCodes.SUCCESS:
    print("Computed cartesian path with %d configurations, " % len(response.configurations))
    print("following %d%% of requested trajectory." % (response.fraction * 100))
    print("Executing this path at full speed would take approx. %.3f seconds." % response.solution.joint_trajectory.points[-1].time_from_start.seconds())
    print(response.configurations)

robot.client.close()
robot.client.terminate()
