from PIL import Image
import os

def save_uploaded_file(uploaded_file, folder="uploads"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def is_xray(file_path):
    """
    Kiểm tra sơ bộ xem file có phải ảnh X-quang phổi hay không.
    - Ảnh X-quang thường là grayscale (mode 'L') hoặc RGB.
    - Kích thước tối thiểu để tránh ảnh lạ.
    """
    try:
        img = Image.open(file_path)
        # Kiểm tra mode ảnh
        if img.mode not in ["L", "RGB"]:
            return False
        # Kiểm tra kích thước tối thiểu
        if img.size[0] < 50 or img.size[1] < 50:
            return False
        return True
    except Exception:
        return False
