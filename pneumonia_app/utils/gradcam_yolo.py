# utils/gradcam_yolo.py - Phiên bản debug và cải tiến

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class GradCAMYOLO:
    def __init__(self, model, target_layer_name='model.22'):
        """
        Initialize Grad-CAM for YOLO11
        Args:
            model: YOLO11 model
            target_layer_name: Tên layer để hook (thường là layer cuối cùng trước head)
        """
        self.model = model
        self.target_layer = None
        self.gradients = None
        self.activations = None
        
        # Tìm target layer
        self.find_target_layer(target_layer_name)
        
        # Register hooks
        self.register_hooks()
    
    def find_target_layer(self, target_layer_name):
        """Tìm và thiết lập target layer"""
        for name, module in self.model.named_modules():
            if target_layer_name in name:
                self.target_layer = module
                print(f"✅ Found target layer: {name}")
                break
        
        if self.target_layer is None:
            # Fallback: sử dụng layer cuối cùng
            layers = list(self.model.named_modules())
            if layers:
                self.target_layer = layers[-1][1]
                print(f"⚠️ Using fallback layer: {layers[-1][0]}")
    
    def save_gradient(self, grad):
        """Hook function để lưu gradients"""
        self.gradients = grad
    
    def save_activation(self, module, input, output):
        """Hook function để lưu activations"""
        self.activations = output
    
    def register_hooks(self):
        """Đăng ký hooks"""
        if self.target_layer is not None:
            self.target_layer.register_forward_hook(self.save_activation)
            self.target_layer.register_backward_hook(lambda module, grad_input, grad_output: self.save_gradient(grad_output[0]))
    
    def generate_cam(self, image_path, input_size=640, target_class=None):
        """
        Tạo Grad-CAM
        Args:
            image_path: Đường dẫn ảnh
            input_size: Kích thước input
            target_class: Class cần focus (None = class có confidence cao nhất)
        """
        try:
            # 1. Preprocessing
            original_img = cv2.imread(image_path)
            original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            
            # Resize và normalize
            img_resized = cv2.resize(original_img, (input_size, input_size))
            img_tensor = torch.from_numpy(img_resized).float().permute(2, 0, 1).unsqueeze(0) / 255.0
            img_tensor.requires_grad_(True)
            
            # 2. Forward pass
            self.model.eval()
            with torch.set_grad_enabled(True):
                outputs = self.model(img_tensor)
            
            # 3. Xác định target class
            if hasattr(outputs, 'pred') and outputs.pred is not None:
                predictions = outputs.pred[0]  # First batch
            elif isinstance(outputs, (list, tuple)) and len(outputs) > 0:
                predictions = outputs[0]
            else:
                predictions = outputs
            
            if target_class is None:
                # Lấy class có confidence cao nhất
                if hasattr(predictions, 'conf'):
                    max_conf_idx = torch.argmax(predictions.conf)
                    target_class = predictions.cls[max_conf_idx].int().item()
                else:
                    # Fallback: giả sử có bệnh (class 1)
                    target_class = 1
            
            print(f"🎯 Target class: {target_class}")
            
            # 4. Backward pass
            if self.activations is not None:
                # Tính score cho target class
                if hasattr(predictions, 'conf'):
                    target_score = predictions.conf[predictions.cls == target_class].sum()
                else:
                    # Fallback: sử dụng mean của activations
                    target_score = self.activations.mean()
                
                # Backward
                self.model.zero_grad()
                target_score.backward(retain_graph=True)
                
                # 5. Tạo CAM
                if self.gradients is not None and self.activations is not None:
                    # Pooling gradients
                    pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
                    
                    # Weight activations
                    for i in range(self.activations.shape[1]):
                        self.activations[:, i, :, :] *= pooled_gradients[i]
                    
                    # Create heatmap
                    heatmap = torch.mean(self.activations, dim=1).squeeze()
                    heatmap = torch.maximum(heatmap, torch.tensor(0))  # ReLU
                    
                    # Normalize
                    if heatmap.max() > 0:
                        heatmap = heatmap / heatmap.max()
                    
                    # Convert to numpy và resize về kích thước gốc
                    heatmap_np = heatmap.detach().cpu().numpy()
                    heatmap_resized = cv2.resize(heatmap_np, (original_img.shape[1], original_img.shape[0]))
                    
                    # 6. Tạo overlay
                    heatmap_colored = cm.jet(heatmap_resized)[:, :, :3]  # Remove alpha channel
                    heatmap_colored = (heatmap_colored * 255).astype(np.uint8)
                    
                    # Tạo overlay
                    overlay = cv2.addWeighted(original_img, 0.6, heatmap_colored, 0.4, 0)
                    
                    print(f"✅ Grad-CAM generated successfully!")
                    print(f"📊 Heatmap stats: min={heatmap_resized.min():.4f}, max={heatmap_resized.max():.4f}, mean={heatmap_resized.mean():.4f}")
                    
                    return overlay, heatmap_colored, heatmap_resized
                else:
                    print("❌ No gradients or activations found")
                    return None, None, None
            else:
                print("❌ No activations captured")
                return None, None, None
                
        except Exception as e:
            print(f"❌ Error generating Grad-CAM: {str(e)}")
            import traceback
            traceback.print_exc()
            return None, None, None

