import os

import compas
from compas.robots import Joint
from compas.robots import LocalPackageMeshLoader
from compas.robots import RobotModel
from compas_fab.backends import RosClient
from compas_fab.robots import Robot
from compas_fab.robots import RobotSemantics

#from compas_fab.ghpython import RobotArtist

compas.PRECISION = '12f'

HERE = os.path.dirname(__file__)

path = os.path.join(HERE, "robot_description")
packages = ['abb_irb4600_40_255', 'rfl']

loaders = [LocalPackageMeshLoader(path, package) for package in packages]

urdf_filename = "rfl.urdf"
srdf_filename = "rfl.srdf"
package = "rfl"

urdf_filename = os.path.join(path, package, "urdf", urdf_filename)
srdf_filename = os.path.join(path, package, srdf_filename)

model = RobotModel.from_urdf_file(urdf_filename)
#model.load_geometry(loader)
artist = None
#artist = RobotArtist(model)
semantics = RobotSemantics.from_srdf_file(srdf_filename, model)

robot = Robot(model, artist, semantics)
robot.scale(1000)

"""
print("planning groups:", robot.group_names)
print("main planning group:", robot.main_group_name)
print("base_frame:", robot.get_base_frame())
print("Joints of main planning group:")
for joint in robot.get_configurable_joints(robot.main_group_name):
    info = "\t%s is of type '%s'" % (joint.name, list(Joint.SUPPORTED_TYPES)[joint.type])
    if joint.limit:
        info += " and has limits [%.3f, %.3f]" % (joint.limit.upper, joint.limit.lower)
    print(info)

"""
