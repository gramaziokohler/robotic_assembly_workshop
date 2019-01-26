# load brick network from saved json file
# create rfl robot and client
# set start state, iterate over brick placing frames and ask if reachable
# from all reachable, exclude those which are not buildable (network) with fixed linear axes
# and generate fabrication sequence
# iterate over sequence and generate paths


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
group = "abb"

picking_frame = Frame([1.926, 1.5, 1], [0, 1, 0], [1, 0, 0])
picking_configuration = Configuration.from_prismatic_and_revolute_values([-1.800], [0.569, 0.849, -0.235, 6.283, 0.957, 2.140])

savelevel_vector = Vector(0, 0, 0.1)
savelevel_frame1 = Frame(picking_frame.point + savelevel_vector, picking_frame.xaxis, picking_frame.yaxis)

"""
solutions = []

for i, placing_frames in enumerate(layers):

    print("=" * 30)
    print("Calculating %d. of %d layers..." % (i + 1, len(layers)))
    print("=" * 30)

    start_configuration = picking_configuration

    solutions.append([])

    for j, placing_frame in enumerate(placing_frames):

        #print("Calculating %d. of %d brick placing paths..." % (j + 1, len(placing_frames)))

        savelevel_frame2 = Frame(placing_frame.point + savelevel_vector, placing_frame.xaxis, placing_frame.yaxis)

        try:
            response = robot.inverse_kinematics(frame_WCF=savelevel_frame2, 
                                                start_configuration=start_configuration, 
                                                group=group, 
                                                constraints=None, 
                                                attempts=20)
            start_configuration = response.configuration
            try:
                response = robot.inverse_kinematics(frame_WCF=placing_frame, 
                                                    start_configuration=start_configuration, 
                                                    group=group, 
                                                    constraints=None, 
                                                    attempts=20)
                start_configuration = response.configuration
                print(start_configuration)              
                solutions[i].append(j)
            except RosError as error:
                print(error)
        except RosError as error:
            print(error)
            
print(solutions)

"""
# Do somehting with solutions
solutions = [[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6]]

pc = None

brick = Mesh.from_obj(os.path.join(os.path.dirname(__file__), "brick.obj"))
aco = robot.create_collision_mesh_attached_to_end_effector('brick', brick, group)

for i, indices in enumerate(solutions):

    print("=" * 30)
    print("Calculating %d. of %d layers..." % (i + 1, len(solutions)))
    print("=" * 30)

    start_configuration = picking_configuration

    for j in indices:

        placing_frame = layers[i][j]
        savelevel_frame2 = Frame(placing_frame.point + savelevel_vector, placing_frame.xaxis, placing_frame.yaxis)
        print("savelevel_frame2", savelevel_frame2)

        #print("Calculating %d. of %d brick placing paths..." % (j + 1, len(placing_frames)))
        print(i, j)

        

        try:
            response = robot.motion_plan_goal_frame(frame_WCF=savelevel_frame2, 
                                                    start_configuration=picking_configuration, 
                                                    tolerance_position=0.005, 
                                                    tolerance_angle=math.radians(1), 
                                                    group=group,
                                                    path_constraints=pc, 
                                                    planner_id='RRT',
                                                    num_planning_attempts=20, 
                                                    allowed_planning_time=8.,
                                                    attached_collision_object=aco)
            configurations = response.configurations
            #solutions.append(configurations)
            print(configurations[-1])
        except RosError as error:
            print(error)
            break
        time.sleep(5)
        break
    break


robot.client.close()
robot.client.terminate()


