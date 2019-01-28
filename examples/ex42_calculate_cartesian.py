"""
Compute the cartesian path based on 2 frames and a starting configuration.
"""
from ex21_load_compas_fab_robot import robot

from compas.geometry import Frame
from compas_fab.backends import RosClient
from compas_fab.backends.ros import MoveItErrorCodes
from compas_fab.robots import Configuration

robot.client = RosClient('127.0.0.1', 9090)
robot.client.run()

frames = []
frames.append(Frame([0.3, 0.1, 0.5], [1, 0, 0], [0, 1, 0]))
frames.append(Frame([0.4, 0.3, 0.4], [0, 1, 0], [0, 0, 1]))

start_configuration = Configuration.from_revolute_values((-0.042, -1.988, 2.174, -3.327, -1.528, -6.283))
group = "manipulator" # or robot.main_group_name

response = robot.compute_cartesian_path(frames,
                                        start_configuration,
                                        max_step=0.01,
                                        avoid_collisions=True,
                                        group=group,
                                        path_constraints=None)

print("Computed cartesian path with %d configurations, " % len(response.configurations))
print("following %d%% of requested trajectory." % (response.fraction * 100))
print("Executing this path at full speed would take approx. %.3f seconds." % response.solution.joint_trajectory.points[-1].time_from_start.seconds())
print(response.configurations)

robot.client.close()
robot.client.terminate()
