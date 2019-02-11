"""
Creates a robot model of a UR5 robot
and draws it in rhino.
"""
import os

from compas.robots import RobotModel
from compas.robots import LocalPackageMeshLoader
from compas_fab.rhino import RobotArtist

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'robot_description')

package = 'ur_description'
urdf_filename = os.path.join(PATH, package, "urdf", "ur5.urdf")

model = RobotModel.from_urdf_file(urdf_filename)

# Load external geometry files (i.e. meshes)
loader = LocalPackageMeshLoader(PATH, package)
model.load_geometry(loader)

artist = RobotArtist(model)
artist.draw_visual()
