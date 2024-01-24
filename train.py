# BRGINE

from ultralytics import YOLO

# Load the model.
model = YOLO('yolov8.pt')

# Training.
results = model.train(
    data='custom_data.yaml',
    imgsz=1080,
    epochs=10,
    batch=8,
    name='yolov8_custom')


# END
