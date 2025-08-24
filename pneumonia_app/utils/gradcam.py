import torch
import cv2
import numpy as np

def generate_gradcam_yolo(model, img_path, target_layer="model.24"):
    """
    Sinh Grad-CAM cho YOLO11
    model: YOLO model đã load
    img_path: đường dẫn ảnh
    target_layer: tên layer backbone muốn hook (xem model.model để biết)
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()

    # Load ảnh
    img = cv2.imread(img_path)
    img_resized = cv2.resize(img, (640, 640))  # YOLO input
    img_tensor = torch.from_numpy(img_resized).permute(2, 0, 1).unsqueeze(0).float() / 255.0
    img_tensor = img_tensor.to(device)

    # Hook để lấy feature map + gradient
    activations = {}
    gradients = {}

    def forward_hook(module, input, output):
        activations["value"] = output

    def backward_hook(module, grad_in, grad_out):
        gradients["value"] = grad_out[0]

    # Lấy layer mục tiêu
    for name, layer in model.model.named_modules():
        if name == target_layer:
            layer.register_forward_hook(forward_hook)
            layer.register_full_backward_hook(backward_hook)

    # Forward
    preds = model(img_tensor)
    # Lấy class có confidence cao nhất
    score = preds[0].boxes.conf.max()
    score.backward()

    # Lấy grad & feature map
    grads = gradients["value"].detach().cpu().numpy()[0]
    fmap = activations["value"].detach().cpu().numpy()[0]

    # Tính trọng số
    weights = np.mean(grads, axis=(1, 2))

    # Tạo heatmap
    cam = np.zeros(fmap.shape[1:], dtype=np.float32)
    for i, w in enumerate(weights):
        cam += w * fmap[i, :, :]
    cam = np.maximum(cam, 0)
    cam = cam / cam.max()

    # Resize heatmap
    heatmap = cv2.resize(cam, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Overlay lên ảnh gốc
    overlay = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)

    return overlay, heatmap
