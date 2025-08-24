import streamlit as st
import pandas as pd
from utils.db_utils import get_connection

# CSS tùy chỉnh cho giao diện đẹp
st.markdown("""
<style>
    /* Màu chủ đạo xanh đậm - xanh nhạt */
    .main {
        background-color: #f8fcff;
    }
    
    /* Tiêu đề chính */
    .main-title {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(30, 58, 138, 0.3);
    }
    
    /* Card container */
    .feedback-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
        margin: 15px 0;
        border-left: 4px solid #3b82f6;
    }
    
    /* Form container */
    .form-container {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #bfdbfe;
        margin-bottom: 30px;
    }
    
    /* Filter container */
    .filter-container {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #bae6fd;
        margin: 15px 0;
    }
    
    /* Edit form container */
    .edit-form-container {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #bbf7d0;
        margin: 15px 0;
    }
    
    /* Hiển thị sao - ENHANCED */
    .star-rating {
        font-size: 32px;
        margin: 15px 0;
        letter-spacing: 3px;
        display: inline-block;
    }
    
    /* Hiệu ứng hover cho các sao */
    .star-filled {
        transition: all 0.2s ease;
        display: inline-block;
    }
    
    .star-filled:hover {
        transform: scale(1.1);
        filter: brightness(1.2);
    }
    
    /* Animation cho 5 sao */
    @keyframes pulse-gold {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .star-5-special {
        animation: pulse-gold 2s infinite;
        filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.6));
    }
    
    /* Glow effect cho rating cao */
    .star-excellent {
        filter: drop-shadow(0 0 6px rgba(255, 215, 0, 0.4));
    }
    
    .star-good {
        filter: drop-shadow(0 0 4px rgba(34, 197, 94, 0.4));
    }
    
    /* User feedback section */
    .user-feedback {
        background: linear-gradient(135deg, #ecfeff, #e0f7fa);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #0891b2;
        margin: 15px 0;
        position: relative;
    }
    
    /* Action buttons container */
    .action-buttons {
        position: absolute;
        top: 15px;
        right: 15px;
        display: flex;
        gap: 10px;
    }
    
    /* Public feedback section */
    .public-feedback {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #3b82f6;
        margin: 15px 0;
        box-shadow: 0 1px 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Admin response */
    .admin-response {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        padding: 15px;
        border-radius: 8px;
        border-left: 3px solid #0ea5e9;
        margin-top: 10px;
    }
    
    /* Username styling */
    .username {
        color: #1e40af;
        font-weight: bold;
        font-size: 16px;
    }
    
    /* Date styling */
    .date-time {
        color: #6b7280;
        font-size: 13px;
        font-style: italic;
    }
    
    /* Comment styling */
    .comment-text {
        color: #374151;
        line-height: 1.6;
        margin: 10px 0;
        padding-right: 80px; /* Để chừa chỗ cho nút edit/delete */
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        margin: 20px 0 15px 0;
        box-shadow: 0 2px 4px rgba(30, 64, 175, 0.2);
    }
    
    /* Toggle section header */
    .toggle-header {
        background: linear-gradient(135deg, #059669, #10b981);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        margin: 20px 0 15px 0;
        box-shadow: 0 2px 4px rgba(5, 150, 105, 0.2);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .toggle-header:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(5, 150, 105, 0.3);
    }
    
    /* Stats container */
    .stats-container {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid #f59e0b;
    }
    
    /* Warning and info styling */
    .stAlert > div {
        border-radius: 10px;
    }
    
    /* Delete confirmation dialog styling */
    .delete-confirm {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        border: 2px solid #fca5a5;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Edit success message */
    .edit-success {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 2px solid #86efac;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: #166534;
    }
</style>
""", unsafe_allow_html=True)

def render_stars(rating):
    """Render star rating display với màu sắc đẹp - version đơn giản cho Streamlit"""
    
    # Màu sắc cho từng mức
    color_map = {
        1: "#dc2626",  # Đỏ đậm - Rất tệ
        2: "#ea580c",  # Cam đỏ - Tệ
        3: "#d97706",  # Cam vàng - Bình thường  
        4: "#059669",  # Xanh lá đẹp - Tốt
        5: "#ffd700"   # Vàng kim - Tuyệt vời
    }
    
    rating_text = {
        1: "Rất tệ",
        2: "Tệ", 
        3: "Bình thường",
        4: "Tốt",
        5: "Tuyệt vời"
    }
    
    star_color = color_map.get(rating, "#6b7280")
    empty_color = "#e5e7eb"
    
    # Tạo HTML đơn giản
    stars_html = f'<div style="font-size: 28px; margin: 10px 0; letter-spacing: 2px;">'
    
    # Render các sao
    for i in range(1, 6):
        if i <= rating:
            stars_html += f'<span style="color: {star_color}; text-shadow: 0 1px 2px rgba(0,0,0,0.2);">★</span>'
        else:
            stars_html += f'<span style="color: {empty_color};">☆</span>'
    
    # Thêm text rating
    stars_html += f' <strong style="color: {star_color};">({rating}/5 - {rating_text.get(rating, "")})</strong></div>'
    
    return stars_html

