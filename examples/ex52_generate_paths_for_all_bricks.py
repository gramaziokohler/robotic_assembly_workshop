"""
Some clever text what this example is about...
"""

import os
import json
import math
import time
from threading import Thread

from compas.geometry import Frame
from compas.geometry import Vector
from compas.geometry import Transformation
from compas.utilities import await_callback
from compas.datastructures import Mesh
from compas.datastructures import mesh_transformed

from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends import RosError
from compas_fab.backends.ros import MoveItErrorCodes
from compas_fab.backends.ros import Constraints
from compas_fab.backends.ros import JointConstraint

from ex50_abb_linear_axis_robot import robot

robot.client = RosClient('127.0.0.1', 9090)
robot.client.run()

path = r"C:\Users\rustr\workspace\robot_description"
package = "abb_linear_axis"
mesh = Mesh.from_stl(os.path.join(path, package, 'meshes', 'collision', 'platform.stl'))
robot.add_collision_mesh_to_planning_scene('platform', mesh)


# Load frames 
path = os.path.dirname(__file__)
filename = os.path.join(path, 'frames.json')
with open(filename, 'r') as f:
    layers = json.load(f)
layers = [[Frame.from_data(frame) for frame in frames] for frames in layers]

# Settings
picking_frame = Frame([1.926, 1.5, 1], [0, 1, 0], [1, 0, 0])
picking_configuration = Configuration.from_prismatic_and_revolute_values([-0.0], [1.571, 0.108, 0.867, 0.000, 0.596, 3.142])


savelevel_vector = Vector(0, 0, 0.1)
group = "axis_abb"

# Constrain movement of one axis 
pc = Constraints()
#pc.joint_constraints.append(JointConstraint('axis_joint', picking_configuration.values[0], 0.05, 0.05, 1.))
pc.joint_constraints.append(JointConstraint('joint_2', picking_configuration.values[1], math.pi/2, math.pi/2, 1.))
#pc.joint_constraints.append(JointConstraint('joint_6', picking_configuration.values[6], math.pi/2, math.pi/2, 1.))
#pc = None

savelevel_frame1 = Frame(picking_frame.point + savelevel_vector, picking_frame.xaxis, picking_frame.yaxis)

# Calculate cartesian path between picking frame and savelevel_frame1
response = robot.compute_cartesian_path(frames_WCF=[picking_frame, savelevel_frame1], 
                                        start_configuration=picking_configuration, 
                                        max_step=0.01, 
                                        avoid_collisions=True, 
                                        group=group, 
                                        path_constraints=None)
if response.fraction != 1.:
    print(response.fraction)
    #raise Exception("Please check, something's wrong with picking configuration and frame...")

picking_configurations = response.configurations
start_configuration = picking_configurations[-1]
print("start_configuration", start_configuration)
start_configuration = robot.merge_group_with_full_configuration(start_configuration, picking_configuration, group)
print("start_configuration", start_configuration)

brick = Mesh.from_obj(os.path.join(os.path.dirname(__file__), "brick.obj"))
robot.add_attached_collision_mesh('brick', brick, group)
robot.remove_collision_mesh_from_planning_scene("brick_wall")

time.sleep(0.5) # TODO check if move_group has subscribed

for i, placing_frames in enumerate(layers):

    print("=" * 30)
    print("Calculating %d. of %d layers..." % (i + 1, len(layers)))
    print("=" * 30)

    for j, placing_frame in enumerate(placing_frames):

        print("Calculating %d. of %d brick placing paths..." % (j + 1, len(placing_frames)))
        solutions = []
        
        savelevel_frame2 = Frame(placing_frame.point + savelevel_vector, placing_frame.xaxis, placing_frame.yaxis)

        # Calculate kinematic path between savelevel_frame1 and savelevel_frame2
        try:
            response = robot.motion_plan_goal_frame(frame_WCF=savelevel_frame2, 
                                                    start_configuration=start_configuration, 
                                                    tolerance_position=0.005, 
                                                    tolerance_angle=math.radians(1), 
                                                    group=group,
                                                    path_constraints=pc, 
                                                    planner_id='RRT',
                                                    num_planning_attempts=20, 
                                                    allowed_planning_time=8.,
                                                    attached_collision_object=aco)
            configurations = response.configurations
            solutions.append(configurations)
        except RosError as error:
            print(error)
            break
        last_configuration = solutions[-1][-1]
        print("last_configuration", last_configuration)

        # Calculate cartesian path between savelevel_frame2 and placing_frame
        frames = [savelevel_frame2, placing_frame]
        try:
            print(last_configuration)
            response = robot.compute_cartesian_path(frames_WCF=frames, 
                                                    start_configuration=last_configuration, 
                                                    max_step=0.01, 
                                                    avoid_collisions=True, 
                                                    group=group, 
                                                    path_constraints=pc)
            if response.fraction == 1.:
                configurations = response.configurations
                solutions.append(configurations)
            else:
                print("Cartesian computed only %d percent of the path" % (response.fraction * 100))
                break
        except RosError as error:
            print("Cartesian:", error)
            break

        # Merge brick with brick_wall and publish new collision mesh
        # TODO
        brick_transformed = mesh_transformed(brick, Transformation.from_frame(placing_frame))
        robot.append_collision_mesh_to_planning_scene('brick_wall', brick_transformed)
        
        # Calculate kinematic path between savelevel_frame2 and savelevel_frame1
        try:
            response = robot.motion_plan_goal_frame(frame_WCF=savelevel_frame1, 
                                                    start_configuration=last_configuration, 
                                                    tolerance_position=0.005, 
                                                    tolerance_angle=math.radians(1), 
                                                    group=group,
                                                    path_constraints=pc, 
                                                    planner_id='RRT',
                                                    num_planning_attempts=20, 
                                                    allowed_planning_time=8.)

            configurations = response.configurations
            solutions.append(configurations)
        except RosError as error:
            print("Kinematic:", error)
            break

print(solutions)

robot.client.close()
robot.client.terminate()