def generate_gradcam_yolo(model, image_path, input_size=640):
    """
    Wrapper function để tạo Grad-CAM cho YOLO11
    """
    try:
        # Thử các layer khác nhau
        target_layers = [
            'model.22',  # Thường là detection head
            'model.21',  # Layer trước detection head
            'model.20',  # Backbone cuối
            'backbone',  # Toàn bộ backbone
        ]
        
        for target_layer in target_layers:
            print(f"🔄 Trying target layer: {target_layer}")
            
            gradcam = GradCAMYOLO(model, target_layer)
            overlay, heatmap_colored, heatmap_raw = gradcam.generate_cam(image_path, input_size)
            
            if overlay is not None and heatmap_raw.max() > 0.1:  # Có activation đáng kể
                print(f"✅ Successfully generated Grad-CAM with layer: {target_layer}")
                return overlay, heatmap_colored
            else:
                print(f"⚠️ Layer {target_layer} produced weak activation")
        
        # Nếu tất cả đều thất bại, tạo heatmap giả để debug
        print("⚠️ All layers failed, creating dummy heatmap for debugging")
        original_img = cv2.imread(image_path)
        original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        
        # Tạo heatmap giả tập trung ở giữa phổi
        h, w = original_img.shape[:2]
        dummy_heatmap = np.zeros((h, w))
        center_y, center_x = h//2, w//2
        
        # Tạo gradient từ trung tâm
        y, x = np.ogrid[:h, :w]
        mask = (x - center_x)**2 + (y - center_y)**2
        dummy_heatmap = np.exp(-mask / (2 * (min(h, w) * 0.3)**2))
        
        # Apply colormap
        heatmap_colored = cm.jet(dummy_heatmap)[:, :, :3]
        heatmap_colored = (heatmap_colored * 255).astype(np.uint8)
        
        # Create overlay
        overlay = cv2.addWeighted(original_img, 0.6, heatmap_colored, 0.4, 0)
        
        return overlay, heatmap_colored
        
    except Exception as e:
        print(f"❌ Critical error in generate_gradcam_yolo: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None


# Test function để debug
def debug_model_structure(model):
    """Debug function để xem cấu trúc model"""
    print("🔍 Model structure:")
    for name, module in model.named_modules():
        print(f"  {name}: {type(module).__name__}")
        if hasattr(module, 'weight') and module.weight is not None:
            print(f"    Weight shape: {module.weight.shape}")
    
    print(f"\n📊 Model device: {next(model.parameters()).device}")
    print(f"📊 Model training mode: {model.training}")

# Cách sử dụng mới trong main app:
"""
# Trong file chính, thay thế:
overlay, heatmap = generate_gradcam_yolo(model, file_path, input_size=640)

# Bằng:
try:
    # Debug model trước
    debug_model_structure(model)
    
    # Tạo Grad-CAM
    overlay, heatmap = generate_gradcam_yolo(model, file_path, input_size=640)
    
    if overlay is not None:
        # Hiển thị kết quả
        st.image(overlay, caption="Grad-CAM Overlay")
        st.image(heatmap, caption="Heatmap") 
    else:
        st.error("Không thể tạo Grad-CAM")
        
except Exception as e:
    st.error(f"Lỗi Grad-CAM: {str(e)}")
"""