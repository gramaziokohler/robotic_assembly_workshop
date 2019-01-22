# load brick network from saved json file
# create rfl robot and client
# set start state, iterate over brick placing frames and ask if reachable
# from all reachable, exclude those which are not buildable (network) with fixed linear axes
# and generate fabrication sequence
# iterate over sequence and generate paths
import os
import json
from threading import Thread

from compas.geometry import Frame
from compas.utilities import await_callback

from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends.ros import MoveItErrorCodes
from compas_fab.backends.ros import Constraints
from compas_fab.backends.ros import JointConstraint




from rfl_robot import robot

path = os.path.dirname(__file__)
filename = os.path.join(path, 'frames.json')

def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

frames = read_json(filename)
frames = [Frame.from_data(frame) for frame in frames]

robot.client = RosClient('127.0.0.1', 9090)

types = robot.get_configurable_joint_types()
values = [7009.358, -841.219, -2714.523, 1.371, 0.132, -1.703, 0.490, 0.000, 0.668, -4900.000, -2000.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000]
start_configuration = Configuration(values, types)

group = "rob11"

pc = Constraints()
print("pc", pc)
#names = ['gantry_joint', 'rob11_joint_cart', 'rob11_joint_cart_zaxis']
names = ['gantry_joint']
tol = 0.01
for name in names:
    pos = robot.get_position_by_joint_name(start_configuration, name)/robot.scale_factor
    pc.joint_constraints.append(JointConstraint(name, pos, tol, tol, 1.))

print(pc)

constraints = pc
#constraints = None

class Service(object):

    def loop(self, frames):
        self.frames = frames
        self.index = -1
        self.step()
        self.solution = []
    
    def step(self):
        self.index += 1
        if self.index == len(self.frames):
            robot.client.terminate()
            print("self.solution =", self.solution)
        else:
            print(self.index)
            frame = self.frames[self.index]
            #robot.inverse_kinematics(frame, start_configuration, self.response, group, True, constraints)
            tolerance_position = 5
            tolerance_angle = 10
            robot.motion_plan_goal_frame(frame, start_configuration, tolerance_position, tolerance_angle, self.response, group, goal_constraints=constraints, num_planning_attempts=8, allowed_planning_time=10.)

    def response(self, response):
        if response.error_code == MoveItErrorCodes.SUCCESS:
            print(response.configurations[-1])
            #print(response.configuration)
            self.solution.append(self.index)
        else:
            print(response.error_code.human_readable)
        self.step()

s = Service()
s.loop(frames)
    
#robot.client.call_later(3, robot.client.close)
#robot.client.call_later(5, robot.client.terminate)
robot.client.run_forever()