def get_feedback_stats(feedbacks):
    """Tính toán thống kê phản hồi"""
    if not feedbacks:
        return None
    
    ratings = [fb['rating'] for fb in feedbacks]
    total = len(ratings)
    avg_rating = sum(ratings) / total
    
    # Đếm từng loại đánh giá
    rating_counts = {i: ratings.count(i) for i in range(1, 6)}
    
    return {
        'total': total,
        'average': round(avg_rating, 1),
        'counts': rating_counts
    }

def filter_feedbacks(feedbacks, rating_filter, sort_order):
    """Lọc và sắp xếp phản hồi"""
    filtered = feedbacks
    
    # Lọc theo rating
    if rating_filter != "Tất cả":
        rating_value = int(rating_filter.split()[0])
        filtered = [fb for fb in filtered if fb['rating'] == rating_value]
    
    # Sắp xếp
    if sort_order == "Mới nhất":
        filtered.sort(key=lambda x: x['created_at'], reverse=True)
    elif sort_order == "Cũ nhất":
        filtered.sort(key=lambda x: x['created_at'])
    elif sort_order == "Đánh giá cao nhất":
        filtered.sort(key=lambda x: x['rating'], reverse=True)
    elif sort_order == "Đánh giá thấp nhất":
        filtered.sort(key=lambda x: x['rating'])
    
    return filtered

def delete_feedback(feedback_id, user_id):
    """Xóa phản hồi của người dùng"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Kiểm tra xem feedback có thuộc về user này không
        cursor.execute("SELECT id FROM feedbacks WHERE id=%s AND user_id=%s", (feedback_id, user_id))
        result = cursor.fetchone()
        
        if result:
            cursor.execute("DELETE FROM feedbacks WHERE id=%s AND user_id=%s", (feedback_id, user_id))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False
    except Exception as e:
        st.error(f"Lỗi khi xóa phản hồi: {str(e)}")
        return False

def update_feedback(feedback_id, user_id, new_rating, new_comment):
    """Cập nhật phản hồi của người dùng"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Kiểm tra xem feedback có thuộc về user này không
        cursor.execute("SELECT id FROM feedbacks WHERE id=%s AND user_id=%s", (feedback_id, user_id))
        result = cursor.fetchone()
        
        if result:
            # Cập nhật feedback và thời gian sửa đổi
            cursor.execute("""
                UPDATE feedbacks 
                SET rating=%s, comment=%s, updated_at=NOW() 
                WHERE id=%s AND user_id=%s
            """, (new_rating, new_comment, feedback_id, user_id))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False
    except Exception as e:
        st.error(f"Lỗi khi cập nhật phản hồi: {str(e)}")
        return False

# Page config
st.set_page_config(
    page_title="Đánh giá & Phản hồi", 
    page_icon="⭐",
    layout="wide"
)

# Main title
st.markdown("""
<div class="main-title">
    <h1>⭐ ĐÁNH GIÁ & PHẢN HỒI</h1>
    <p>Chia sẻ trải nghiệm của bạn và đóng góp ý kiến</p>
</div>
""", unsafe_allow_html=True)

# Check authentication
if "user" not in st.session_state or not st.session_state.get("logged_in"):
    st.error("🔒 Vui lòng đăng nhập để gửi phản hồi.")
    st.stop()

user_id = st.session_state["user"]["id"]

# Feedback form
st.markdown("### 📝 Gửi phản hồi mới")

with st.form("feedback_form"):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        rating = st.slider(
            "Đánh giá của bạn", 
            1, 5, 3,  # Default value changed to 3 instead of 5
            help="Kéo để chọn số sao từ 1-5"
        )
        # Display stars preview with real-time update
        st.markdown(render_stars(int(rating)), unsafe_allow_html=True)
    
    with col2:
        comment = st.text_area(
            "Nội dung phản hồi", 
            placeholder="Chia sẻ trải nghiệm của bạn...",
            height=100
        )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col2:
        submitted = st.form_submit_button(
            "🚀 Gửi phản hồi", 
            use_container_width=True,
            type="primary"
        )

    if submitted:
        if comment.strip():
            conn = get_connection()
            cursor = conn.cursor()
            sql = """
                INSERT INTO feedbacks (user_id, username, rating, comment) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                user_id,
                st.session_state["user"]["username"],
                rating,
                comment
            ))
            conn.commit()
            conn.close()
            st.success("🎉 Cảm ơn bạn đã gửi phản hồi!")
            st.rerun()
        else:
            st.warning("⚠️ Vui lòng nhập nội dung phản hồi!")

# Get feedback data
conn = get_connection()
cursor = conn.cursor(dictionary=True)

# User's own feedbacks - thêm id để có thể xóa và chỉnh sửa
cursor.execute("""
    SELECT id, rating, comment, phan_hoi_admin, created_at, updated_at
    FROM feedbacks 
    WHERE user_id=%s 
    ORDER BY created_at DESC
