from ex23_load_robot import robot

import os
import time

from compas.datastructures import Mesh
from compas_fab.backends import RosClient

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'cylinder.obj')

robot.client = RosClient()
robot.client.run()

group = robot.main_group_name
cylinder = Mesh.from_obj(PATH)

robot.add_attached_collision_mesh('cylinder', cylinder, group)
time.sleep(2)

robot.remove_attached_collision_mesh('cylinder', group)
time.sleep(2)
