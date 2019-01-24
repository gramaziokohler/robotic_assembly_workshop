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

from compas.geometry import Frame, Vector
from compas.utilities import await_callback

from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends.ros import MoveItErrorCodes
from compas_fab.backends.ros import Constraints
from compas_fab.backends.ros import JointConstraint

from abb_linear_axis import robot

# 1. Load frames 
path = os.path.dirname(__file__)
filename = os.path.join(path, 'frames.json')
with open(filename, 'r') as f:
    layers = json.load(f)
layers = [[Frame.from_data(frame) for frame in frames] for frames in layers]

# 2. Configure
picking_frame = Frame([-0.353, -0.791, 0.566], [0, 1, 0], [1, 0, 0])
picking_configuration = Configuration([-1.392, -2.232, 0.966, 0.451, -6.283, 0.155, -0.661], robot.get_configurable_joint_types())
savelevel_vector = Vector(0, 0, 0.1)
group = "manipulator"
pc = Constraints()
pc.joint_constraints.append(JointConstraint('axis_joint', picking_configuration.values[0], 0.05, 0.05, 1.))
pc.joint_constraints.append(JointConstraint('joint_1', picking_configuration.values[0], math.pi, math.pi, 1.))
#pc = None

savelevel_point1 = Frame(picking_frame.point + savelevel_vector, picking_frame.xaxis, picking_frame.yaxis)

# cartesian path between picking frame and savelevel_point1
frames = [picking_frame, savelevel_point1]
response = await_callback(robot.compute_cartesian_path, 
                            frames_WCF=frames, 
                            start_configuration=picking_configuration, 
                            max_step=0.01, 
                            avoid_collisions=True, 
                            group=group, 
                            constraints=pc)

if response.error_code == MoveItErrorCodes.SUCCESS:
    if response.fraction == 1.:
        configurations = response.configurations
start_configuration = response.configurations[-1]
print("start_configuration", start_configuration)

for i, frames in enumerate(layers):

    print("%d of %d layers ===========" % (i, len(layers)))
    current_configuration = start_configuration
    for j, placing_frame in enumerate(frames):
        print(">>", j)

        
        savelevel_frame2 = Frame(placing_frame.point + savelevel_vector, placing_frame.xaxis, placing_frame.yaxis)

        """
        solutions = []

        # kinematic path between 
        tolerance_position = 0.005
        tolerance_angle = math.radians(1)
        response = await_callback(robot.motion_plan_goal_frame, 
                                  frame_WCF=savelevel_frame2, 
                                  start_configuration=start_configuration, 
                                  tolerance_position=tolerance_position, 
                                  tolerance_angle=tolerance_angle, 
                                  group=group,
                                  path_constraints=pc, 
                                  planner_id='RRT',
                                  num_planning_attempts=20, 
                                  allowed_planning_time=8.)

        if response.error_code == MoveItErrorCodes.SUCCESS:
            configurations = response.configurations
            # save configurations
            last_configuration = configurations[-1]
        else:
            print(response.error_code.human_readable)
            continue
        print("last_configuration", last_configuration)
        """
        print("current", current_configuration)
        response = await_callback(robot.inverse_kinematics, frame_WCF=savelevel_frame2, current_configuration=current_configuration, group=group, constraints=pc, attempts=50)
        if response.error_code == MoveItErrorCodes.SUCCESS:
            print("IK", response.configuration)
            current_configuration = response.configuration
        else:
            print(response.error_code.human_readable)

        #print("last_configuration", last_configuration)

        """
        frames = [savelevel_frame2, placing_frame]
        response = await_callback(robot.compute_cartesian_path, 
                                  frames_WCF=frames, 
                                  start_configuration=last_configuration, 
                                  max_step=0.01, 
                                  avoid_collisions=True, 
                                  group=group, 
                                  constraints=pc)

        last_configuration = None
        if response.error_code == MoveItErrorCodes.SUCCESS:
            if response.fraction == 1.:
                configurations = response.configurations
                # save configurations
                last_configuration = configurations[-1]
            else:
                print("Computed only %d percent of the path" % (response.fraction * 100))
                continue
        else:
            print(response.error_code.human_readable)
            print("Not possible to find path")
            continue
        print("last_configuration", last_configuration)
        """


robot.client.close()
robot.client.terminate()