""", (user_id,))
user_feedbacks = cursor.fetchall()

# All public feedbacks
cursor.execute("""
    SELECT username, rating, comment, phan_hoi_admin, created_at, updated_at
    FROM feedbacks 
    ORDER BY created_at DESC
""")
all_feedbacks = cursor.fetchall()
conn.close()

# Display user's own feedbacks
st.markdown("""
<div class="section-header">
    <h3>📌 Phản hồi của bạn</h3>
</div>
""", unsafe_allow_html=True)

if user_feedbacks:
    for i, fb in enumerate(user_feedbacks):
        # Kiểm tra xem có đang trong chế độ edit không
        edit_mode = st.session_state.get(f'edit_mode_{i}', False)
        
        if edit_mode:
            # Form chỉnh sửa
            st.markdown('<div class="edit-form-container">', unsafe_allow_html=True)
            st.markdown("### ✏️ Chỉnh sửa phản hồi")
            
            with st.form(f"edit_form_{i}"):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    new_rating = st.slider(
                        "Đánh giá mới", 
                        1, 5, fb['rating'],
                        help="Chỉnh sửa đánh giá của bạn",
                        key=f"edit_rating_{i}"
                    )
                    st.markdown(render_stars(int(new_rating)), unsafe_allow_html=True)
                
                with col2:
                    new_comment = st.text_area(
                        "Nội dung mới", 
                        value=fb['comment'],
                        height=100,
                        key=f"edit_comment_{i}"
                    )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    save_edit = st.form_submit_button(
                        "💾 Lưu thay đổi", 
                        use_container_width=True,
                        type="primary"
                    )
                
                with col2:
                    cancel_edit = st.form_submit_button(
                        "❌ Hủy", 
                        use_container_width=True
                    )
                
                if save_edit:
                    if new_comment.strip():
                        if update_feedback(fb['id'], user_id, new_rating, new_comment):
                            st.success("✅ Đã cập nhật phản hồi!")
                            st.session_state[f'edit_mode_{i}'] = False
                            st.rerun()
                        else:
                            st.error("❌ Không thể cập nhật phản hồi!")
                    else:
                        st.warning("⚠️ Vui lòng nhập nội dung phản hồi!")
                
                if cancel_edit:
                    st.session_state[f'edit_mode_{i}'] = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            # Hiển thị bình thường
            st.markdown('<div class="user-feedback" style="position: relative;">', unsafe_allow_html=True)
            
            # Nút action ở góc phải trên
            col_content, col_actions = st.columns([5, 1])
            
            with col_content:
                # Star rating
                st.markdown(render_stars(fb['rating']), unsafe_allow_html=True)
                
                # Comment
                st.markdown(f'<div class="comment-text">💬 "{fb["comment"]}"</div>', unsafe_allow_html=True)
                
                # Date - hiển thị cả created_at và updated_at nếu có
                date_text = f'📅 {fb["created_at"]}'
                if fb['updated_at'] and fb['updated_at'] != fb['created_at']:
                    date_text += f' (Đã sửa: {fb["updated_at"]})'
                st.markdown(f'<div class="date-time">{date_text}</div>', unsafe_allow_html=True)
                
                # Admin response if exists
                if fb['phan_hoi_admin']:
                    st.markdown(f"""
                    <div class="admin-response">
                        <strong>💡 Phản hồi từ Admin:</strong><br>
                        {fb['phan_hoi_admin']}
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_actions:
                # Nút chỉnh sửa
                if st.button(
                    "✏️", 
                    key=f"edit_btn_{i}", 
                    help="Chỉnh sửa phản hồi này",
                    use_container_width=True
                ):
                    st.session_state[f'edit_mode_{i}'] = True
                    # Reset các state khác
                    if f'confirm_delete_{i}' in st.session_state:
                        st.session_state[f'confirm_delete_{i}'] = False
                    st.rerun()
                
                # Nút xóa
                if st.button(
                    "🗑️", 
                    key=f"delete_btn_{i}", 
                    help="Xóa phản hồi này",
                    use_container_width=True
                ):
                    st.session_state[f'confirm_delete_{i}'] = True
                    # Reset edit mode nếu có
                    if f'edit_mode_{i}' in st.session_state:
                        st.session_state[f'edit_mode_{i}'] = False
                    st.rerun()
                
                # Xác nhận xóa
                if st.session_state.get(f'confirm_delete_{i}', False):
                    st.markdown('<div class="delete-confirm">', unsafe_allow_html=True)
                    st.warning("⚠️ Bạn có chắc muốn xóa?")
                    
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.button("✅ Xóa", key=f"confirm_yes_{i}", use_container_width=True):
                            if delete_feedback(fb['id'], user_id):
                                st.success("✅ Đã xóa phản hồi!")
                                st.session_state[f'confirm_delete_{i}'] = False
                                st.rerun()
                            else:
                                st.error("❌ Không thể xóa phản hồi!")
                    
                    with col_no:
                        if st.button("❌ Hủy", key=f"confirm_no_{i}", use_container_width=True):
                            st.session_state[f'confirm_delete_{i}'] = False
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        
else:
    st.info("📭 Bạn chưa có phản hồi nào.")

