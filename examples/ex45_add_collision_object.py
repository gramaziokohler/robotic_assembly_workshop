import os
import time

from ex21_load_compas_fab_robot import robot

from compas.datastructures import Mesh

floor = Mesh.from_stl(os.path.join(os.path.dirname(__file__), "floor.stl"))
robot.add_collision_mesh_to_planning_scene("floor", floor)
#robot.remove_collision_mesh_from_planning_scene("floor")

time.sleep(1)

