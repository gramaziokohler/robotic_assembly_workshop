# load brick network from saved json file
# create rfl robot and client
# set start state, iterate over brick placing frames and ask if reachable
# from all reachable, exclude those which are not buildable (network) with fixed linear axes
# and generate fabrication sequence
# iterate over sequence and generate paths


import os
import json
import math
from threading import Thread

from compas.geometry import Frame
from compas.geometry import Vector
from compas.geometry import Transformation
from compas.utilities import await_callback
from compas.datastructures import Mesh
from compas.datastructures import mesh_transformed

from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
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
picking_frame = Frame([-0.353, -0.791, 0.566], [0, 1, 0], [1, 0, 0])
picking_configuration = Configuration.from_prismatic_and_revolute_values([-1.422], [-2.215, 0.678, 0.574, -6.283, 0.319, 5.639])

savelevel_vector = Vector(0, 0, 0.1)
group = "manipulator"

# Constrain movement of one axis 
pc = Constraints()
pc.joint_constraints.append(JointConstraint('axis_joint', picking_configuration.values[0], 0.05, 0.05, 1.))
pc.joint_constraints.append(JointConstraint('joint_1', picking_configuration.values[0], math.pi, math.pi, 1.))

savelevel_frame1 = Frame(picking_frame.point + savelevel_vector, picking_frame.xaxis, picking_frame.yaxis)



for i, placing_frames in enumerate(layers):

    print("=" * 30)
    print("Calculating %d. of %d layers..." % (i + 1, len(layers)))
    print("=" * 30)

    start_configuration = picking_configuration

    for j, placing_frame in enumerate(placing_frames):

        print("Calculating %d. of %d brick placing paths..." % (j + 1, len(placing_frames)))
        solutions = []
        savelevel_frame2 = Frame(placing_frame.point + savelevel_vector, placing_frame.xaxis, placing_frame.yaxis)

        response = await_callback(robot.inverse_kinematics, 
                                  frame_WCF=savelevel_frame2, 
                                  start_configuration=start_configuration, 
                                  group=group, 
                                  constraints=pc, 
                                  attempts=50)
        if response.error_code == MoveItErrorCodes.SUCCESS:
            start_configuration = response.configuration
            print(start_configuration)
        else:
            print(response.error_code.human_readable)


robot.client.close()
robot.client.terminate()


