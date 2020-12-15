#!/usr/bin/env python

# ==============================================================================
# Sample tutorial code:
#    - connects to the CARLA Server;
#    - adds a car;
#    - adds a camera attached to the car;
#    - accelerates the car straight at maximum speed;
#    - displays captured images.
# ==============================================================================

__author__ = "Rambod Rahmani"
__copyright__ = "Copyright (C) 2020 Rambod Rahmani"
__license__ = "GPLv3"

import os
import sys
import time
import glob
import random
import numpy as np
import cv2

# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================
try:
    sys.path.append(glob.glob('carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

# ==============================================================================
# -- configuration---- ---------------------------------------------------------
# ==============================================================================
IM_HEIGHT = 480
IM_WIDTH = 640

# ==============================================================================
# -- callback method for the camera sensor -------------------------------------
# ==============================================================================
def process_image(image):
    raw_image = np.array(image.raw_data)

    # reshape raw image array to height, width, RGBA
    reshaped = raw_image.reshape((IM_HEIGHT, IM_WIDTH, 4))

    # remove alpha: not really needed at this point
    no_alpha = reshaped[:, :, :3]

    # show resulting image
    cv2.imshow("Front Camera", no_alpha)
    cv2.waitKey()
    cv2.destroyAllWindows()

    # return normalized image data for (an eventual) neural network
    return no_alpha/255.0

# ==============================================================================
# -- entry point ---------------------------------------------------------------
# ==============================================================================

# world actors list: need to keep track of them for final cleaning procedure
actors_list = []

try:
    # connect to CARLA server
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    # retrieve world
    world = client.get_world()

    # retrieve default blueprint library
    blueprint_library = world.get_blueprint_library()

    # retrieve vehicle blueprint
    vehicle_bp = blueprint_library.filter('model3')[0]
    print(vehicle_bp)

    # vehicle spawn point: chosen randomly
    spawn_point = random.choice(world.get_map().get_spawn_points())

    # spawn the vehicle into the world
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)

    # HARDCODED self-driving car using the CARLA engine: not good for simulating
    # human behavoir, just to simulate traffic, if you just wanted some NPCs to drive
    # around
    #vehicle.set_autopilot(True)

    # make the vehicle move straight at maximum speed
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))

    # ad the vehicle to the actors list
    actors_list.append(vehicle)

    # get the blueprint for an RGBA camera sensor
    camera_bp = blueprint_library.find('sensor.camera.rgb')

    # set camera blueprint attributes: change image dimension
    camera_bp.set_attribute('image_size_y', f'{IM_HEIGHT}')
    camera_bp.set_attribute('image_size_x', f'{IM_WIDTH}')

    # set camera blueprint attributes: change image field of view
    camera_bp.set_attribute('fov', '110')

    # set the time in seconds between sensor captures
    camera_bp.set_attribute('sensor_tick', '0.1')

    # camera spawn point (relative to the vehicle)
    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))

    # spawn the camera sensor and attach to the vehicle
    camera = world.spawn_actor(camera_bp, spawn_point, attach_to=vehicle)

    # add camera sensor to list of actors
    actors_list.append(camera)

    # set camera sensor callback
    camera.listen(lambda data: process_image(data))

    # wait some time before destroying everything
    time.sleep(5)

    # stop camera sensor
    camera.stop()

finally:
    print('Destroying actors.')
    for actor in actors_list:
        actor.destroy()
    print('All actors destroyed.')
