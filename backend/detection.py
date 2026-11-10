import os
from pathlib import Path

class ObjectDetector:
    def __init__(self):
        self.model=None; self.error=None
        model_path=os.getenv('YOLO_MODEL','')
        try:
            from ultralytics import YOLO
            # Explicit custom weights take priority; otherwise use pretrained YOLOv8 nano.
            self.model=YOLO(model_path if model_path and Path(model_path).exists() else 'yolov8n.pt')
        except Exception as exc: self.error=str(exc)
    def detect(self,frame):
        if self.model is None: return [],self.error or 'YOLO model unavailable'
        try:
            result=self.model.predict(frame,verbose=False,conf=0.3)[0]
            found=[]
            for box in result.boxes:
                cls=int(box.cls[0]); conf=float(box.conf[0]); name=self.model.names[cls]
                found.append({'label':str(name).lower(),'confidence':round(conf,3),'box':[round(float(v),3) for v in box.xyxy[0].tolist()]})
            return found,None
        except Exception as exc: return [],str(exc)

detector=ObjectDetector()
