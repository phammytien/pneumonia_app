# pages/4_Trang_ca_nhan.py
import streamlit as st
import os
from utils.db_utils import get_connection
from utils.preprocess import save_uploaded_file

st.set_page_config(page_title="Trang cá nhân", layout="wide")

# Custom CSS cho giao diện đẹp
st.markdown("""
<style>
    /* Màu nền chính */
    .main {
        background-color: #f8fbff;
    }
    
    /* Header styling */
    .profile-header {
        background: linear-gradient(135deg, #4a90e2 0%, #2c5aa0 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(74, 144, 226, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .profile-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="white" opacity="0.1"><path d="M0,20 C200,80 400,0 600,40 C800,80 900,20 1000,40 V100 H0 Z"/></svg>');
        pointer-events: none;
    }
    
    .profile-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    
    .profile-header p {
        color: #e8f4f8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    /* Main profile container */
    .profile-container {
        background: white;
        border-radius: 20px;
        padding: 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        border: 1px solid #e3f2fd;
    }
    
    /* Profile sidebar */
    .profile-sidebar {
        background: linear-gradient(180deg, #f8faff 0%, #e3f2fd 100%);
        padding: 2rem;
        border-right: 1px solid #e3f2fd;
        text-align: center;
        min-height: 600px;
    }
    
    /* Avatar container */
    .avatar-container {
        position: relative;
        display: inline-block;
        margin-bottom: 1.5rem;
    }
    
    .avatar-frame {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        border: 4px solid #4a90e2;
        padding: 4px;
        background: white;
        box-shadow: 0 8px 25px rgba(74, 144, 226, 0.3);
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
    }
    
    .avatar-placeholder {
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #4a90e2 0%, #2c5aa0 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        color: white;
    }
    
    /* User info in sidebar */
    .user-title {
        color: #2c5aa0;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .user-role {
        color: #666;
        font-size: 1rem;
        margin-bottom: 1.5rem;
        padding: 0.3rem 1rem;
        background: #e8f4f8;
        border-radius: 20px;
        display: inline-block;
    }
    
    /* Profile content */
    .profile-content {
        padding: 2rem;
    }
    
    /* Section styling */
    .section-title {
        color: #2c5aa0;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e3f2fd;
        display: flex;
        align-items: center;
    }
    
    /* Info cards */
    .info-card {
        background: linear-gradient(135deg, #f8faff 0%, #ffffff 100%);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border: 1px solid #e3f2fd;
        border-left: 4px solid #4a90e2;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 20px rgba(74, 144, 226, 0.15);
    }
    
    .info-label {
        color: #666;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .info-value {
        color: #2c5aa0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* Edit form styling */
    .edit-form {
        background: linear-gradient(135deg, #f0f9ff 0%, #f8faff 100%);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 1rem;
        border: 1px solid #b3e5fc;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4a90e2 0%, #2c5aa0 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.4);
    }
    
    /* Form inputs */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e3f2fd;
        padding: 0.7rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4a90e2;
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: white;
        border-radius: 10px;
        border: 2px dashed #4a90e2;
        padding: 1.5rem;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    .status-active {
        background: #e8f5e8;
        color: #2e7d32;
        border: 1px solid #c8e6c9;
    }
    
    /* Action buttons */
    .action-buttons {
        background: linear-gradient(135deg, #e8f4f8 0%, #f0f9ff 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 2rem;
        border: 1px solid #b3e5fc;
    }
    
    /* Quick stats */
    .quick-stats {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border: 1px solid #c8e6c9;
    }
    
    .stat-item {
        text-align: center;
        padding: 0.5rem;
    }
    
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2e7d32;
        margin: 0;
    }
    
    .stat-label {
        color: #4caf50;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .profile-sidebar {
            border-right: none;
            border-bottom: 1px solid #e3f2fd;
            min-height: auto;
        }
        
        .avatar-frame {
            width: 120px;
            height: 120px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header chính
st.markdown("""
<div class="profile-header">
    <h1>👤 Trang Cá Nhân</h1>
    <p>Quản lý thông tin cá nhân và cài đặt tài khoản</p>
</div>
""", unsafe_allow_html=True)

# Kiểm tra đăng nhập
if "user" not in st.session_state or not st.session_state.logged_in:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fff3e0 0%, #fff8f0 100%); 
                border-radius: 10px; padding: 2rem; text-align: center; 
                border: 1px solid #ffcc02; color: #e65100; margin: 2rem 0;">
        <h3>⚠️ Cần đăng nhập</h3>
        <p>Vui lòng đăng nhập để xem trang cá nhân.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

uploads_dir = "uploads"
os.makedirs(uploads_dir, exist_ok=True)

user = st.session_state.user

# Flag edit profile
if "edit_profile" not in st.session_state:
    st.session_state.edit_profile = False

# Layout chính - 2 cột
st.markdown('<div class="profile-container">', unsafe_allow_html=True)

col_sidebar, col_content = st.columns([1, 2])

# Sidebar - Avatar và thông tin cơ bản
with col_sidebar:
    # st.markdown('<div class="profile-sidebar">', unsafe_allow_html=True)
    
    # Avatar
    st.markdown('<div class="avatar-container">', unsafe_allow_html=True)
    avatar_file = user.get("avatar")
    if avatar_file:
        avatar_path = os.path.join(uploads_dir, avatar_file)
        if os.path.exists(avatar_path):
            # st.markdown('<div class="avatar-frame">', unsafe_allow_html=True)
            st.image(avatar_path, width=142)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="avatar-frame">
                <div class="avatar-placeholder">👤</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="avatar-frame">
            <div class="avatar-placeholder">👤</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Thông tin cơ bản
    full_name = user.get('full_name', 'Chưa cập nhật')
    username = user.get('username', 'Unknown')
    
    st.markdown(f"""
    <div class="user-title">{full_name}</div>
    <div class="user-role">@{username}</div>
    <div class="status-badge status-active">🟢 Đang hoạt động</div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    try:
        # Lấy thống kê nhanh từ database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM lich_su_chan_doan WHERE user_id=%s", (user['id'],))
        total_diagnoses = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    except:
        total_diagnoses = 0
    
    st.markdown(f"""
    <div class="quick-stats">
        <h4 style="color: #2e7d32; text-align: center; margin-bottom: 1rem;">📊 Thống kê</h4>
        <div class="stat-item">
            <div class="stat-number">{total_diagnoses}</div>
            <div class="stat-label">Lần chẩn đoán</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Content - Chi tiết và form chỉnh sửa
with col_content:
    st.markdown('<div class="profile-content">', unsafe_allow_html=True)
    
    # Thanh điều khiển
    col_title, col_actions = st.columns([2, 1])
    
    with col_title:
        st.markdown('<h3 class="section-title">📋 Thông tin chi tiết</h3>', unsafe_allow_html=True)
    
    with col_actions:
        if st.session_state.edit_profile:
            if st.button("❌ Hủy chỉnh sửa", use_container_width=True):
                st.session_state.edit_profile = False
                st.rerun()
        else:
            if st.button("✏️ Chỉnh sửa", use_container_width=True):
                st.session_state.edit_profile = True
                st.rerun()
    
    # Form chỉnh sửa hoặc hiển thị thông tin
    if st.session_state.edit_profile:
        st.markdown('<div class="edit-form">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #2c5aa0; margin-bottom: 1.5rem;">✏️ Chỉnh sửa thông tin</h4>', unsafe_allow_html=True)
        
        with st.form(key="edit_profile_form"):
            col_form1, col_form2 = st.columns([1, 1])
            
            with col_form1:
                full_name = st.text_input("👤 Họ và tên", user.get("full_name",""), placeholder="Nhập họ và tên")
                email = st.text_input("📧 Email", user.get("email",""), placeholder="email@example.com")
                
            with col_form2:
                phone = st.text_input("📱 Số điện thoại", user.get("phone",""), placeholder="+84 xxx xxx xxx")
                address = st.text_input("🏠 Địa chỉ", user.get("address",""), placeholder="Nhập địa chỉ")
            
            uploaded_avatar = st.file_uploader(
                "📸 Cập nhật ảnh đại diện (không bắt buộc)", 
                type=["jpg","png","jpeg"],
                help="Chọn file ảnh có định dạng JPG, PNG hoặc JPEG"
            )
            
            col_submit, col_cancel = st.columns([1, 1])
            
            with col_submit:
                submit_button = st.form_submit_button("💾 Lưu thông tin", use_container_width=True)
            
            with col_cancel:
                if st.form_submit_button("🔄 Reset", use_container_width=True):
                    st.rerun()

            if submit_button:
                try:
                    avatar_filename = user.get("avatar")
                    if uploaded_avatar:
                        avatar_filename = uploaded_avatar.name
                        save_path = os.path.join(uploads_dir, avatar_filename)
                        with open(save_path, "wb") as f:
                            f.write(uploaded_avatar.getbuffer())

                    # Cập nhật DB
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users
                        SET full_name=%s, email=%s, phone=%s, address=%s, avatar=%s
                        WHERE id=%s
                    """, (full_name, email, phone, address, avatar_filename, user["id"]))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    # Cập nhật session
                    st.session_state.user.update({
                        "full_name": full_name,
                        "email": email,
                        "phone": phone,
                        "address": address,
                        "avatar": avatar_filename
                    })
                    
                    st.success("✅ Cập nhật thông tin thành công!")
                    st.session_state.edit_profile = False
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Lỗi khi cập nhật: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Hiển thị thông tin chi tiết
        info_data = [
            ("👤", "Họ và tên", user.get('full_name', 'Chưa cập nhật')),
            ("📧", "Email", user.get('email', 'Chưa cập nhật')),
            ("📱", "Số điện thoại", user.get('phone', 'Chưa cập nhật')),
            ("🏠", "Địa chỉ", user.get('address', 'Chưa cập nhật')),
            ("🔐", "Tên đăng nhập", user.get('username', 'Unknown'))
        ]
        
        for icon, label, value in info_data:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-label">{icon} {label}</div>
                <div class="info-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Thời gian tạo tài khoản
        created_at = user.get("created_at")
        if created_at:
            formatted_date = created_at.strftime('%d/%m/%Y lúc %H:%M:%S')
        else:
            formatted_date = "Chưa có thông tin"
            
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">📅 Ngày tham gia</div>
            <div class="info-value">{formatted_date}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown(f"""
    <div class="action-buttons">
        <h4 style="color: #2c5aa0; text-align: center; margin-bottom: 1rem;">🚀 Hành động nhanh</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col_action1, col_action2, col_action3 = st.columns([1, 1, 1])
    
    with col_action1:
        if st.button("🩻 Chẩn đoán mới", use_container_width=True):
            st.switch_page("pages/1_🔍_Chẩn_đoán.py")
    
    with col_action2:
        if st.button("📊 Xem thống kê", use_container_width=True):
            st.switch_page("pages/3_📊_Thống_kê.py")
    
    with col_action3:
        if st.button("🏠 Về trang chủ", use_container_width=True):
            st.switch_page("app.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)