# Isaac ROS YOLOv8

## Quickstart

```sh
ros2 launch isaac_ros_yolov8 isaac_ros_yolov8.launch.py
```

## Exporting YOLO models

Export the trained `.pt` file to `.onnx`, specifying the `imgsz` parameter. e.g.:

```python
from ultralytics import YOLO
model = YOLO(f"weights/yolov8n_050624_imgsz_640_1.pt")
model.export(format="onnx", imgsz=(480, 640))
```

## Netron

(netron)[https://netron.app] can be used to obtain the required parameters for `isaac_ros_yolov8.launch.py`.

- `out_dim` can be obtained by loading the `.onnx` file and checking the dimensions at the very bottom.
- `num_classes` and the class labels can be obtained from the `.pt` file, the `names: dict` somewhere near the bottom.
