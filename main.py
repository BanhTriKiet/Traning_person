from ultralytics import YOLO

model = YOLO("./Model/yolo11n.pt")
if __name__ == "__main__":
    model.train(data="train.yaml",epochs=50,device='0', batch=32,imgsz=320,tracker='bytetrack.yaml')