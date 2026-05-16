def sensor_fusion(camera_steering, lidar_distance):
    if lidar_distance < 5:
        return camera_steering * 0.5
    return camera_steering