import cv2
import numpy as np

def detect_lane(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    height = edges.shape[0]
    mask = np.zeros_like(edges)

    polygon = np.array([[
        (0, height),
        (frame.shape[1], height),
        (frame.shape[1], int(height * 0.6)),
        (0, int(height * 0.6))
    ]])

    cv2.fillPoly(mask, polygon, 255)
    cropped = cv2.bitwise_and(edges, mask)

    lines = cv2.HoughLinesP(cropped, 2, np.pi/180, 100,
                            minLineLength=40, maxLineGap=5)

    lane_center = frame.shape[1] // 2

    if lines is not None:
        x_coords = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            x_coords.extend([x1, x2])

        lane_center = int(np.mean(x_coords))

    return lane_center