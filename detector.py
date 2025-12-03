from ultralytics import YOLO

class DetectorIA:
    def __init__(self, model_path="models/yolov8n.pt"):
        print("Cargando modelo YOLOv8...")
        self.model = YOLO(model_path)
        print("Modelo listo.")

    def detectar(self, img):
        # conf=0.35 para filtrar detecciones débiles
        results = self.model.predict(img, conf=0.35)
        return results[0]
