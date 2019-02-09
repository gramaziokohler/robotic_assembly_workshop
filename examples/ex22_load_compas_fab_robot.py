"""
Creates a full *COMPAS_FAB* robot class representing
a UR5 robot from a urdf model and the semantics from a srdf file.
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
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'robot_description')

package = 'ur_description'
urdf_filename = os.path.join(PATH, package, "urdf", "ur5.urdf")
srdf_filename = os.path.join(PATH, package, "ur5.srdf")

model = RobotModel.from_urdf_file(urdf_filename)

# Load external geometry files (i.e. meshes)
# loader = LocalPackageMeshLoader(PATH, 'ur_description')
# model.load_geometry(loader)

artist = None
#artist = RobotArtist(model)

semantics = RobotSemantics.from_srdf_file(srdf_filename, model)

robot = Robot(model, artist, semantics, client=None)
robot.info()
