from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
import tempfile
import os

from detector import DetectorIA
from utils_draw import draw_boxes

app = Flask(__name__)

# Carga del modelo YOLOv8
detector = DetectorIA("models/yolov8n.pt")

@app.route("/")
def index():
    return jsonify({"status": "ok", "service": "yolo-ia"})

@app.route("/detect", methods=["POST"])
def detect():
    if "image" not in request.files:
        return jsonify({"error": "No image"}), 400

    file = request.files["image"]
    img_bytes = file.read()

    # Decodificar imagen
    try:
        arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    except Exception:
        return jsonify({"error": "Invalid image"}), 400

    # Inferencia
    detections = detector.detectar(img)

    resultado = []
    for box in detections.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cls = int(box.cls[0])
        name = detections.names[cls]
        conf = float(box.conf[0])
        resultado.append({
            "label": name,
            "confidence": conf,
            "box": [x1, y1, x2, y2]
        })

    # Devolver imagen con cajas si se pide
    if request.args.get("draw") == "1":
        img_draw = draw_boxes(img.copy(), detections)
        tmp = tempfile.mktemp(suffix=".jpg")
        cv2.imwrite(tmp, img_draw)
        return send_file(tmp, mimetype="image/jpeg")

    return jsonify({
        "detections": resultado,
        "num_objects": len(resultado)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
