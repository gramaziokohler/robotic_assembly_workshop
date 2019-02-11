"""
Creates a `Robot` representing a UR5 robot from a urdf model and the semantics 
from a srdf file.
"""
import os
import compas
from compas.robots import RobotModel
from compas_fab.robots import Robot
from compas_fab.robots import RobotSemantics
from compas_fab.backends import RosClient

compas.PRECISION = '12f'

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'robot_description')

package = 'ur_description'
urdf_filename = os.path.join(PATH, package, "urdf", "ur5.urdf")
srdf_filename = os.path.join(PATH, package, "ur5.srdf")

model = None
artist = None
semantics = None
robot = None
robot.info()
