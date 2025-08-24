import streamlit as st
from utils.db_utils import get_connection
import datetime

# CSS tùy chỉnh cho giao diện chuyên nghiệp
st.markdown("""
<style>
    /* Màu chủ đạo xanh đậm - xanh nhạt - nền trắng */
    .main {
        background-color: #f8fcff;
    }
    
    /* Header section */
    .admin-header {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.3);
    }
    
    .admin-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .admin-header p {
        margin: 10px 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Statistics cards */
    .stats-container {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }
    
    .stat-card {
        flex: 1;
        min-width: 200px;
        background: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
        border-left: 5px solid #3b82f6;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.2);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e40af;
        margin: 0;
    }
    
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin: 5px 0 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Feedback card */
    .feedback-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.1);
        border: 1px solid #e5f3ff;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .feedback-card:hover {
        box-shadow: 0 10px 35px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    
    .feedback-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 2px solid #f1f5f9;
    }
    
    .user-info {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .user-avatar {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .user-details h4 {
        margin: 0;
        color: #1e40af;
        font-size: 1.2rem;
    }
    
    .user-details p {
        margin: 5px 0 0 0;
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    /* Star rating */
    .star-rating-admin {
        font-size: 24px;
        margin: 15px 0;
    }
    
    .star-filled {
        color: #fbbf24;
        text-shadow: 0 1px 3px rgba(251, 191, 36, 0.5);
    }
    
    .star-empty {
        color: #e5e7eb;
    }
    
    /* Comment section */
    .comment-section {
        background: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        margin: 20px 0;
    }
    
    .comment-text {
        color: #374151;
        font-size: 1.1rem;
        line-height: 1.6;
        margin: 0;
        font-style: italic;
    }
    
    /* Admin replies section */
    .replies-section {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .replies-header {
        color: #0369a1;
        font-weight: bold;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .admin-reply {
        background: white;
        padding: 15px 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 3px solid #0ea5e9;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.1);
    }
    
    .admin-reply-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    
    .admin-name {
        color: #0369a1;
        font-weight: bold;
        font-size: 0.95rem;
    }
    
    .reply-date {
        color: #6b7280;
        font-size: 0.8rem;
    }
    
    .reply-text {
        color: #374151;
        line-height: 1.5;
    }
    
    /* Action buttons */
    .action-buttons {
        display: flex;
        gap: 15px;
        margin-top: 20px;
        flex-wrap: wrap;
    }
    
    /* New reply form */
    .reply-form {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        padding: 25px;
        border-radius: 15px;
        margin-top: 20px;
        border: 1px solid #bfdbfe;
    }
    
    .reply-form h5 {
        color: #1e40af;
        margin: 0 0 15px 0;
        font-size: 1.1rem;
    }
    
    /* Edit form */
    .edit-form {
        background: linear-gradient(135deg, #fef3e2, #fed7aa);
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border: 1px solid #f97316;
    }
    
    /* Priority indicators */
    .priority-high {
        border-left-color: #ef4444 !important;
    }
    
    .priority-medium {
        border-left-color: #f59e0b !important;
    }
    
    .priority-low {
        border-left-color: #10b981 !important;
    }
    
    /* Status badges */
    .status-badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-new {
        background: #fef3c7;
        color: #92400e;
    }
    
    .status-replied {
        background: #d1fae5;
        color: #065f46;
    }
    
    /* No data state */
    .no-data {
        text-align: center;
        padding: 60px 30px;
        color: #6b7280;
    }
    
    .no-data-icon {
        font-size: 4rem;
        margin-bottom: 20px;
        opacity: 0.5;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .feedback-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 15px;
        }
        
        .stats-container {
            flex-direction: column;
        }
        
        .action-buttons {
            flex-direction: column;
        }
    }
</style>
""", unsafe_allow_html=True)

def render_stars_admin(rating):
    """Render star rating for admin view"""
    stars = ""
    for i in range(1, 6):
        if i <= rating:
            stars += "⭐"
        else:
            stars += "☆"
    return f"{stars} ({rating}/5)"

def get_priority_class(rating):
    """Get priority class based on rating"""
    if rating <= 2:
        return "priority-high"
    elif rating == 3:
        return "priority-medium"
    else:
        return "priority-low"

def get_status_badge(has_replies):
    """Get status badge based on reply status"""
    if has_replies:
        return '<span class="status-badge status-replied">Đã phản hồi</span>'
    else:
        return '<span class="status-badge status-new">Chưa phản hồi</span>'

def get_user_initials(username):
    """Get user initials for avatar"""
    if username:
        words = username.split()
        if len(words) >= 2:
            return f"{words[0][0]}{words[1][0]}".upper()
        else:
            return username[0].upper() if username else "U"
    return "U"

# Page configuration
st.set_page_config(
    page_title="Quản lý phản hồi", 
    page_icon="📋",
    layout="wide"
)

