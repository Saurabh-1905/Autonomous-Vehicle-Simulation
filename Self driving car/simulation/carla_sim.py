import carla
import random
import numpy as np
from main import main_pipeline

client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

world = client.get_world()
blueprint_library = world.get_blueprint_library()

vehicle_bp = blueprint_library.filter('vehicle.*')[0]
spawn_point = random.choice(world.get_map().get_spawn_points())
vehicle = world.spawn_actor(vehicle_bp, spawn_point)

print("Vehicle spawned at:", spawn_point.location)

print("Vehicle spawned at:", spawn_point.location)

spectator = world.get_spectator()
transform = vehicle.get_transform()
spectator.set_transform(carla.Transform(
    transform.location + carla.Location(z=10),
    carla.Rotation(pitch=-30)
))

import time

print("Testing vehicle movement...")

for _ in range(50):
    vehicle.apply_control(carla.VehicleControl(throttle=0.5, steer=0.0))
    time.sleep(0.1)
camera_bp = blueprint_library.find('sensor.camera.rgb')
camera = world.spawn_actor(camera_bp, carla.Transform(carla.Location(x=1.5, z=2.4)), attach_to=vehicle)

lidar_distance = 10

def process_image(image):
    global lidar_distance

    print("Processing frame...")  # 👈 ADD THIS LINE

    import numpy as np

    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    frame = array.reshape((image.height, image.width, 4))[:, :, :3]

    steering = main_pipeline(frame, lidar_distance)

    control = carla.VehicleControl()
    control.throttle = 0.5
    control.steer = float(steering)

    vehicle.apply_control(control)

camera.listen(lambda image: process_image(image))

import time

print("Simulation running...")

while True:
    time.sleep(1)