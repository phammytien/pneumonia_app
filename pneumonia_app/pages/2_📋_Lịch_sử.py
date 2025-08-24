import streamlit as st
import pandas as pd
from utils.db_utils import get_connection
import math

st.set_page_config(page_title="Lịch sử chẩn đoán", layout="wide")

# Custom CSS với theme xanh nhạt - xanh đậm - trắng (giữ nguyên CSS cũ)
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset và base styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header chính với gradient xanh đẹp */
    .main-header {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 50%, #1d4ed8 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.15);
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
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 0 4px 8px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        opacity: 0.95;
        font-size: 1.3rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* Container cho filters với thiết kế card */
    .filter-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 1px solid #cbd5e1;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.08);
        border-left: 5px solid #3b82f6;
    }
    
    .filter-title {
        color: #1e40af;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Metrics cards đẹp hơn */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: white;
        border: 2px solid #e0f2fe;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #1e40af);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
        border-color: #3b82f6;
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: #3b82f6;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e40af;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #64748b;
        font-weight: 500;
    }
    
    /* Cải thiện expander với theme xanh */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 2px solid #bae6fd;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border-color: #3b82f6;
        transform: translateX(4px);
    }
    
    .streamlit-expanderHeader p {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e40af;
        margin: 0;
    }
    
    .streamlit-expanderContent {
        background: white;
        border: 2px solid #e0f2fe;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
    }
    
    /* Info boxes trong expander */
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .info-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid #3b82f6;
    }
    
    .info-card p {
        margin: 0.5rem 0;
        font-size: 1.1rem;
        color: #334155;
    }
    
    .info-card strong {
        color: #1e40af;
        font-weight: 600;
    }
    
    /* Recommendation box đẹp hơn */
    .recommendation-box {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        position: relative;
    }
    
    .recommendation-box::before {
        content: '💡';
        position: absolute;
        top: -10px;
        left: 20px;
        background: white;
        padding: 0.5rem;
        border-radius: 50%;
        font-size: 1.2rem;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
    }
    
    .recommendation-text {
        color: #065f46;
        font-size: 1.1rem;
        font-weight: 500;
        margin: 0;
        padding-left: 2rem;
    }
    
    /* Image container với styling đẹp */
    .image-container {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
        margin: 2rem auto 0;
        max-width: 400px;
        border: 3px solid #e0f2fe;
        transition: all 0.3s ease;
    }
    
    .image-container:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.2);
        border-color: #3b82f6;
    }
    
    /* Empty state với theme xanh */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 3px dashed #94a3b8;
        border-radius: 20px;
        margin: 3rem 0;
    }
    
    .empty-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        color: #64748b;
        opacity: 0.7;
    }
    
    .empty-state h3 {
        color: #334155;
        font-size: 1.8rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .empty-state p {
        color: #64748b;
        font-size: 1.2rem;
        margin: 0;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #e0f2fe;
        border-radius: 8px;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
    }
    
    /* Divider đẹp hơn */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #3b82f6, transparent);
        margin: 3rem 0;
    }
    
    /* Section titles */
    .section-title {
        color: #1e40af;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 2rem 0 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Warning styling */
    .stWarning {
        background: linear-gradient(135deg, #fef3cd 0%, #fde68a 100%);
        border: 2px solid #f59e0b;
        color: #92400e;
    }
    
    /* Success styling */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 2px solid #10b981;
        color: #065f46;
    }
    
    /* Error styling */
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 2px solid #ef4444;
        color: #991b1b;
    }
    
    /* Pagination styling */
    .pagination-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 2px solid #e0f2fe;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
    }
    
    .pagination-info {
        color: #1e40af;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Bulk action styling */
    .bulk-actions {
        background: linear-gradient(135deg, #fef3cd 0%, #fde68a 100%);
        border: 2px solid #f59e0b;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.1);
    }
    
    .bulk-title {
        color: #92400e;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Delete buttons */
    .delete-btn {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 2px solid #ef4444;
        border-radius: 8px;
        color: #991b1b;
        padding: 0.5rem 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .delete-btn:hover {
        background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(239, 68, 68, 0.2);
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        background: white;
        border: 2px solid #e0f2fe;
        border-radius: 8px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stCheckbox > label:hover {
        border-color: #3b82f6;
        background: #f0f9ff;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .info-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .metrics-container {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header với gradient đẹp
st.markdown("""
<div class="main-header">
    <h1>📜 Lịch sử chẩn đoán</h1>
    <p>Theo dõi và quản lý kết quả chẩn đoán của bạn</p>
</div>
""", unsafe_allow_html=True)

# Kiểm tra đăng nhập
if "user" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔐 Bạn cần đăng nhập để xem lịch sử.")
    st.stop()

# Khởi tạo session states
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'selected_records' not in st.session_state:
    st.session_state.selected_records = []
if 'refresh_data' not in st.session_state:
    st.session_state.refresh_data = False

# Hàm xóa bản ghi đơn lẻ
def delete_record(record_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lich_su_chan_doan WHERE id=%s AND user_id=%s", 
                      (record_id, st.session_state.user['id']))
        conn.commit()
        cursor.close()
        conn.close()
        st.session_state.refresh_data = True
        return True
    except Exception as e:
        st.error(f"Lỗi khi xóa: {e}")
        return False

# Hàm xóa nhiều bản ghi
def delete_multiple_records(record_ids):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        placeholders = ','.join(['%s'] * len(record_ids))
        query = f"DELETE FROM lich_su_chan_doan WHERE id IN ({placeholders}) AND user_id=%s"
        cursor.execute(query, record_ids + [st.session_state.user['id']])
        conn.commit()
        cursor.close()
        conn.close()
        st.session_state.selected_records = []
        st.session_state.refresh_data = True
        return True
    except Exception as e:
        st.error(f"Lỗi khi xóa hàng loạt: {e}")
        return False

try:
    # Lấy dữ liệu từ DB
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, filename, result, algorithm, confidence, severity, recommendation, created_at
        FROM lich_su_chan_doan 
        WHERE user_id=%s 
        ORDER BY created_at DESC
    """, (st.session_state.user['id'],))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if rows:
        df = pd.DataFrame(rows)
        
        # Format confidence (DB lưu 0-1)
        df["confidence"] = df["confidence"].apply(
            lambda x: f"{float(x):.2f}%" if x is not None else "N/A"
        )
        
        # Bộ lọc trong container đẹp
        st.markdown("""
        <div class="filter-section">
            <div class="filter-title">🔍 Bộ lọc tìm kiếm</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            algo_filter = st.selectbox("🤖 Thuật toán", ["Tất cả"] + sorted(df["algorithm"].unique()))
        with col2:
            res_filter = st.selectbox("📋 Kết luận", ["Tất cả"] + sorted(df["result"].unique()))
        with col3:
            severity_filter = st.selectbox("⚠️ Mức độ", ["Tất cả"] + sorted(df["severity"].unique()))
        with col4:
            records_per_page = st.selectbox("📄 Số bản ghi/trang", [5, 10, 20, 50], index=1)
        
        # Áp dụng bộ lọc
        filtered_df = df.copy()
        if algo_filter != "Tất cả":
            filtered_df = filtered_df[filtered_df["algorithm"] == algo_filter]
        if res_filter != "Tất cả":
            filtered_df = filtered_df[filtered_df["result"] == res_filter]
        if severity_filter != "Tất cả":
            filtered_df = filtered_df[filtered_df["severity"] == severity_filter]
        
        # Tính toán phân trang
        total_records = len(filtered_df)
        total_pages = math.ceil(total_records / records_per_page)
        
        # Đảm bảo page hợp lệ
        if st.session_state.page > total_pages and total_pages > 0:
            st.session_state.page = 1
        
        # Thông tin tổng quan với metrics cards đẹp
        st.markdown("""
        <div class="metrics-container">
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-value">{}</div>
                <div class="metric-label">Tổng số bản ghi</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">🔍</div>
                <div class="metric-value">{}</div>
                <div class="metric-label">Sau khi lọc</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">📅</div>
                <div class="metric-value">{}</div>
                <div class="metric-label">Gần nhất</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">📄</div>
                <div class="metric-value">{}/{}</div>
                <div class="metric-label">Trang hiện tại</div>
            </div>
        </div>
        """.format(
            len(df),
            len(filtered_df),
            str(filtered_df['created_at'].iloc[0])[:16] if len(filtered_df) > 0 else "N/A",
            st.session_state.page,
            max(total_pages, 1)
        ), unsafe_allow_html=True)
        
        if len(filtered_df) > 0:
            # Phần chọn và xóa hàng loạt
            st.markdown("""
            <div class="bulk-actions">
                <div class="bulk-title">🗂️ Thao tác hàng loạt</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                select_all = st.checkbox("🔲 Chọn tất cả trong trang này")
            with col2:
                if st.button("🗑️ Xóa đã chọn", type="secondary"):
                    if st.session_state.selected_records:
                        if delete_multiple_records(st.session_state.selected_records):
                            st.success(f"✅ Đã xóa {len(st.session_state.selected_records)} bản ghi!")
                            st.rerun()
                    else:
                        st.warning("⚠️ Chưa chọn bản ghi nào!")
            with col3:
                if st.button("🆑 Bỏ chọn tất cả"):
                    st.session_state.selected_records = []
                    st.rerun()
            
            # Lấy dữ liệu cho trang hiện tại
            start_idx = (st.session_state.page - 1) * records_per_page
            end_idx = start_idx + records_per_page
            page_df = filtered_df.iloc[start_idx:end_idx]
            
            # Xử lý select all
            if select_all:
                st.session_state.selected_records = list(page_df['id'].values)
         
            
            # Hiển thị danh sách với checkbox và nút xóa
            for idx, row in page_df.iterrows():
                # Container cho mỗi bản ghi
                record_container = st.container()
                
                with record_container:
                    col1, col2, col3 = st.columns([0.5, 8, 1])
                    
                    with col1:
                        # Checkbox để chọn bản ghi
                        is_selected = st.checkbox("", 
                                                key=f"select_{row['id']}", 
                                                value=row['id'] in st.session_state.selected_records)
                        if is_selected and row['id'] not in st.session_state.selected_records:
                            st.session_state.selected_records.append(row['id'])
                        elif not is_selected and row['id'] in st.session_state.selected_records:
                            st.session_state.selected_records.remove(row['id'])
                    
                    with col2:
                        # Expander cho thông tin chi tiết
                        with st.expander(f"📌 {row['created_at']} - {row['result']} ({row['severity']})", expanded=False):
                            
                            # Grid layout cho thông tin
                            st.markdown(f"""
                            <div class="info-grid">
                                <div class="info-card">
                                    <p><strong>📁 File:</strong> {row['filename']}</p>
                                    <p><strong>🤖 Thuật toán:</strong> {row['algorithm']}</p>
                                </div>
                                <div class="info-card">
                                    <p><strong>📊 Độ tin cậy:</strong> {row['confidence']}</p>
                                    <p><strong>⚠️ Mức độ:</strong> {row['severity']}</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Khuyến nghị với styling đẹp
                            st.markdown(f"""
                            <div class="recommendation-box">
                                <p class="recommendation-text"><strong>Khuyến nghị:</strong> {row['recommendation']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Hiển thị ảnh với styling đẹp
                            if row["filename"]:
                                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                                st.image(f"uploads/{row['filename']}", caption=row["filename"], width=350)
                                st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col3:
                        # Nút xóa đơn lẻ
                        if st.button("🗑️", key=f"delete_{row['id']}", help="Xóa bản ghi này"):
                            if st.session_state.get(f'confirm_delete_{row["id"]}', False):
                                if delete_record(row['id']):
                                    st.success("✅ Đã xóa bản ghi!")
                                    st.rerun()
                            else:
                                st.session_state[f'confirm_delete_{row["id"]}'] = True
                                st.warning("⚠️ Nhấn lại để xác nhận xóa!")
                                st.rerun()
            
            # Phần điều hướng phân trang ở cuối trang
            if total_pages > 1:
             
                
                col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
                
                with col1:
                    if st.button("⏮️ Đầu", disabled=(st.session_state.page <= 1)):
                        st.session_state.page = 1
                        st.rerun()
                
                with col2:
                    if st.button("◀️ Trước", disabled=(st.session_state.page <= 1)):
                        st.session_state.page -= 1
                        st.rerun()
                
                with col3:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 0.5rem; color: #1e40af; font-weight: 600;">
                        Trang {st.session_state.page} / {total_pages}<br>
                        <small style="color: #64748b;">({start_idx + 1}-{min(end_idx, total_records)} trong {total_records} bản ghi)</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    if st.button("▶️ Sau", disabled=(st.session_state.page >= total_pages)):
                        st.session_state.page += 1
                        st.rerun()
                
                with col5:
                    if st.button("⏭️ Cuối", disabled=(st.session_state.page >= total_pages)):
                        st.session_state.page = total_pages
                        st.rerun()
        
        else:
            # Không có kết quả sau khi lọc
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🔍</div>
                <h3>Không tìm thấy kết quả</h3>
                <p>Thử thay đổi bộ lọc để xem nhiều kết quả hơn</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Empty state đẹp
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📋</div>
            <h3>Chưa có lịch sử chẩn đoán</h3>
            <p>Hãy thực hiện chẩn đoán đầu tiên để xem kết quả tại đây</p>
        </div>
        """, unsafe_allow_html=True)
        

except Exception as e:
    st.error(f"❌ **Lỗi hệ thống:** {e}")

# Reset refresh flag
if st.session_state.refresh_data:
    st.session_state.refresh_data = False