"""
"""


import os
import json

from compas.geometry import Frame
from compas.geometry import Vector
from compas.datastructures import Mesh

from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends import RosError

from ex50_abb_linear_axis_robot import robot

robot.client = RosClient('127.0.0.1', 9090)
robot.client.run()

# Add platform as collision mesh
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

save_vector = Vector(0, 0, 0.1)
saveframe_pick = Frame(picking_frame.point + save_vector, picking_frame.xaxis, picking_frame.yaxis)

solutions = []

# Iterate over placing frames
for i, placing_frames in enumerate(layers):

    print("=" * 30)
    print("Calculating %d. of %d layers..." % (i + 1, len(layers)))
    print("=" * 30)

    start_configuration = picking_configuration

    solutions.append([])

    for j, placing_frame in enumerate(placing_frames):

        # Calculate saveframe at placing frame
        saveframe_place = Frame(placing_frame.point + save_vector, placing_frame.xaxis, placing_frame.yaxis)

        # Check ik for placing_frame and saveframe_place
        # Only if both work, save to solutions
        try:
            response = robot.inverse_kinematics(frame_WCF=saveframe_place, 
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

# save solutions to json?            
print(solutions)

robot.client.close()
robot.client.terminate()


