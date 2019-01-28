"""
Creates a ur5 robot from a urdf model and loads
the semantics from a srdf file.
"""
import os
import compas
from compas.robots import RobotModel
from compas.robots import LocalPackageMeshLoader
from compas_fab.robots import Robot
from compas_fab.robots import RobotSemantics
from compas_fab.backends import RosClient
#from compas_fab.ghpython import RobotArtist

compas.PRECISION = '12f'

HERE = os.path.dirname(__file__)

path = os.path.join(HERE, "robot_description")
package = 'ur_description'
urdf_filename = os.path.join(path, package, "urdf", "ur5.urdf")
srdf_filename = os.path.join(path, package, "ur5.srdf")
# loader = LocalPackageMeshLoader(path, 'ur_description')

model = RobotModel.from_urdf_file(urdf_filename)
# model.load_geometry(loader)

artist = None
#artist = RobotArtist(model)

semantics = RobotSemantics.from_srdf_file(srdf_filename, model)

robot = Robot(model, artist, semantics, client=None)
robot.info()
