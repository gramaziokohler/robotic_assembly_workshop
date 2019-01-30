"""
Creates a full *COMPAS_FAB* robot class representing
a UR5 robot from a urdf model and the semantics from a srdf file.
"""
import os
import compas
from compas.robots import RobotModel
from compas_fab.robots import Robot
from compas_fab.robots import RobotSemantics
from compas_fab.backends import RosClient
from compas_

compas.PRECISION = '12f'

HERE = os.path.dirname(__file__)

package = 'ur_description'
path = os.path.join(HERE, "robot_description")
urdf_filename = os.path.join(path, package, "urdf", "ur5.urdf")
srdf_filename = os.path.join(path, package, "ur5.srdf")

model = 
artist = 
semantics = 
robot = 
robot.info()
