import os

import compas
from compas.robots import RobotModel
from compas.robots import LocalPackageMeshLoader
from compas.robots import Joint
from compas.datastructures import Mesh

from compas_fab.robots import Robot
from compas_fab.robots import RobotSemantics
from compas_fab.artists import BaseRobotArtist
from compas_fab.backends import RosClient
from compas_fab.backends import RosError

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
artist = BaseRobotArtist(model)
#artist = RobotArtist(model)
semantics = RobotSemantics.from_srdf_file(srdf_filename, model)

robot = Robot(model, artist, semantics)
#robot.info()

print(robot.get_base_frame("abb"))
print(robot.get_base_frame("axis_abb"))

group = "abb"
base_link_name = robot.get_base_link_name(group)
ee_name = robot.get_end_effector_link_name(group)
print(base_link_name)
print(ee_name)
links_with_geometry = []
for link in robot.model.iter_link_chain(base_link_name, ee_name):
    if len(link.collision) or len(link.visual):
        links_with_geometry.append(link.name)
print(links_with_geometry)