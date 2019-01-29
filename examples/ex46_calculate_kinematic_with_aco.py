from ex22_load_compas_fab_robot import robot

import os
import math
from compas.geometry import Frame
from compas.datastructures import Mesh
from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends.ros import MoveItErrorCodes

robot.client = RosClient('127.0.0.1', 9090)
robot.client.run()

goal_frame = Frame([0.20, 0.38, 0.32], [0, 1, 0], [0, 0, 1])

start_configuration = Configuration.from_revolute_values([-0.042, 4.295, -4.110, -3.327, 4.755, 0.])
group = robot.main_group_name

# Create attached collision object
brick = Mesh.from_obj(os.path.join(os.path.dirname(__file__), "brick.obj"))
aco = robot.create_collision_mesh_attached_to_end_effector('brick', brick, group)

response = robot.motion_plan_goal_frame(goal_frame,
                                        start_configuration,
                                        tolerance_position=0.001,
                                        tolerance_angle=math.radians(1),
                                        group=group,
                                        path_constraints=None,
                                        planner_id='RRT',
                                        num_planning_attempts=20,
                                        allowed_planning_time=8.,
                                        attached_collision_object=aco)

print("Computed kinematic path with %d configurations." % len(response.configurations))
print("Executing this path at full speed would take approx. %.3f seconds." % response.trajectory.joint_trajectory.points[-1].time_from_start.seconds())

for config in response.configurations:
    print(config)

robot.client.terminate()
