import streamlit as st
from utils.auth import login, register

st.set_page_config(
    page_title="Hệ thống Chẩn đoán Bệnh Phổi", 
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS với màu xanh nhạt/đậm và nền trắng
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-blue: #2E86AB;
        --light-blue: #A5C3D9; 
        --lighter-blue: #E8F4F8;
        --dark-blue: #1B5E7F;
        --white: #FFFFFF;
        --light-gray: #F8FAFB;
        --text-dark: #2C3E50;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--primary-blue) 0%, var(--dark-blue) 100%);
    }
    
    .css-17eq0hr {
        background: transparent;
        color: white;
    }
    
    .css-pkbazv {
        color: white !important;
        font-weight: 600;
    }
    
    /* Main content area */
    .main .block-container {
        background: var(--white);
        padding: 1rem 2rem;
        max-width: 1200px;
    }
    
    /* Header styling - COMPACT VERSION */
    .main-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--light-blue) 100%);
        padding: 1.5rem 2rem;  /* Giảm từ 3rem xuống 1.5rem */
        border-radius: 15px;   /* Giảm từ 20px xuống 15px */
        margin-bottom: 1.5rem; /* Giảm từ 2rem xuống 1.5rem */
        text-align: center;
        color: white;
        box-shadow: 0 4px 20px rgba(46, 134, 171, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); } /* Giảm animation */
    }
    
    .main-header h1 {
        font-size: 1.8rem;     /* Giảm từ 2.5rem xuống 1.8rem */
        margin-bottom: 0.3rem; /* Giảm từ 0.5rem xuống 0.3rem */
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: relative;
        z-index: 2;
    }
    
    .main-header p {
        font-size: 1rem;       /* Giảm từ 1.3rem xuống 1rem */
        opacity: 0.95;
        position: relative;
        z-index: 2;
        margin: 0;
    }
    
    /* Feature cards */
    .feature-card {
        background: var(--white);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(46, 134, 171, 0.15);
        margin: 1rem 0;
        border: 1px solid var(--lighter-blue);
        border-left: 6px solid var(--primary-blue);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-blue), var(--light-blue));
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(46, 134, 171, 0.25);
    }
    
    .feature-card h4 {
        color: var(--primary-blue);
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .feature-card p {
        color: var(--text-dark);
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    
    /* Stats cards */
    .stats-card {
        background: linear-gradient(135deg, var(--lighter-blue) 0%, var(--light-blue) 100%);
        padding: 2rem 1rem;
        border-radius: 16px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(46, 134, 171, 0.2);
        transition: transform 0.3s ease;
        border: 1px solid rgba(46, 134, 171, 0.1);
    }
    
    .stats-card:hover {
        transform: scale(1.02);
    }
    
    .stats-card h3 {
        color: var(--dark-blue);
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stats-card p {
        color: var(--primary-blue);
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* Login container - COMPACT VERSION */
    .login-container {
        background: var(--white);
        padding: 1.5rem;        /* Giảm từ 2rem xuống 1.5rem */
        border-radius: 15px;    /* Giảm từ 20px xuống 15px */
        box-shadow: 0 6px 25px rgba(46, 134, 171, 0.15);
        border: 1px solid var(--lighter-blue);
        max-width: 380px;       /* Giảm từ 450px xuống 380px */
        margin: 1rem auto;      /* Giảm từ 2rem xuống 1rem */
    }
    
    .login-container h4 {
        color: var(--primary-blue);
        text-align: center;
        margin-bottom: 1.2rem;  /* Giảm từ 1.5rem xuống 1.2rem */
        font-size: 1.2rem;      /* Giảm từ 1.4rem xuống 1.2rem */
        font-weight: 600;
    }
    
    /* Compact form styling */
    .compact-form {
        margin: 0.8rem 0;       /* Giảm khoảng cách giữa các field */
    }
    
    .compact-form .stTextInput > div > div > input {
        padding: 0.6rem 1rem;   /* Giảm padding */
        font-size: 0.95rem;     /* Giảm font size */
        border-radius: 8px;     /* Giảm border radius */
    }
    
    .compact-form .stTextInput > label {
        font-size: 0.9rem;      /* Giảm font size của label */
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    
    /* Buttons - COMPACT */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--dark-blue) 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem; /* Giảm từ 0.8rem 1.5rem */
        border-radius: 10px;    /* Giảm từ 12px */
        font-weight: 600;
        font-size: 0.9rem;      /* Giảm từ 1rem */
        transition: all 0.3s ease;
        box-shadow: 0 3px 12px rgba(46, 134, 171, 0.3);
        margin: 0.3rem 0;       /* Thêm margin để tạo khoảng cách */
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 18px rgba(46, 134, 171, 0.4);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border: 2px solid var(--light-blue);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 3px rgba(46, 134, 171, 0.1);
    }
    
    /* Sidebar welcome message */
    .sidebar-welcome {
        background: rgba(255, 255, 255, 0.15);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: black;
        text-align: center;
    }
    
    /* Auth box */
    .auth-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: black;
        text-align: center;
    }
    
    /* Info box */
    .stInfo {
        background: var(--lighter-blue);
        border: 1px solid var(--light-blue);
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: #D4F4DD;
        border: 1px solid #4CAF50;
        color: #2E7D32;
        border-radius: 10px;
    }
    
    .stError {
        background: #FFEBEE;
        border: 1px solid #F44336;
        color: #C62828;
        border-radius: 10px;
    }
    
    .stWarning {
        background: #FFF3E0;
        border: 1px solid #FF9800;
        color: #E65100;
        border-radius: 10px;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--light-blue), transparent);
        margin: 2rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: var(--primary-blue);
        padding: 2rem;
        background: var(--light-gray);
        border-radius: 15px;
        margin-top: 2rem;
    }
    
    /* Page navigation */
    .nav-item {
        background: rgba(255, 255, 255, 0.1);
        margin: 0.2rem 0;
        border-radius: 8px;
        transition: background 0.3s ease;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Need login message */
    .need-login {
        background: var(--lighter-blue);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        border: 2px solid var(--light-blue);
    }
    
    /* Button group compact styling */
    .button-group-compact {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.8rem;
    }
    
    .button-group-compact .stButton {
        flex: 1;
    }
    
    .button-group-compact .stButton > button {
        margin: 0;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if 'show_auth' not in st.session_state:
    st.session_state.show_auth = False

if 'auth_page' not in st.session_state:  
    st.session_state.auth_page = "Đăng nhập"

# Sidebar - luôn hiển thị menu
st.sidebar.title("🫁 Menu Chính")

# Kiểm tra trạng thái đăng nhập và hiển thị thông tin user
if st.session_state.logged_in:
    st.sidebar.markdown(f"""
    <div class="sidebar-welcome">
        <h4>👋 Xin chào!</h4>
        <p><strong>{st.session_state.user['username']}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.show_auth = False
        st.rerun()
else:
    # Hiển thị form đăng nhập/đăng ký trong sidebar
    st.sidebar.markdown("""
    <div class="auth-box">
        <h4>🔐 Xác thực</h4>
        <p>Đăng nhập để sử dụng đầy đủ tính năng</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚀 Đăng nhập", use_container_width=True):
        st.session_state.show_auth = True
        st.session_state.auth_page = "Đăng nhập"
    
    if st.sidebar.button("📝 Đăng ký", use_container_width=True):
        st.session_state.show_auth = True
        st.session_state.auth_page = "Đăng ký"

# Hiển thị nội dung trang chủ
# Hiển thị form đăng nhập/đăng ký nếu được yêu cầu
if st.session_state.show_auth and not st.session_state.logged_in:
    # COMPACT HEADER
    st.markdown("""
    <div class="main-header">
        <h1>🫁 Hệ thống Chẩn đoán Bệnh Phổi</h1>
        <p>Công nghệ AI tiên tiến - Chẩn đoán chính xác, nhanh chóng</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Container trung tâm cho form auth - COMPACT
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.session_state.auth_page == "Đăng nhập":
            st.markdown("""
            <div class="login-container">
                <h4>🔐 Đăng nhập</h4>
            </div>
            """, unsafe_allow_html=True)

            # Compact form container
            st.markdown('<div class="compact-form">', unsafe_allow_html=True)
            
            username = st.text_input("👤 Tên đăng nhập", placeholder="Username", key="login_user")
            password = st.text_input("🔒 Mật khẩu", type="password", placeholder="Password", key="login_pass")
            
            st.markdown('</div>', unsafe_allow_html=True)

            # Compact button group
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("🚀 Đăng nhập", use_container_width=True):
                    if username and password:
                        user = login(username, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user = user
                            st.session_state.show_auth = False
                            st.success("✅ Đăng nhập thành công!")
                            st.rerun()
                        else:
                            st.error("❌ Sai thông tin")
                    else:
                        st.warning("⚠️ Nhập đầy đủ thông tin")

            with col_btn2:
                if st.button("📝 Đăng ký", use_container_width=True):
                    st.session_state.auth_page = "Đăng ký"
                    st.rerun()
            
            with col_btn3:
                if st.button("❌ Hủy", use_container_width=True):
                    st.session_state.show_auth = False
                    st.rerun()

        elif st.session_state.auth_page == "Đăng ký":
            st.markdown("""
            <div class="login-container">
                <h4>📝 Tạo tài khoản</h4>
            </div>
            """, unsafe_allow_html=True)

            # Compact form container
            st.markdown('<div class="compact-form">', unsafe_allow_html=True)
            
            username = st.text_input("👤 Tên đăng nhập", placeholder="Username", key="reg_user")
            password = st.text_input("🔒 Mật khẩu", type="password", placeholder="Password", key="reg_pass")
            confirm_password = st.text_input("🔒 Xác nhận mật khẩu", type="password", placeholder="Confirm Password", key="reg_pass2")
            
            st.markdown('</div>', unsafe_allow_html=True)

            # Compact button group
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("✅ Tạo TK", use_container_width=True):
                    if username and password and confirm_password:
                        if password == confirm_password:
                            try:
                                if register(username, password):
                                    st.success("🎉 Đăng ký thành công!")
                                    st.balloons()
                                    st.session_state.auth_page = "Đăng nhập"
                                    st.rerun()
                            except Exception as e:
                                st.error(f"❌ Lỗi: {e}")
                        else:
                            st.error("❌ Mật khẩu không khớp")
                    else:
                        st.warning("⚠️ Nhập đầy đủ thông tin")

            with col_btn2:
                if st.button("🔄 Đăng nhập", use_container_width=True):
                    st.session_state.auth_page = "Đăng nhập"
                    st.rerun()
                    
            with col_btn3:
                if st.button("❌ Hủy", use_container_width=True):
                    st.session_state.show_auth = False
                    st.rerun()
else:
    # Trang chủ chính - luôn hiển thị cho tất cả người dùng
    st.markdown("""
    <div class="main-header">
        <h1>🫁 Hệ thống Chẩn đoán Bệnh Phổi AI</h1>
        <p>Chào mừng bạn đến với hệ thống chẩn đoán thông minh</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Thống kê nhanh
    st.markdown("### 📈 Thống kê tổng quan")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stats-card">
            <h3>1,250+</h3>
            <p>Ca chẩn đoán thành công</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <h3>95.8%</h3>
            <p>Độ chính xác trung bình</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card">
            <h3>2.3s</h3>
            <p>Thời gian xử lý trung bình</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stats-card">
            <h3>24/7</h3>
            <p>Hỗ trợ liên tục</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Chức năng chính
    st.markdown("### 🎯 Chức năng chính của hệ thống")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🔍 Chẩn đoán từ X-quang</h4>
            <p>• Tải lên ảnh X-quang ngực chất lượng cao</p>
            <p>• Phân tích tự động bằng AI tiên tiến</p>
            <p>• Nhận kết quả chi tiết với tỷ lệ tin cậy</p>
            <p>• Xuất báo cáo PDF chuyên nghiệp</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Lịch sử & Thống kê</h4>
            <p>• Xem lại các ca đã chẩn đoán trước đó</p>
            <p>• So sánh kết quả theo thời gian</p>
            <p>• Phân tích xu hướng bệnh lý</p>
            <p>• Báo cáo thống kê tổng hợp</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🎓 Trung tâm kiến thức</h4>
            <p>• Thư viện bệnh phổi thường gặp</p>
            <p>• Hướng dẫn đọc X-quang cơ bản</p>
            <p>• Cập nhật nghiên cứu y khoa mới nhất</p>
            <p>• Video hướng dẫn chi tiết</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🤖 AI Tư vấn thông minh</h4>
            <p>• Tư vấn sơ bộ dựa trên triệu chứng</p>
            <p>• Gợi ý các xét nghiệm cần thiết</p>
            <p>• Hỗ trợ 24/7 với chatbot AI</p>
            <p>• Kết nối với bác sĩ chuyên khoa</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Hướng dẫn sử dụng
    st.markdown("### 🚀 Hướng dẫn sử dụng nhanh")
    
    st.info("""
    **📋 Các bước thực hiện:**
    
    1. **🔍 Chẩn đoán:** Chọn "Chẩn đoán" trong menu → Đăng nhập nếu chưa → Tải ảnh X-quang → Nhận kết quả
    2. **📊 Theo dõi:** Vào "Lịch sử" để xem các ca đã chẩn đoán và thống kê chi tiết  
    3. **🤖 Tư vấn:** Sử dụng "AI Tư vấn" để được hỗ trợ và tư vấn sơ bộ
    4. **📚 Học hỏi:** Tham khảo "Trung tâm kiến thức" để nâng cao kiến thức y khoa
    
    💡 **Lưu ý quan trọng:** 
    • Sử dụng ảnh X-quang rõ nét, chất lượng cao để có kết quả chính xác nhất
    • Kết quả chỉ mang tính tham khảo, cần có ý kiến của bác sĩ chuyên khoa
    • Dữ liệu của bạn được bảo mật tuyệt đối theo tiêu chuẩn y tế
    """)



# Footer - luôn hiển thị
st.markdown("""
<hr>
<div class="footer">
    <h4>🫁 Hệ thống Chẩn đoán Bệnh Phổi AI</h4>
    <p><strong>Công nghệ tiên tiến - Chẩn đoán chính xác</strong></p>
    <p>🏥 Phát triển bởi Đội ngũ Y tế Công nghệ | 📞 Hỗ trợ: 1900-XXX-XXX</p>
    <p>🌐 Website: <strong>lung-diagnosis.ai</strong> | ✉️ Email: support@lung-diagnosis.ai</p>
</div>
""", unsafe_allow_html=True)