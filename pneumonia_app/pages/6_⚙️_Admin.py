import streamlit as st
import pandas as pd
from utils.db_utils import get_connection
from io import BytesIO

# ==========================
# 🎨 CSS Styling cho Admin Panel
# ==========================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Admin */
    .admin-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #0f172a 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.3);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .admin-header::before {
        content: '⚙️';
        position: absolute;
        top: 20px;
        right: 30px;
        font-size: 3rem;
        opacity: 0.1;
    }
    
    .admin-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .admin-header .subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        margin-top: 0.8rem;
        font-weight: 400;
    }
    
    /* Tab Styling */
    .stTabs > div > div > div > div {
        background: white !important;
        border-radius: 15px 15px 0 0 !important;
        border: 2px solid #e0f2fe !important;
        border-bottom: none !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 600 !important;
        color: #1e40af !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs > div > div > div > div[aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #1e40af) !important;
        color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stTabs > div > div:first-child {
        border-bottom: 3px solid #e0f2fe !important;
        margin-bottom: 2rem !important;
    }
    
    /* Card Container */
    .admin-card {
        background: white;
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.12);
        border: 2px solid #e0f2fe;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .admin-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #3b82f6, #60a5fa, #93c5fd);
    }
    
    .admin-card h3 {
        color: #1e40af;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        font-size: 1.4rem;
    }
    
    /* Statistics Cards */
    .stat-card {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #93c5fd;
        box-shadow: 0 4px 12px rgba(147, 197, 253, 0.2);
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(147, 197, 253, 0.3);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #1e40af;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #1e40af;
        font-weight: 500;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Filter Section */
    .filter-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    
    .filter-title {
        color: #1e40af;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1e40af) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.7rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Download Button Styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669, #10b981) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.7rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* Update Button */
    .update-btn button {
        background: linear-gradient(135deg, #f59e0b, #d97706) !important;
    }
    
    .update-btn button:hover {
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4) !important;
    }
    
    /* Upload Section */
    .upload-section {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #60a5fa;
        text-align: center;
        margin: 1.5rem 0;
    }
    
    .upload-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #3b82f6;
    }
    
    /* DataFrames */
    .stDataFrame {
        border: 1px solid #e0f2fe !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    /* Alert Styling */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        margin: 1rem 0 !important;
    }
    
    /* Info Messages */
    .info-message {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: #1e40af;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    
    /* Export Section */
    .export-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
    
    .export-title {
        color: #1e40af;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1.2rem;
    }
    
    /* Role Badge */
    .role-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .role-admin { background: linear-gradient(135deg, #dc2626, #ef4444); color: white; }
    .role-doctor { background: linear-gradient(135deg, #059669, #10b981); color: white; }
    .role-user { background: linear-gradient(135deg, #3b82f6, #60a5fa); color: white; }
    
    /* Success/Error Messages */
    .success-message {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        color: #065f46;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        color: #991b1b;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .admin-header h1 {
            font-size: 2rem;
        }
        .admin-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Admin Dashboard", 
    layout="wide",
    page_icon="🛠️",
    initial_sidebar_state="collapsed"
)

# ==========================
# 🎨 Header Section
# ==========================
st.markdown("""
<div class="admin-header">
    <h1>🛠️ Admin Dashboard</h1>
    <div class="subtitle">Hệ thống quản trị toàn diện - AI Healthcare Platform</div>
</div>
""", unsafe_allow_html=True)

# ================== CHECK QUYỀN ==================
if "user" not in st.session_state or not st.session_state.logged_in:
    st.markdown("""
    <div class="error-message">
        <strong>⚠️ Yêu cầu đăng nhập</strong><br>
        Vui lòng đăng nhập bằng tài khoản quản trị viên để truy cập trang này.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if st.session_state.user.get("role") != "admin":
    st.markdown("""
    <div class="error-message">
        <strong>🚫 Không có quyền truy cập</strong><br>
        Bạn không có quyền truy cập vào trang quản trị này.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ==========================
# Welcome Message
# ==========================
st.markdown(f"""
<div class="info-message">
    <strong>👋 Chào mừng quản trị viên: {st.session_state.user.get('username', 'Admin')}</strong><br>
    Bạn đang truy cập với quyền cao nhất trong hệ thống.
</div>
""", unsafe_allow_html=True)

# ================== TAB MENU ==================
tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard & Lịch sử", 
    "👥 Quản lý người dùng", 
    # "🤖 Quản lý AI Model", 
    "📋 Logs & Báo cáo"
])

# ================== TAB 1: DASHBOARD & LỊCH SỬ ==================
with tab1:
    # Stats Overview
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Lấy thống kê tổng quan
        cursor.execute("SELECT COUNT(*) as total_users FROM users")
        total_users = cursor.fetchone()['total_users']
        
        cursor.execute("SELECT COUNT(*) as total_diagnoses FROM lich_su_chan_doan")
        total_diagnoses = cursor.fetchone()['total_diagnoses']
        
        cursor.execute("SELECT COUNT(DISTINCT algorithm) as total_algorithms FROM lich_su_chan_doan")
        total_algorithms = cursor.fetchone()['total_algorithms']
        
        cursor.execute("SELECT COUNT(*) as total_logs FROM activity_logs")
        total_logs = cursor.fetchone()['total_logs']
        
        # Hiển thị stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{total_users}</div>
                <div class="stat-label">👥 Người dùng</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{total_diagnoses}</div>
                <div class="stat-label">🏥 Chẩn đoán</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{total_algorithms}</div>
                <div class="stat-label">🤖 AI Models</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{total_logs}</div>
                <div class="stat-label">📋 Activity Logs</div>
            </div>
            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Lỗi khi lấy thống kê: {e}")
    
    # Lịch sử chẩn đoán
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown('<h3>📊 Lịch sử chẩn đoán toàn hệ thống</h3>', unsafe_allow_html=True)
    
    try:
        cursor.execute("""
            SELECT u.username, l.*, 
                   DATE_FORMAT(l.created_at, '%d/%m/%Y %H:%i') as formatted_date
            FROM lich_su_chan_doan l
            JOIN users u ON l.user_id = u.id
            ORDER BY l.created_at DESC
        """)
        rows = cursor.fetchall()
        cursor.close(); conn.close()

        if rows:
            df = pd.DataFrame(rows)
            
            # Filter Section
            st.markdown("""
            <div class="filter-section">
                <div class="filter-title">🔍 Bộ lọc dữ liệu</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            user_filter = col1.selectbox("👤 Người dùng", ["Tất cả"] + sorted(df["username"].unique()))
            algo_filter = col2.selectbox("🤖 Thuật toán", ["Tất cả"] + sorted(df["algorithm"].unique()))
            severity_filter = col3.selectbox("⚕️ Mức độ", ["Tất cả"] + sorted(df["severity"].unique()) if "severity" in df.columns else ["Tất cả"])

            # Apply filters
            filtered_df = df.copy()
            if user_filter != "Tất cả":
                filtered_df = filtered_df[filtered_df["username"] == user_filter]
            if algo_filter != "Tất cả":
                filtered_df = filtered_df[filtered_df["algorithm"] == algo_filter]
            if severity_filter != "Tất cả" and "severity" in df.columns:
                filtered_df = filtered_df[filtered_df["severity"] == severity_filter]

            # Display data
            st.dataframe(
                filtered_df.drop('created_at', axis=1) if 'created_at' in filtered_df.columns else filtered_df,
                use_container_width=True, 
                height=500
            )
        else:
            st.markdown('<div class="info-message">📊 Chưa có dữ liệu chẩn đoán nào trong hệ thống.</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="error-message">❌ Lỗi khi tải dữ liệu: {e}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================== TAB 2: QUẢN LÝ USER ==================
with tab2:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown('<h3>👥 Quản lý người dùng</h3>', unsafe_allow_html=True)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, username, email, role, 
                   DATE_FORMAT(created_at, '%d/%m/%Y %H:%i') as join_date
            FROM users 
            ORDER BY created_at DESC
        """)
        users = cursor.fetchall()
        cursor.close(); conn.close()

        if users:
            # Tạo dataframe với role badges
            df_users = pd.DataFrame(users)
            
            # Display users table
            st.dataframe(df_users, use_container_width=True, height=400)
            
            # User management section
            st.markdown("""
            <div class="filter-section">
                <div class="filter-title">⚙️ Phân quyền người dùng</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                selected_user = st.selectbox(
                    "👤 Chọn người dùng:", 
                    options=[(user['id'], f"{user['username']} ({user['email']})") for user in users],
                    format_func=lambda x: x[1]
                )
                user_id = selected_user[0]
            
            with col2:
                new_role = st.selectbox("🎭 Chọn quyền mới:", ["user", "doctor", "admin"])
            
            with col3:
                st.markdown('<div class="update-btn">', unsafe_allow_html=True)
                if st.button("🔄 Cập nhật quyền", key="update_role"):
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET role=%s WHERE id=%s", (new_role, user_id))
                        conn.commit()
                        cursor.close(); conn.close()
                        st.markdown('<div class="success-message">✅ Cập nhật quyền thành công!</div>', unsafe_allow_html=True)
                        st.rerun()
                    except Exception as e:
                        st.markdown(f'<div class="error-message">❌ Lỗi khi cập nhật: {e}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-message">👥 Chưa có người dùng nào trong hệ thống.</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="error-message">❌ Lỗi khi tải dữ liệu người dùng: {e}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# # ================== TAB 3: QUẢN LÝ MÔ HÌNH ==================
# with tab3:
#     st.markdown('<div class="admin-card">', unsafe_allow_html=True)
#     st.markdown('<h3>🤖 Quản lý AI Models & Algorithms</h3>', unsafe_allow_html=True)
    
#     st.markdown("""
#     <div class="upload-section">
#         <div class="upload-icon">📤</div>
#         <h4 style="color: #1e40af; margin-bottom: 1rem;">Upload mô hình AI mới</h4>
#         <p style="color: #64748b;">Hỗ trợ các định dạng: .pt (PyTorch), .keras (TensorFlow), .joblib (Scikit-learn)</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     uploaded_model = st.file_uploader(
#         "🔍 Chọn file mô hình", 
#         type=["pt", "keras", "joblib", "pkl", "h5"],
#         accept_multiple_files=True,
#         help="Có thể chọn nhiều file cùng lúc"
#     )
    
#     if uploaded_model:
#         st.markdown('<div class="success-message">', unsafe_allow_html=True)
#         if isinstance(uploaded_model, list):
#             for model_file in uploaded_model:
#                 try:
#                     with open(f"models/{model_file.name}", "wb") as f:
#                         f.write(model_file.getbuffer())
#                     st.write(f"✅ Đã upload thành công: **{model_file.name}** ({model_file.size} bytes)")
#                 except Exception as e:
#                     st.write(f"❌ Lỗi upload {model_file.name}: {e}")
#         else:
#             try:
#                 with open(f"models/{uploaded_model.name}", "wb") as f:
#                     f.write(uploaded_model.getbuffer())
#                 st.write(f"✅ Đã upload thành công: **{uploaded_model.name}** ({uploaded_model.size} bytes)")
#             except Exception as e:
#                 st.write(f"❌ Lỗi upload: {e}")
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     # Model Status
#     st.markdown("""
#     <div class="info-message">
#         <strong>📋 Trạng thái mô hình hiện tại:</strong><br>
#         • YOLO Detection: ✅ Hoạt động<br>
#         • Gemini AI Consultation: ✅ Hoạt động<br>
#         • Custom Models: 📁 Kiểm tra thư mục /models
#     </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown('</div>', unsafe_allow_html=True)

# ================== TAB 4: LOG & EXPORT ==================
with tab3:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown('<h3>📋 Activity Logs & Báo cáo hệ thống</h3>', unsafe_allow_html=True)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT *, 
                   DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') as formatted_date
            FROM activity_logs 
            ORDER BY created_at DESC 
            LIMIT 500
        """)
        logs = cursor.fetchall()
        cursor.close(); conn.close()

        if logs:
            df_logs = pd.DataFrame(logs)
            
            # Log filters
            st.markdown("""
            <div class="filter-section">
                <div class="filter-title">🔍 Bộ lọc logs</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            if 'action' in df_logs.columns:
                action_filter = col1.selectbox("📝 Loại hoạt động:", ["Tất cả"] + sorted(df_logs["action"].unique()))
                if action_filter != "Tất cả":
                    df_logs = df_logs[df_logs["action"] == action_filter]
            
            if 'user_id' in df_logs.columns:
                user_filter = col2.selectbox("👤 Người dùng (ID):", ["Tất cả"] + sorted(df_logs["user_id"].unique().astype(str)))
                if user_filter != "Tất cả":
                    df_logs = df_logs[df_logs["user_id"].astype(str) == user_filter]
            
            # Display logs
            st.dataframe(
                df_logs.drop('created_at', axis=1) if 'created_at' in df_logs.columns else df_logs,
                use_container_width=True, 
                height=400
            )

            # Export Section
            st.markdown("""
            <div class="export-section">
                <div class="export-title">📤 Xuất dữ liệu báo cáo</div>
                <p style="color: #64748b; margin-bottom: 1.5rem;">Chọn định dạng để tải xuống dữ liệu logs</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)

            # CSV Export
            with col1:
                csv = df_logs.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📊 Xuất CSV",
                    csv,
                    f"activity_logs_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                    "text/csv",
                    help="Định dạng CSV cho Excel, Google Sheets"
                )

            # Excel Export
            with col2:
                output = BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df_logs.to_excel(writer, index=False, sheet_name="Activity_Logs")
                    # Có thể thêm sheet khác nếu cần
                    # df_other.to_excel(writer, index=False, sheet_name="Other_Data")
                
                st.download_button(
                    "📈 Xuất Excel",
                    output.getvalue(),
                    f"activity_logs_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help="Định dạng Excel với nhiều sheet"
                )

            # JSON Export
            with col3:
                json_data = df_logs.to_json(orient='records', indent=2).encode('utf-8')
                st.download_button(
                    "📋 Xuất JSON",
                    json_data,
                    f"activity_logs_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.json",
                    "application/json",
                    help="Định dạng JSON cho API, databases"
                )

            # PDF Export
            with col4:
                try:
                    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                    from reportlab.lib import colors
                    from reportlab.lib.pagesizes import A4, landscape
                    from reportlab.lib.styles import getSampleStyleSheet
                    
                    pdf_output = BytesIO()
                    doc = SimpleDocTemplate(pdf_output, pagesize=landscape(A4))
                    styles = getSampleStyleSheet()
                    
                    # Title
                    title = Paragraph("📋 Activity Logs Report", styles['Title'])
                    subtitle = Paragraph(f"Generated: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal'])
                    
                    # Table data (limit columns to fit)
                    display_cols = ['id', 'action', 'user_id', 'formatted_date']
                    available_cols = [col for col in display_cols if col in df_logs.columns]
                    
                    table_data = [available_cols] + df_logs[available_cols].head(50).values.tolist()
                    
                    table = Table(table_data)
                    table.setStyle(TableStyle([
                        ("BACKGROUND", (0,0), (-1,0), colors.navy),
                        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
                        ("ALIGN", (0,0), (-1,-1), "CENTER"),
                        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                        ("FONTSIZE", (0,0), (-1,0), 10),
                        ("BOTTOMPADDING", (0,0), (-1,0), 12),
                        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
                        ("GRID", (0,0), (-1,-1), 1, colors.black),
                        ("FONTSIZE", (0,1), (-1,-1), 8),
                        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.lightgrey])
                    ]))
                    
                    # Build PDF
                    story = [title, Spacer(1, 12), subtitle, Spacer(1, 20), table]
                    doc.build(story)
                    
                    st.download_button(
                        "📄 Xuất PDF",
                        pdf_output.getvalue(),
                        f"activity_logs_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.pdf",
                        "application/pdf",
                        help="Định dạng PDF cho báo cáo in ấn"
                    )
                except ImportError:
                    st.markdown("""
                    <div style="background: #fef3c7; padding: 0.8rem; border-radius: 8px; border: 1px solid #f59e0b; color: #92400e;">
                        ⚠️ <strong>Chưa cài đặt ReportLab</strong><br>
                        Chạy: <code>pip install reportlab</code> để kích hoạt xuất PDF
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Lỗi tạo PDF: {e}")

            # Additional Export Options
            st.markdown("---")
            
            # Bulk Export Section
            with st.expander("🎯 Xuất dữ liệu nâng cao", expanded=False):
                st.markdown("""
                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <h5 style="color: #1e40af; margin-bottom: 0.5rem;">📊 Tùy chọn xuất dữ liệu</h5>
                </div>
                """, unsafe_allow_html=True)
                
                export_col1, export_col2 = st.columns(2)
                
                with export_col1:
                    # Date range filter
                    st.write("📅 **Lọc theo thời gian:**")
                    if 'created_at' in df_logs.columns:
                        date_from = st.date_input("Từ ngày:", value=pd.Timestamp.now().date() - pd.Timedelta(days=30))
                        date_to = st.date_input("Đến ngày:", value=pd.Timestamp.now().date())
                
                with export_col2:
                    # Column selection
                    st.write("📋 **Chọn cột xuất:**")
                    selected_columns = st.multiselect(
                        "Columns:",
                        options=df_logs.columns.tolist(),
                        default=df_logs.columns.tolist()[:5]  # First 5 columns by default
                    )
                
                # Custom export button
                if st.button("🚀 Xuất dữ liệu tùy chỉnh", key="custom_export"):
                    if selected_columns:
                        filtered_data = df_logs[selected_columns]
                        
                        # Apply date filter if available
                        if 'created_at' in df_logs.columns:
                            filtered_data = filtered_data[
                                (pd.to_datetime(df_logs['created_at']).dt.date >= date_from) &
                                (pd.to_datetime(df_logs['created_at']).dt.date <= date_to)
                            ]
                        
                        custom_csv = filtered_data.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "⬇️ Tải CSV tùy chỉnh",
                            custom_csv,
                            f"custom_logs_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                            "text/csv"
                        )
                    else:
                        st.warning("⚠️ Vui lòng chọn ít nhất một cột để xuất!")

        else:
            st.markdown("""
            <div class="info-message">
                <strong>📋 Không có logs</strong><br>
                Chưa có hoạt động nào được ghi lại trong hệ thống.
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            <strong>❌ Lỗi khi tải logs</strong><br>
            Chi tiết: {e}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================
# 🔹 Footer với thông tin hệ thống
# ==========================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; background: white; border-radius: 15px; margin-top: 2rem; box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);">
    <h4 style="color: #1e40af; margin-bottom: 1rem;">🛠️ Admin Control Panel</h4>
    <p style="color: #64748b; margin-bottom: 0.5rem;">
        <strong>Hệ thống quản trị AI Healthcare Platform</strong>
    </p>
    <p style="color: #64748b; font-size: 0.9rem;">
        Phiên bản: 2.0.1 | Cập nhật: {pd.Timestamp.now().strftime('%d/%m/%Y')} | 
        Người dùng: <strong>{st.session_state.user.get('username', 'Admin')}</strong>
    </p>
    <div style="margin-top: 1rem; color: #64748b; font-size: 0.8rem;">
        💡 <em>Với quyền Admin, bạn có toàn quyền kiểm soát và giám sát hệ thống</em>
    </div>
</div>
""", unsafe_allow_html=True)