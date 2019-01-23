import os

import compas
from compas.robots import RobotModel
from compas.robots import LocalPackageMeshLoader
from compas.robots import Joint
from compas.datastructures import Mesh

from compas_fab.robots import Robot
from compas_fab.robots import RobotSemantics
from compas_fab.backends import RosClient

compas.PRECISION = '12f'

path = r"C:\Users\rustr\workspace\robot_description"
#packages = ['abb_irb4600_40_255', 'abb_linear_axis', 'abb_end_effectors']
#loaders = [LocalPackageMeshLoader(path, package) for package in packages]

urdf_filename = "abb_linear_axis_brick_suction_tool.urdf"
srdf_filename = "abb_linear_axis_suction_tool.srdf"
#urdf_filename = "abb_linear_axis.urdf"
#srdf_filename = "abb_linear_axis.srdf"
package = "abb_linear_axis"

urdf_filename = os.path.join(path, package, "urdf", urdf_filename)
srdf_filename = os.path.join(path, package, srdf_filename)

model = RobotModel.from_urdf_file(urdf_filename)
#model.load_geometry(loader)
artist = None
#artist = RobotArtist(model)
semantics = RobotSemantics.from_srdf_file(srdf_filename, model)

client = RosClient('127.0.0.1', 9090)
client.run()

robot = Robot(model, artist, semantics, client)
#robot.info()

mesh = Mesh.from_stl(os.path.join(path, package, 'meshes', 'collision', 'platform.stl'))
robot.add_collision_mesh_to_planning_scene('platform', mesh)