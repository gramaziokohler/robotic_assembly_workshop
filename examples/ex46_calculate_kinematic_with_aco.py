from ex23_load_robot import robot

import os
import math

from compas.geometry import Frame
from compas.datastructures import Mesh
from compas_fab.robots import Configuration
from compas_fab.backends import RosClient

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'cylinder.obj')

robot.client = RosClient()
robot.client.run()

goal_frame = Frame([0.20, 0.38, 0.32], [0, 1, 0], [0, 0, 1])

start_configuration = Configuration.from_revolute_values((-0.042, -1.988, 2.174, -3.327, -1.528, -6.283))
group = robot.main_group_name

# Create attached collision object
cylinder = Mesh.from_obj(PATH)
aco = robot.create_collision_mesh_attached_to_end_effector('cylinder', cylinder, group)

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