# Check admin access
if "user" not in st.session_state or st.session_state["user"]["role"] != "admin":
    st.error("❌ Bạn không có quyền truy cập trang này")
    st.stop()

# Initialize edit state in session
if "editing_reply" not in st.session_state:
    st.session_state.editing_reply = {}

# Header
st.markdown("""
<div class="admin-header">
    <h1>📋 QUẢN LÝ PHẢN HỒI</h1>
    <p>Tổng hợp và quản lý phản hồi từ người dùng</p>
</div>
""", unsafe_allow_html=True)

# Get feedback data
conn = get_connection()
cursor = conn.cursor(dictionary=True)

# Get statistics
cursor.execute("SELECT COUNT(*) as total FROM feedbacks")
total_feedbacks = cursor.fetchone()['total']

cursor.execute("SELECT COUNT(*) as replied FROM feedbacks WHERE phan_hoi_admin IS NOT NULL")
replied_feedbacks = cursor.fetchone()['replied']

cursor.execute("SELECT AVG(rating) as avg_rating FROM feedbacks")
avg_rating_result = cursor.fetchone()['avg_rating']
avg_rating = round(avg_rating_result, 1) if avg_rating_result else 0

# Statistics cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{total_feedbacks}</div>
        <div class="stat-label">Tổng phản hồi</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{replied_feedbacks}</div>
        <div class="stat-label">Đã phản hồi</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    pending = total_feedbacks - replied_feedbacks
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{pending}</div>
        <div class="stat-label">Chưa phản hồi</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{avg_rating}</div>
        <div class="stat-label">Đánh giá TB</div>
    </div>
    """, unsafe_allow_html=True)

# Filter options
st.markdown("### 🔍 Bộ lọc")
col1, col2, col3 = st.columns(3)

with col1:
    filter_rating = st.selectbox("Lọc theo đánh giá", ["Tất cả", "5 sao", "4 sao", "3 sao", "2 sao", "1 sao"])

with col2:
    filter_status = st.selectbox("Lọc theo trạng thái", ["Tất cả", "Đã phản hồi", "Chưa phản hồi"])

with col3:
    sort_by = st.selectbox("Sắp xếp theo", ["Mới nhất", "Cũ nhất", "Đánh giá cao", "Đánh giá thấp"])

# Build filter query
where_conditions = []
if filter_rating != "Tất cả":
    rating_value = int(filter_rating.split()[0])
    where_conditions.append(f"rating = {rating_value}")

if filter_status == "Đã phản hồi":
    where_conditions.append("phan_hoi_admin IS NOT NULL")
elif filter_status == "Chưa phản hồi":
    where_conditions.append("phan_hoi_admin IS NULL")

where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""

# Build order clause
if sort_by == "Mới nhất":
    order_clause = "ORDER BY created_at DESC"
elif sort_by == "Cũ nhất":
    order_clause = "ORDER BY created_at ASC"
elif sort_by == "Đánh giá cao":
    order_clause = "ORDER BY rating DESC, created_at DESC"
else:  # Đánh giá thấp
    order_clause = "ORDER BY rating ASC, created_at DESC"

# Get filtered feedbacks
query = f"SELECT * FROM feedbacks {where_clause} {order_clause}"
cursor.execute(query)
feedbacks = cursor.fetchall()

st.markdown(f"### 📝 Danh sách phản hồi ({len(feedbacks)} kết quả)")

if feedbacks:
    for fb in feedbacks:
        # Check if has replies
        cursor.execute("""
            SELECT COUNT(*) as reply_count FROM admin_replies WHERE feedback_id=%s
        """, (fb['id'],))
        has_replies = cursor.fetchone()['reply_count'] > 0
        
        # Create feedback card using Streamlit components
        with st.container():
            # Header section
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### 👤 {fb['username']}")
                st.markdown(f"📅 {fb['created_at']}")
            with col2:
                if has_replies:
                    st.success("✅ Đã phản hồi")
                else:
                    st.warning("⏳ Chưa phản hồi")
            
            # Rating
            st.markdown(f"**Đánh giá:** {render_stars_admin(fb['rating'])}")
            
            # Comment
            st.info(f"💬 \"{fb['comment']}\"")
            
            # Admin replies
            cursor.execute("""
                SELECT * FROM admin_replies
                WHERE feedback_id=%s
                ORDER BY created_at ASC
            """, (fb['id'],))
            replies = cursor.fetchall()
            
            if replies:
                st.markdown("**💬 Phản hồi từ Admin:**")
                for rp in replies:
                    reply_key = f"{rp['id']}"
                    
                    # Check if this reply is being edited
                    if st.session_state.editing_reply.get(reply_key, False):
                        # Edit mode
                        st.markdown("""
                        <div class="edit-form">
                            <h5>✏️ Chỉnh sửa phản hồi</h5>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        edit_text = st.text_area(
                            "Nội dung chỉnh sửa",
                            value=rp['reply'],
                            key=f"edit_text_{reply_key}",
                            help="Chỉnh sửa nội dung phản hồi của bạn",
                            label_visibility="collapsed"
                        )
                        
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            if st.button("💾 Lưu thay đổi", key=f"save_{reply_key}", type="primary"):
                                if edit_text.strip():
                                    # Update the reply in database
                                    cursor.execute("""
                                        UPDATE admin_replies 
                                        SET reply = %s, updated_at = CURRENT_TIMESTAMP
                                        WHERE id = %s
                                    """, (edit_text.strip(), rp['id']))
                                    conn.commit()
                                    
                                    # Clear edit state
                                    st.session_state.editing_reply[reply_key] = False
                                    
                                    # Show success message
                                    st.success("✅ Đã cập nhật phản hồi thành công!")
                                    st.balloons()  # Add celebration animation
                                    
                                    # Wait a moment then refresh
                                    import time
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("⚠️ Nội dung không được để trống!")
                        
                        with col2:
                            if st.button("❌ Hủy", key=f"cancel_{reply_key}"):
                                st.session_state.editing_reply[reply_key] = False
                                st.rerun()
                    
                    else:
                        # Display mode
                        col1, col2 = st.columns([5, 1])
                        with col1:
                            # Show edited indicator if reply has been updated
                            edited_text = ""
                            if 'updated_at' in rp and rp['updated_at'] and rp['updated_at'] != rp['created_at']:
                                edited_text = " *(đã chỉnh sửa)*"
                            
                            st.markdown(f"""
                            > 👨‍💼 **{rp['admin_name']}** ({rp['created_at']}){edited_text}  
                            > {rp['reply']}
                            """)
                        
                        with col2:
                            # Action buttons for each reply
                            col_edit, col_del = st.columns(2)
                            
                            with col_edit:
                                if st.button("✏️", key=f"edit_btn_{reply_key}", help="Chỉnh sửa phản hồi"):
                                    st.session_state.editing_reply[reply_key] = True
                                    st.rerun()
                            
                            with col_del:
                                if st.button("🗑️", key=f"del_rp_{rp['id']}", help="Xóa phản hồi"):
                                    cursor.execute("DELETE FROM admin_replies WHERE id=%s", (rp['id'],))
                                    conn.commit()
                                    st.success("✅ Đã xóa phản hồi thành công!")
                                    import time
                                    time.sleep(1)
                                    st.rerun()
            
            # Reply form
            st.markdown("**💌 Phản hồi mới:**")
            reply_key = f"reply_{fb['id']}"
            reply_text = st.text_area(
                "Nội dung phản hồi", 
                key=reply_key,
                placeholder="Nhập phản hồi của bạn...",
                label_visibility="collapsed"
            )
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                if st.button("💌 Gửi phản hồi", key=f"send_{fb['id']}", type="primary"):
                    if reply_text.strip():
                        sql = """
                            INSERT INTO admin_replies (feedback_id, admin_id, admin_name, reply, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        """
                        cursor.execute(sql, (
                            fb['id'],
                            st.session_state["user"]["id"],
                            st.session_state["user"]["username"],
                            reply_text
                        ))
                        conn.commit()
                        
                        # Show success message with animation
                        st.success("✅ Đã gửi phản hồi thành công!")
                        st.balloons()
                        
                        # Clear the text area and refresh
                        import time
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("⚠️ Vui lòng nhập nội dung phản hồi!")
            
            with col3:
                if st.button("🗑️ Xóa đánh giá", key=f"del_fb_{fb['id']}"):
                    # Show confirmation dialog using session state
                    if f"confirm_delete_{fb['id']}" not in st.session_state:
                        st.session_state[f"confirm_delete_{fb['id']}"] = False
                    
                    if not st.session_state[f"confirm_delete_{fb['id']}"]:
                        st.session_state[f"confirm_delete_{fb['id']}"] = True
                        st.warning("⚠️ Bạn có chắc chắn muốn xóa đánh giá này? Nhấn lại để xác nhận.")
                        st.rerun()
                    else:
                        # Delete all replies first
                        cursor.execute("DELETE FROM admin_replies WHERE feedback_id=%s", (fb['id'],))
                        # Then delete the feedback
                        cursor.execute("DELETE FROM feedbacks WHERE id=%s", (fb['id'],))
                        conn.commit()
                        
                        # Clear confirmation state
                        del st.session_state[f"confirm_delete_{fb['id']}"]
                        
                        st.success("✅ Đã xóa đánh giá và tất cả phản hồi liên quan thành công!")
                        import time
                        time.sleep(1)
                        st.rerun()
            
            st.divider()

else:
    st.info("📭 Không có phản hồi nào phù hợp với bộ lọc của bạn.")

conn.close()

# Footer
st.markdown("""
---
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>🛠️ Trang quản lý dành cho Admin - Phiên bản 2.1 (với chức năng chỉnh sửa)</p>
</div>
""", unsafe_allow_html=True)