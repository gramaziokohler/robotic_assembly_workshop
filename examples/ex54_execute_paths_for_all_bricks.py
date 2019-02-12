"""
Execute fabrication process for all bricks.

1. Load assembly from '53_wall_paths.json'
"""

import os
import sys
import time

from compas_fab.robots import Configuration
from compas_fab.backends import RosClient
from compas_fab.backends import RosError

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_block_building_sequence

from ex50_abb_linear_axis_robot import robot

# SETTINGS =====================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, '53_wall_paths.json')

robot.client = RosClient()
robot.client.run()

group = "abb"

# Load assembly
assembly = Assembly.from_json(PATH)

# Get the top keys of the assembly
c_max = max(assembly.get_vertices_attribute('course'))
keys_on_top = list(assembly.vertices_where({'course': c_max}))

# Iterate over keys on top
for key_on_top in keys_on_top:

    # Define the sequence to be checked if buildable
    sequence = assembly_block_building_sequence(assembly, key_on_top)

    # only include keys that are buildable and have not been built already
    include_keys = list(assembly.vertices_where_predicate(lambda key, attr: not attr['is_built'] and attr['is_buildable'], False))
    sequence = [k for k in sequence if k in include_keys]  # keep order

    print("Will begin fabricating sequence:", sequence)

    # Iterate over the sequence
    for key in sequence:
        paths = assembly.get_vertex_attribute(key, 'paths')

        for index, path in enumerate(paths):
            action_data = dict(started_at=time.strftime('%X'), state='EXECUTING')

            def completion(result):
                if action_data['state'] == 'EXECUTING':
                    action_data['state'] = 'SUCCESSFUL'
                action_data['completed_at'] = time.strftime('%X')
                del action_data['cancellable']

            def failure(e):
                action_data['state'] = 'ERROR'
                action_data['completed_at'] = time.strftime('%X')
                action_data['exception'] = e

            options = dict(joint_trajectory=path['joint_trajectory'],
                           callback=completion,
                           errback=failure,
                           timeout=None)

            print('Executing trajectory {}/{} of brick {}'.format(index + 1, len(paths), key))

            cancellable = robot.client.follow_joint_trajectory(**options)
            action_data['cancellable'] = cancellable

            while action_data['state'] == 'EXECUTING':
                print('.', end='', flush=True)
                time.sleep(0.5)

            print()
            print('Task {state}: Started at {started_at}, finished at {completed_at}'.format(**action_data))

        assembly.set_vertex_attribute(key, 'is_built', True)

        while True:
            print('Select one of the options:')
            opt = input('a) Save and build next brick? b) Next brick without saving, c) Stop [a/b/c]: ').lower()
            if opt in ['a', 'b', 'c']:
                break

        if opt == 'a':
            assembly.to_json(PATH)
        if opt == 'c':
            print('Stop')
            sys.exit(0)

robot.client.close()
robot.client.terminate()