# Toggle for community feedbacks
st.markdown("""
<div class="toggle-header">
    <h3>🌍 Phản hồi từ cộng đồng</h3>
</div>
""", unsafe_allow_html=True)

# Button to show/hide community feedbacks
show_community = st.button(
    "👀 Xem tất cả phản hồi từ cộng đồng" if not st.session_state.get('show_community_feedbacks', False) 
    else "🙈 Ẩn phản hồi cộng đồng", 
    key="toggle_community",
    use_container_width=True
)

if show_community:
    st.session_state['show_community_feedbacks'] = not st.session_state.get('show_community_feedbacks', False)
    st.rerun()

# Display community feedbacks if toggled on
if st.session_state.get('show_community_feedbacks', False):
    if all_feedbacks:
        # Statistics
        stats = get_feedback_stats(all_feedbacks)
        if stats:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Tổng phản hồi", stats['total'])
            
            with col2:
                st.metric("⭐ Đánh giá trung bình", f"{stats['average']}/5")
            
            with col3:
                most_common = max(stats['counts'], key=stats['counts'].get)
                st.metric("🎯 Đánh giá phổ biến nhất", f"{most_common} sao")
            
            with col4:
                five_star_percent = round((stats['counts'][5] / stats['total']) * 100, 1)
                st.metric("🌟 Tỷ lệ 5 sao", f"{five_star_percent}%")
        
        # Filters
        st.markdown("### 🔍 Bộ lọc & Sắp xếp")
        
        col1, col2 = st.columns(2)
        
        with col1:
            rating_options = ["Tất cả", "5 sao", "4 sao", "3 sao", "2 sao", "1 sao"]
            rating_filter = st.selectbox(
                "Lọc theo đánh giá:",
                rating_options,
                key="rating_filter"
            )
        
        with col2:
            sort_options = ["Mới nhất", "Cũ nhất", "Đánh giá cao nhất", "Đánh giá thấp nhất"]
            sort_order = st.selectbox(
                "Sắp xếp theo:",
                sort_options,
                key="sort_order"
            )
        
        # Apply filters
        filtered_feedbacks = filter_feedbacks(all_feedbacks, rating_filter, sort_order)
        
        # Display filtered results count
        if len(filtered_feedbacks) != len(all_feedbacks):
            st.info(f"🔍 Hiển thị {len(filtered_feedbacks)} trong tổng số {len(all_feedbacks)} phản hồi")
        
        # Display filtered feedbacks
        if filtered_feedbacks:
            for fb in filtered_feedbacks:
                st.markdown('<div class="public-feedback">', unsafe_allow_html=True)
                
                # Username
                st.markdown(f'<div class="username">👤 {fb["username"]}</div>', unsafe_allow_html=True)
                
                # Star rating
                st.markdown(render_stars(fb['rating']), unsafe_allow_html=True)
                
                # Comment
                st.markdown(f'<div class="comment-text">💬 "{fb["comment"]}"</div>', unsafe_allow_html=True)
                
                # Date - hiển thị cả created_at và updated_at nếu có
                date_text = f'📅 {fb["created_at"]}'
                if fb['updated_at'] and fb['updated_at'] != fb['created_at']:
                    date_text += f' (Đã sửa: {fb["updated_at"]})'
                st.markdown(f'<div class="date-time">{date_text}</div>', unsafe_allow_html=True)
                
                # Admin response if exists
                if fb['phan_hoi_admin']:
                    st.markdown(f"""
                    <div class="admin-response">
                        <strong>💡 Phản hồi từ Admin:</strong><br>
                        {fb['phan_hoi_admin']}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("📭 Không tìm thấy phản hồi phù hợp với bộ lọc.")
    else:
        st.info("📭 Chưa có phản hồi nào từ cộng đồng.")

# Footer
st.markdown("""
---
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>💙 Cảm ơn bạn đã đóng góp ý kiến để chúng tôi cải thiện dịch vụ!</p>
</div>
""", unsafe_allow_html=True)