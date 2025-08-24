import joblib
from ultralytics import YOLO
import cv2
import numpy as np
from tensorflow.keras.applications import MobileNetV2

# ================== LOAD MODEL ==================

# Load YOLO model (dùng alias model cho gọn)
model = YOLO("models/best.pt")

# Load RandomForest + MobileNet bundle
rf_bundle = joblib.load("models/xray_rf_mobilenet.joblib")

# ================== HÀM DỰ ĐOÁN ==================

def predict_yolo(image_path: str):
    """Dự đoán bằng YOLO11"""
    results = model.predict(source=image_path, imgsz=224, conf=0.25)
    r = results[0]

    if hasattr(r, "probs") and r.probs is not None:
        top1_idx = r.probs.top1
        pred_label = r.names[top1_idx]
        conf = r.probs.top1conf.item()

        if pred_label == "PNEUMONIA":
            conclusion = "Có bệnh"
        elif pred_label == "NORMAL":
            conclusion = "Không bệnh"
        elif pred_label == "NOT_XRAY":
            conclusion = "Không phải X-ray phổi"
        else:
            conclusion = "Không xác định"

        return pred_label, conclusion, conf
    else:
        return "Unknown", "Không xác định", 0.0


def predict_rf(image_path: str):
    """Dự đoán bằng RandomForest + MobileNetV2"""
    rf = rf_bundle["rf"]
    class_names = rf_bundle["class_names"]
    img_size = rf_bundle["img_size"]

    # Khởi tạo lại base_model
    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        pooling="avg",
        input_shape=(img_size[0], img_size[1], 3)
    )

    # Tiền xử lý ảnh
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, tuple(img_size))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # Trích đặc trưng
    feat = base_model(img, training=False).numpy()

    # Dự đoán RF
    proba = rf.predict_proba(feat)[0]
    pred_idx = int(np.argmax(proba))
    pred_label = class_names[pred_idx]
    conf = float(proba[pred_idx])

    if pred_label == "PNEUMONIA":
        conclusion = "Có bệnh"
    elif pred_label == "NORMAL":
        conclusion = "Không bệnh"
    else:
        conclusion = "Không xác định"

    return pred_label, conclusion, conf
