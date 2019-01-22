import os

import compas
from compas.robots import RobotModel
from compas.robots import LocalPackageMeshLoader
from compas.robots import Joint

from compas_fab.robots import Robot
from compas_fab.robots import RobotSemantics
from compas_fab.backends import RosClient

#from compas_fab.ghpython import RobotArtist

compas.PRECISION = '12f'

path = r"C:\Users\rustr\workspace\robot_description"
package = 'ur_description'

loader = LocalPackageMeshLoader(path, package)

urdf_filename = "ur5.urdf"
srdf_filename = "ur5.srdf"

urdf_filename = os.path.join(path, package, "urdf", urdf_filename)
srdf_filename = os.path.join(path, package, srdf_filename)

model = RobotModel.from_urdf_file(urdf_filename)
# model.load_geometry(loader)
artist = None
# artist = RobotArtist(model)
semantics = RobotSemantics.from_srdf_file(srdf_filename, model)

robot = Robot(model, artist, semantics)

print("planning groups:", robot.group_names)
print("main planning group:", robot.main_group_name)
print("base_frame:", robot.get_base_frame())
print("Joints of main planning group:")
for joint in robot.get_configurable_joints(robot.main_group_name):
    info = "\t%s is of type '%s'" % (joint.name, list(Joint.SUPPORTED_TYPES)[joint.type])
    if joint.limit:
        info += " and has limits [%.3f, %.3f]" % (joint.limit.upper, joint.limit.lower)
    print(info)

