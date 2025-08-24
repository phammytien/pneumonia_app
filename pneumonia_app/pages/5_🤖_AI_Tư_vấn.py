import streamlit as st
import google.generativeai as genai
import mysql.connector
from mysql.connector import Error

# ==========================
# 🎨 CSS Styling
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
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
        padding: 2rem 1.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="20" cy="20" r="1" fill="white" opacity="0.1"/><circle cx="80" cy="40" r="1" fill="white" opacity="0.1"/><circle cx="40" cy="80" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header .subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* Status Card */
    .status-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
        border: 2px solid #e0f2fe;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .status-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #60a5fa, #93c5fd);
    }
    
    .status-title {
        color: #1e40af;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .severity-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 500;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .severity-nang { background: linear-gradient(135deg, #dc2626, #ef4444); color: white; }
    .severity-trung-binh { background: linear-gradient(135deg, #d97706, #f59e0b); color: white; }
    .severity-nhe { background: linear-gradient(135deg, #059669, #10b981); color: white; }
    .severity-khong { background: linear-gradient(135deg, #3b82f6, #60a5fa); color: white; }
    .severity-chua-co { background: linear-gradient(135deg, #6b7280, #9ca3af); color: white; }
    
    /* Chat Container */
    .chat-container {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
        border: 1px solid #e0f2fe;
        max-height: 600px;
        overflow-y: auto;
        margin-bottom: 1rem;
    }
    
    /* Chat Messages */
    .stChatMessage {
        margin-bottom: 1rem;
    }
    
    .stChatMessage[data-testid="chat-message-user"] {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe) !important;
        border-radius: 15px 15px 5px 15px !important;
        padding: 1rem !important;
        border: 1px solid #93c5fd !important;
        margin-left: 2rem !important;
    }
    
    .stChatMessage[data-testid="chat-message-assistant"] {
        background: linear-gradient(135deg, #f8fafc, #f1f5f9) !important;
        border-radius: 15px 15px 15px 5px !important;
        padding: 1rem !important;
        border: 1px solid #e2e8f0 !important;
        margin-right: 2rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }
    
    /* Input Section */
    .input-section {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
        border: 2px solid #e0f2fe;
        margin-top: 1rem;
    }
    
    .input-label {
        color: #1e40af;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: block;
        font-size: 1.1rem;
    }
    
    /* Custom Scrollbar */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #60a5fa, #3b82f6);
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #3b82f6, #1e40af);
    }
    
    /* Warning/Info Messages */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    .stAlert[data-baseweb="notification"] [data-testid="stNotificationContentWarning"] {
        background: linear-gradient(135deg, #fef3c7, #fde68a) !important;
        color: #92400e !important;
    }
    
    .stAlert[data-baseweb="notification"] [data-testid="stNotificationContentInfo"] {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe) !important;
        color: #1e40af !important;
    }
    
    /* Sidebar Enhancement */
    .css-1d391kg {
        background: linear-gradient(180deg, #f0f8ff 0%, #e6f3ff 100%) !important;
    }
    
    /* Button Enhancement */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1e40af) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="AI Tư vấn Sức khỏe", 
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="collapsed"
)

# ==========================
# 🎨 Header Section
# ==========================
st.markdown("""
<div class="main-header">
    <h1>🏥 AI Tư vấn Sức khỏe</h1>
    <div class="subtitle">Hệ thống chẩn đoán và tư vấn thông minh với Gemini AI</div>
</div>
""", unsafe_allow_html=True)

# ==========================
# 🔹 Kiểm tra đăng nhập
# ==========================
if "user" not in st.session_state or not st.session_state.logged_in:
    st.markdown("""
    <div class="status-card">
        <div class="status-title">⚠️ Thông báo</div>
        <p style="color: #dc2626; font-weight: 500;">Vui lòng đăng nhập để sử dụng dịch vụ tư vấn sức khỏe.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ==========================
# 🔹 Kết nối MySQL
# ==========================
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3307,
            database="pneumonia_app_1",
            user="root",
            password="123456"
        )
        return conn if conn.is_connected() else None
    except Error as e:
        st.error(f"❌ Lỗi kết nối cơ sở dữ liệu: {e}")
        return None

def close_connection(conn):
    if conn and conn.is_connected():
        conn.close()

# 🔹 Lấy severity gần nhất
def get_latest_severity(user_id):
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT severity, created_at
        FROM lich_su_chan_doan
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (user_id,)
    )
    row = cursor.fetchone()
    close_connection(conn)
    return row if row else None

# ==========================
# 🔹 Hiển thị thông tin người dùng và severity
# ==========================
col1, col2 = st.columns([2, 1])

with col1:
    latest_result = get_latest_severity(st.session_state.user["id"])
    if latest_result:
        severity = latest_result["severity"]
        created_at = latest_result["created_at"]
        
        # Xác định class CSS cho severity
        severity_class = {
            "Nặng": "severity-nang",
            "Trung bình": "severity-trung-binh", 
            "Nhẹ": "severity-nhe",
            "Không phát hiện": "severity-khong"
        }.get(severity, "severity-chua-co")
        
        # Icon cho từng mức độ
        severity_icon = {
            "Nặng": "🔴",
            "Trung bình": "🟡",
            "Nhẹ": "🟢", 
            "Không phát hiện": "🔵"
        }.get(severity, "⚪")
        
        st.markdown(f"""
        <div class="status-card">
            <div class="status-title">{severity_icon} Tình trạng sức khỏe hiện tại</div>
            <div>
                <span class="severity-badge {severity_class}">{severity}</span>
                <p style="margin-top: 1rem; color: #64748b; font-size: 0.9rem;">
                    Cập nhật lần cuối: {created_at.strftime("%d/%m/%Y %H:%M")}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        latest_severity = severity
    else:
        st.markdown("""
        <div class="status-card">
            <div class="status-title">📊 Tình trạng sức khỏe</div>
            <div>
                <span class="severity-badge severity-chua-co">Chưa có dữ liệu</span>
                <p style="margin-top: 1rem; color: #64748b; font-size: 0.9rem;">
                    Vui lòng thực hiện chẩn đoán để có kết quả tư vấn chính xác hơn.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        latest_severity = None

with col2:
    st.markdown(f"""
    <div class="status-card">
        <div class="status-title">👤 Xin chào</div>
        <div style="color: #1e40af; font-weight: 600; font-size: 1.1rem;">
            {st.session_state.user.get("username", "Người dùng")}
        </div>
        <p style="color: #64748b; font-size: 0.9rem; margin-top: 0.5rem;">
            Chúng tôi sẵn sàng hỗ trợ bạn 24/7
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================
# 🔹 Gemini Client
# ==========================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# Lưu hội thoại
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================
# 🔹 Chat Interface
# ==========================
st.markdown("""
<div style="margin: 2rem 0 1rem 0;">
    <h3 style="color: #1e40af; font-weight: 600; margin-bottom: 1rem;">💬 Trò chuyện với AI Bác sĩ</h3>
</div>
""", unsafe_allow_html=True)

# Container cho chat messages
chat_container = st.container()
with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem; color: #64748b;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
            <h4 style="color: #1e40af; margin-bottom: 0.5rem;">Chào mừng bạn đến với AI Tư vấn Sức khỏe!</h4>
            <p>Hãy đặt câu hỏi về sức khỏe của bạn, tôi sẵn sàng hỗ trợ.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Hiển thị lịch sử chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# ==========================
# 🔹 Chat Input Section
# ==========================
st.markdown("""
<div class="input-section">
    <label class="input-label">💭 Đặt câu hỏi của bạn:</label>
</div>
""", unsafe_allow_html=True)

query = st.chat_input("Ví dụ: Tôi bị ho khan, có nên uống thuốc gì không?", key="health_chat_input")

if query:
    # Thêm tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": query})
    
    with st.chat_message("user"):
        st.write(query)

    # Xử lý response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Đang suy nghĩ..."):
            # Ngữ cảnh cơ bản
            base_context = """Bạn là một AI bác sĩ tư vấn thân thiện và chuyên nghiệp. 
            Hãy trả lời bằng tiếng Việt, ngắn gọn nhưng đầy đủ thông tin, dễ hiểu. 
            Luôn nhắc nhở người dùng rằng đây chỉ là tư vấn sơ bộ và không thay thế việc khám bác sĩ trực tiếp."""

            # Ngữ cảnh theo mức độ bệnh
            if latest_severity == "Nặng":
                severity_context = """Người dùng có kết quả chẩn đoán mức độ NẶNG. 
                Khi tư vấn về các triệu chứng liên quan đến hô hấp hoặc phổi, hãy nhấn mạnh:
                - Cần khám bác sĩ KHẨN CẤP
                - Có thể cần nhập viện theo dõi
                - Không được chủ quan với các triệu chứng"""
            elif latest_severity == "Trung bình":
                severity_context = """Người dùng có kết quả chẩn đoán mức độ TRUNG BÌNH.
                Khi tư vấn về các vấn đề hô hấp, khuyên:
                - Nên đi khám bác sĩ chuyên khoa để kiểm tra chi tiết
                - Theo dõi chặt chẽ các triệu chứng
                - Tuân thủ điều trị nếu có"""
            elif latest_severity == "Nhẹ":
                severity_context = """Người dùng có kết quả chẩn đoán mức độ NHẸ.
                Có thể tư vấn:
                - Theo dõi thêm các triệu chứng
                - Chăm sóc tại nhà với các biện pháp phù hợp
                - Đi khám nếu triệu chứng nặng lên"""
            elif latest_severity == "Không phát hiện":
                severity_context = """Người dùng có kết quả chẩn đoán KHÔNG PHÁT HIỆN vấn đề.
                Tập trung vào:
                - Duy trì lối sống lành mạnh
                - Phòng ngừa bệnh tật
                - Khám sức khỏe định kỳ"""
            else:
                severity_context = """Chưa có dữ liệu chẩn đoán từ hệ thống. 
                Có thể tư vấn chung về sức khỏe và khuyên thực hiện kiểm tra nếu cần thiết."""

            # Prompt đầy đủ
            prompt = f"""{base_context}

{severity_context}

LƯU Ý QUAN TRỌNG:
- Nếu người dùng hỏi về vấn đề sức khỏe khác (không liên quan đến phổi/hô hấp), hãy trả lời bình thường mà không cần nhắc đến kết quả chẩn đoán trước đó
- Luôn khuyên tham khảo ý kiến bác sĩ chuyên khoa khi cần thiết
- Không đưa ra chẩn đoán chắc chắn, chỉ tư vấn hướng xử lý

Câu hỏi của người dùng: {query}"""

            try:
                response = model.generate_content(prompt)
                answer = response.text
                
                # Định dạng response đẹp hơn
                if "❌" not in answer and "Lỗi" not in answer:
                    answer = f"🔍 **Tư vấn từ AI Bác sĩ:**\n\n{answer}\n\n---\n💡 *Lời khuyên này chỉ mang tính chất tham khảo. Hãy tham khảo ý kiến bác sĩ chuyên khoa để có chẩn đoán và điều trị chính xác nhất.*"
                
            except Exception as e:
                answer = f"❌ **Xin lỗi, đã có lỗi xảy ra khi xử lý yêu cầu của bạn.**\n\nChi tiết lỗi: {e}\n\n🔄 Vui lòng thử lại sau hoặc liên hệ bộ phận hỗ trợ kỹ thuật."

            # Hiển thị câu trả lời
            st.write(answer)
            
            # Lưu vào session state
            st.session_state.messages.append({"role": "assistant", "content": answer})

# ==========================
# 🔹 Footer Information
# ==========================
st.markdown("""
---
<div style="text-align: center; padding: 2rem 0; color: #64748b; font-size: 0.9rem;">
    <p><strong>🏥 Hệ thống AI Tư vấn Sức khỏe</strong></p>
    <p>Được phát triển với ❤️ và công nghệ Gemini AI | © 2024</p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">
        ⚠️ <em>Đây là hệ thống hỗ trợ tư vấn, không thay thế cho việc khám và điều trị trực tiếp tại cơ sở y tế.</em>
    </p>
</div>
""", unsafe_allow_html=True)