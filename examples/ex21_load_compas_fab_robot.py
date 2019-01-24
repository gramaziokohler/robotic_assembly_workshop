import os
import compas
from compas.robots import RobotModel
#from compas.robots import LocalPackageMeshLoader
from compas_fab.robots import Robot
from compas_fab.artists import BaseRobotArtist
#from compas_fab.ghpython import RobotArtist
from compas_fab.robots import RobotSemantics
from compas_fab.backends import RosClient

compas.PRECISION = '12f'

path = r"C:\Users\rustr\workspace\robot_description"
package = 'ur_description'
urdf_filename = os.path.join(path, package, "urdf", "ur5.urdf")
srdf_filename = os.path.join(path, package, "ur5.srdf")

model = RobotModel.from_urdf_file(urdf_filename)
artist = BaseRobotArtist(model)
#artist = RobotArtist(model)
semantics = RobotSemantics.from_srdf_file(srdf_filename, model)

robot = Robot(model, artist, semantics, client=None)
robot.info()
