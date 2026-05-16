import sys
import os

# Ensure local modules are found
sys.path.insert(0, os.getcwd())

# ==============================
# IMPORTS
# ==============================
from perception.lane_detection import detect_lane
from perception.object_detection import detect_objects
from fusion.sensor_fusion import sensor_fusion
from control.controller import compute_control


# ==============================
# GLOBAL (for smoothing)
# ==============================
previous_steering = 0


# ==============================
# MAIN PIPELINE
# ==============================
def main_pipeline(frame, lidar_data):

    global previous_steering

    # ==============================
    # PERCEPTION
    # ==============================
    lane_center = detect_lane(frame)
    detections = detect_objects(frame)

    # ==============================
    # SAFE FALLBACK (IMPORTANT)
    # ==============================
    frame_center = frame.shape[1] // 2

    if lane_center is None or lane_center == 0:
        lane_center = frame_center

    # ==============================
    # ERROR CALCULATION
    # ==============================
    error = lane_center - frame_center

    # ==============================
    # DEAD ZONE (NO UNNECESSARY TURNING)
    # ==============================
    if abs(error) < 20:
        steering = 0.0
    else:
        steering = error * 0.004

    # ==============================
    # SMOOTHING (VERY IMPORTANT)
    # ==============================
    steering = 0.7 * previous_steering + 0.3 * steering
    previous_steering = steering

    # ==============================
    # LIMIT STEERING (STABILITY)
    # ==============================
    steering = max(min(steering, 0.5), -0.5)

    # ==============================
    # SENSOR FUSION
    # ==============================
    steering = sensor_fusion(steering, lidar_data)

    # ==============================
    # CONTROL (OBSTACLE HANDLING)
    # ==============================
    final_steering = compute_control(steering, detections)

    # ==============================
    # FINAL SAFETY CLAMP
    # ==============================
    final_steering = max(min(final_steering, 1.0), -1.0)

    return final_steering