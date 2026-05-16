def compute_control(steering, detections):
    
    for cls, conf in detections:
        if cls == 0 and conf > 0.5:  # person detected
            
            # adjust steering dynamically
            if steering > 0:
                return steering - 0.3
            else:
                return steering + 0.3

    return steering