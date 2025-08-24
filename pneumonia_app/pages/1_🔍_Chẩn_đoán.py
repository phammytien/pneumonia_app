import streamlit as st, os


from utils.ml_models import predict_yolo, predict_rf, model  # đảm bảo bạn load model YOLO11 ở đây
from utils.preprocess import save_uploaded_file, is_xray
from utils.db_utils import get_connection, add_log
from utils.speak import speak
from utils.gist import show_diagnosis_conclusion
from utils.gradcam_yolo import generate_gradcam_yolo  # Import Grad-CAM cho YOLO11

st.set_page_config(page_title="Chẩn đoán", layout="wide")

# Custom CSS cho giao diện đẹp
st.markdown("""
<style>
    /* Màu nền chính */
    .main {
        background-color: #f8fbff;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #4a90e2 0%, #2c5aa0 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(74, 144, 226, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    
    .main-header p {
        color: #e8f4f8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Card containers */
    .card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e3f2fd;
    }
    
    .image-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 2px dashed #81c784;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .result-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #4caf50;
    }
    
    .control-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #f8faff 100%);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-top: 4px solid #2196f3;
    }
    
    .gradcam-card {
        background: linear-gradient(135deg, #fff3e0 0%, #fff8f0 100%);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #ff9800;
        margin-top: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4a90e2 0%, #2c5aa0 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.4);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 10px;
        border: 2px solid #e3f2fd;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background-color: white;
        border-radius: 10px;
        border: 2px dashed #4a90e2;
        padding: 2rem;
    }
    
    /* Results styling */
    .result-success {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    
    .result-warning {
        background: linear-gradient(135deg, #fff3e0 0%, #fff8f0 100%);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
    }
    
    .result-error {
        background: linear-gradient(135deg, #ffebee 0%, #fef5f5 100%);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #f44336;
        margin: 1rem 0;
    }
    
    /* Section titles */
    .section-title {
        color: #2c5aa0;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e3f2fd;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #f8faff 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #b3e5fc;
    }
    
    /* Progress bar */
    .confidence-bar {
        background: #e3f2fd;
        border-radius: 10px;
        padding: 0.2rem;
        margin: 0.5rem 0;
    }
    
    .confidence-fill {
        background: linear-gradient(90deg, #4caf50 0%, #81c784 100%);
        border-radius: 8px;
        height: 20px;
        text-align: center;
        color: white;
        font-weight: bold;
        line-height: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header chính
st.markdown("""
<div class="main-header">
    <h1>🩻 Hệ thống Chẩn đoán Bệnh Phổi</h1>
    <p>Sử dụng AI để phân tích ảnh X-quang và đưa ra chẩn đoán chính xác</p>
</div>
""", unsafe_allow_html=True)

# Kiểm tra đăng nhập
if "user" not in st.session_state or not st.session_state.logged_in:
    st.markdown("""
    <div class="result-error">
        <h3>⚠️ Cần đăng nhập</h3>
        <p>Bạn cần đăng nhập để sử dụng chức năng chẩn đoán này.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Layout chính - 3 lớp
# Lớp 1: Thao tác và điều khiển
st.markdown('<h3 class="section-title">🔧 Bảng điều khiển</h3>', unsafe_allow_html=True)

col_ctrl1, col_ctrl2 = st.columns([1, 1])

with col_ctrl1:
    algorithm_choice = st.selectbox(
        "🤖 Chọn thuật toán chẩn đoán:",
        ["YOLO11", "RF-MobileNet"],
        help="YOLO11: Phát hiện đối tượng nhanh | RF-MobileNet: Phân loại chi tiết"
    )

with col_ctrl2:
    uploaded_files = st.file_uploader(
        "📁 Chọn ảnh X-Ray phổi", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True,
        help="Hỗ trợ định dạng: JPG, JPEG, PNG"
    )

# Khởi tạo biến để lưu trữ kết quả
diagnosis_results = []
successful_diagnoses = []

if uploaded_files:
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)

    for uploaded_file in uploaded_files:
        file_path = os.path.join(uploads_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Lớp 2: Ảnh bên trái, Kết quả bên phải
        col_left, col_right = st.columns([1, 1])
        
        # Cột trái - Hiển thị ảnh
        with col_left:
            st.markdown('<h3 class="section-title">📸 Ảnh X-quang đã tải lên</h3>', unsafe_allow_html=True)
            st.image(file_path, caption=f"📁 {uploaded_file.name}", use_container_width=True)
            
            # Thông tin file
            file_size = os.path.getsize(file_path) / 1024  # KB
            st.markdown(f"""
            <div class="info-box">
                <strong>📋 Thông tin file:</strong><br>
                • Tên: {uploaded_file.name}<br>
                • Kích thước: {file_size:.1f} KB<br>
                • Thuật toán: {algorithm_choice}
            </div>
            """, unsafe_allow_html=True)

        # Cột phải - Kết quả chẩn đoán
        with col_right:
            st.markdown('<h3 class="section-title">📊 Kết quả chẩn đoán</h3>', unsafe_allow_html=True)
            
            # Kiểm tra có phải X-ray không
            if not is_xray(file_path):
                st.markdown("""
                <div class="result-error">
                    <h4>❌ Vui lòng chọn ảnh khác</h4>
                    <p>Ảnh này không phải là X-quang phổi hợp lệ.</p>
                </div>
                """, unsafe_allow_html=True)
                continue

            try:
                # Hiển thị trạng thái đang xử lý
                with st.spinner(f'🔄 Đang phân tích bằng {algorithm_choice}...'):
                    # Gọi model theo lựa chọn
                    if algorithm_choice == "YOLO11":
                        pred_label, conclusion, conf = predict_yolo(file_path)
                    else:
                        pred_label, conclusion, conf = predict_rf(file_path)

                confidence_percent = conf * 100

                # Xác định mức độ và màu sắc
                if conclusion in ["PNEUMONIA", "Có bệnh"]:
                    if confidence_percent < 50:
                        severity, recommendation = "Nhẹ", "Theo dõi thêm, nghỉ ngơi và chăm sóc tại nhà"
                        result_class = "result-success"
                        icon = "💚"
                    elif confidence_percent < 80:
                        severity, recommendation = "Trung bình", "Nên đi khám bác sĩ để được kiểm tra chi tiết"
                        result_class = "result-warning"
                        icon = "⚠️"
                    else:
                        severity, recommendation = "Nặng", "Cần nhập viện ngay để điều trị khẩn cấp"
                        result_class = "result-error"
                        icon = "🚨"
                elif conclusion in ["NORMAL", "Không bệnh"]:
                    severity, recommendation = "Không phát hiện bệnh", "Tiếp tục duy trì lối sống lành mạnh"
                    result_class = "result-success"
                    icon = "✅"
                else:
                    severity, recommendation = "Không xác định", "Cần làm thêm xét nghiệm hoặc chụp lại ảnh X-quang"
                    result_class = "result-warning"
                    icon = "❓"

                # Hiển thị kết quả với styling đẹp
                st.markdown(f"""
                <div class="{result_class}">
                    <h4>{icon} Chẩn đoán: {conclusion}</h4>
                    <p><strong>🎯 Mức độ:</strong> {severity}</p>
                    <p><strong>💡 Khuyến nghị:</strong> {recommendation}</p>
                </div>
                """, unsafe_allow_html=True)

                # Thanh độ tin cậy
                st.markdown("**📈 Độ tin cậy:**")
                st.markdown(f"""
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {confidence_percent}%;">
                        {confidence_percent:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Voice + gist
                show_diagnosis_conclusion(conclusion)
                speak(f"Kết luận: {conclusion}. Mức độ: {severity}. Khuyến nghị: {recommendation}")

                # Lưu kết quả để sử dụng sau
                result_data = {
                    'file_path': file_path,
                    'uploaded_file': uploaded_file,
                    'conclusion': conclusion,
                    'confidence_percent': confidence_percent,
                    'severity': severity,
                    'recommendation': recommendation,
                    'algorithm_choice': algorithm_choice
                }
                
                diagnosis_results.append(result_data)
                successful_diagnoses.append(result_data)

                # ========================
                # 🔥 Sinh Grad-CAM cho YOLO11
                # ========================
                if algorithm_choice == "YOLO11":
                    # Chỉ sinh Grad-CAM nếu có bệnh & đúng định dạng ảnh X-Ray
                    if conclusion.upper() not in ["NORMAL", "KHÔNG BỆNH"] and uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:

                        st.markdown('<div class="gradcam-card">', unsafe_allow_html=True)
                        st.markdown('<h3 class="section-title">🔥 Grad-CAM - Vùng nghi ngờ bệnh lý</h3>', unsafe_allow_html=True)
                        
                        try:
                            with st.spinner('🔥 Đang tạo bản đồ nhiệt Grad-CAM...'):
                                overlay, heatmap = generate_gradcam_yolo(model, file_path, input_size=640)

                            col_original, col_overlay, col_heatmap = st.columns([1, 1, 1])

                            with col_original:
                                st.markdown("**📸 Ảnh gốc:**")
                                st.image(file_path, use_container_width=True)

                            with col_overlay:
                                st.markdown("**🔥 Overlay (ảnh gốc + heatmap):**")
                                st.image(overlay, caption="AI highlight vùng nghi ngờ", use_container_width=True)

                            with col_heatmap:
                                st.markdown("**🌡️ Heatmap riêng:**")
                                st.image(heatmap, caption="Bản đồ nhiệt AI chú ý", use_container_width=True)

                            st.markdown("""
                            <div class="info-box">
                                <p><strong>💡 Giải thích Grad-CAM:</strong></p>
                                <p>• Vùng màu đỏ/cam: Khu vực AI tập trung chú ý khi chẩn đoán</p>
                                <p>• Vùng màu xanh: Khu vực ít quan trọng</p>
                                <p>• Grad-CAM giúp bác sĩ hiểu được <em>lý do</em> AI đưa ra kết luận</p>
                            </div>
                            """, unsafe_allow_html=True)

                        except Exception as e:
                            st.markdown(f"""
                            <div class="result-error">
                                <h4>❌ Lỗi Grad-CAM</h4>
                                <p>Không thể tạo bản đồ nhiệt: {str(e)}</p>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown('</div>', unsafe_allow_html=True)

                    else:
                        st.markdown("""
                        <div class="info-box">
                            <p><strong>ℹ️ Thông báo:</strong> Grad-CAM chỉ được tạo khi phát hiện bệnh lý trên ảnh X-ray hợp lệ.</p>
                        </div>
                        """, unsafe_allow_html=True)

                # Lưu vào database
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO lich_su_chan_doan
                        (user_id, username, filename, result, algorithm, confidence, severity, recommendation)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        st.session_state.user['id'], 
                        st.session_state.user['username'],
                        uploaded_file.name, 
                        conclusion, 
                        algorithm_choice, 
                        confidence_percent,
                        severity, 
                        recommendation
                    ))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    add_log(
                        st.session_state.user["id"], 
                        "Chẩn đoán", 
                        f"File: {uploaded_file.name}, KQ: {conclusion}, Độ tin cậy: {confidence_percent:.2f}%, Thuật toán: {algorithm_choice}"
                    )
                except Exception as e:
                    st.error(f"Lỗi lưu database: {str(e)}")

            except Exception as e:
                st.markdown(f"""
                <div class="result-error">
                    <h4>❌ Lỗi xử lý</h4>
                    <p>Không thể phân tích ảnh: {str(e)}</p>
                </div>
                """, unsafe_allow_html=True)
                continue

    # Lớp 3: Thông báo thành công và các nút hành động (chỉ hiện khi có chẩn đoán thành công)
    if successful_diagnoses:
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">✅ Hoàn thành</h3>', unsafe_allow_html=True)
        
        col_action1, col_action2, col_action3 = st.columns([1, 1, 1])
        
        with col_action1:
            if st.button("📝 Xem lịch sử", use_container_width=True):
                st.switch_page("pages/2_📋_Lịch_sử.py")

        
        with col_action2:
            if st.button("🔄 Chẩn đoán mới", use_container_width=True):
                st.rerun()
        
        with col_action3:
            if st.button("📊 Thống kê", use_container_width=True):
                st.switch_page("pages/3_📊_Thống_kê.py")
        
        st.markdown(f"""
        <div class="result-success">
            <h4>🎉 Chẩn đoán hoàn tất!</h4>
            <p>Đã xử lý thành công {len(successful_diagnoses)} ảnh. Lịch sử chẩn đoán đã được lưu vào hệ thống.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Hiển thị hướng dẫn khi chưa upload
    st.markdown("""
    <div class="image-card">
        <h3>📤 Tải lên ảnh X-quang</h3>
        <p>Vui lòng chọn một hoặc nhiều ảnh X-quang phổi để bắt đầu chẩn đoán</p>
        <div style="margin: 1rem 0; color: #666;">
            <p>📋 <strong>Hướng dẫn sử dụng:</strong></p>
            <p>1️⃣ Chọn thuật toán phù hợp</p>
            <p>2️⃣ Tải lên ảnh X-quang chất lượng tốt</p>
            <p>3️⃣ Chờ hệ thống phân tích và xem kết quả</p>
            <p>4️⃣ Xem Grad-CAM (chỉ YOLO11 + có bệnh lý)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)