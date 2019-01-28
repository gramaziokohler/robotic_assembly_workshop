"""
Creates a robot model of a UR5 robot
from URDF/SRDF files.
"""
import os
import compas
from compas.robots import RobotModel
from compas.robots import LocalPackageMeshLoader
from compas_fab.robots import Robot

HERE = os.path.dirname(__file__)

package = 'ur_description'
path = os.path.join(HERE, "robot_description")
urdf_filename = os.path.join(path, package, "urdf", "ur5.urdf")
srdf_filename = os.path.join(path, package, "ur5.srdf")

model = RobotModel.from_urdf_file(urdf_filename)

# Load external geometry files (i.e. meshes)
loader = LocalPackageMeshLoader(path, package)
model.load_geometry(loader)

print(model)
