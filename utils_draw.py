import cv2

def draw_boxes(img, detections):
    for box in detections.boxes:
        x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        label = f"{detections.names[cls]} {conf:.2f}"
        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(img, label, (x1, y1-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    return img
