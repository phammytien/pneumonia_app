import streamlit as st, pandas as pd
from utils.db_utils import get_connection
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Thống kê", layout="wide")

# Custom CSS cho giao diện đẹp
st.markdown("""
<style>
    /* Màu nền chính */
    .main {
        background-color: #f8fbff;
    }
    
    /* Header styling */
    .stats-header {
        background: linear-gradient(135deg, #4a90e2 0%, #2c5aa0 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(74, 144, 226, 0.3);
    }
    
    .stats-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    
    .stats-header p {
        color: #e8f4f8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Card containers */
    .stats-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e3f2fd;
    }
    
    .control-panel {
        background: linear-gradient(135deg, #e3f2fd 0%, #f8faff 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-top: 4px solid #2196f3;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid #c8e6c9;
        margin: 0.5rem 0;
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2e7d32;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #4caf50;
        font-weight: 500;
        margin-top: 0.3rem;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #4a90e2;
    }
    
    /* Section titles */
    .section-title {
        color: #2c5aa0;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e3f2fd;
        display: flex;
        align-items: center;
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
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 10px;
        border: 2px solid #e3f2fd;
    }
    
    /* Info messages */
    .info-message {
        background: linear-gradient(135deg, #f0f9ff 0%, #f8faff 100%);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #b3e5fc;
        color: #0277bd;
    }
    
    .no-data-message {
        background: linear-gradient(135deg, #fff3e0 0%, #fff8f0 100%);
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        border: 1px solid #ffcc02;
        color: #e65100;
    }
    
    /* Filter section */
    .filter-section {
        background: linear-gradient(135deg, #f3e5f5 0%, #fce4ec 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e1bee7;
    }
    
    /* Export buttons */
    .export-section {
        background: linear-gradient(135deg, #e0f2f1 0%, #f1f8e9 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        border: 1px solid #a5d6a7;
    }
</style>
""", unsafe_allow_html=True)

# Header chính
st.markdown("""
<div class="stats-header">
    <h1>📊 Thống Kê & Phân Tích</h1>
    <p>Phân tích chi tiết kết quả chẩn đoán và xu hướng theo thời gian</p>
</div>
""", unsafe_allow_html=True)

# Kiểm tra đăng nhập
if "user" not in st.session_state or not st.session_state.logged_in:
    st.markdown("""
    <div class="info-message">
        <h3>⚠️ Cần đăng nhập</h3>
        <p>Bạn cần đăng nhập để xem thống kê cá nhân.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Hàm để normalize confidence về dạng phần trăm chuẩn
def normalize_confidence(confidence):
    """
    Chuyển đổi confidence về dạng phần trăm chuẩn (0-100)
    """
    if confidence > 100:
        # Nếu lớn hơn 100, có thể đã bị nhân 100 lần, chia về
        return confidence / 100
    elif confidence > 1:
        # Nếu từ 1-100, giữ nguyên
        return confidence
    else:
        # Nếu từ 0-1, nhân 100
        return confidence * 100

def show_detailed_report(df):
    """
    Hiển thị báo cáo chi tiết với các phân tích sâu
    """
    st.markdown("---")
    st.markdown("""
    <div class="stats-header" style="margin-top: 2rem;">
        <h1>📈 Báo Cáo Chi Tiết</h1>
        <p>Phân tích toàn diện và đánh giá xu hướng chẩn đoán</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Nút đóng báo cáo
    if st.button("❌ Đóng báo cáo chi tiết", type="secondary"):
        st.session_state.show_detailed_report = False
        st.rerun()
    
    # 1. Phân tích theo thuật toán
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4 class="section-title">🤖 So sánh hiệu suất thuật toán</h4>', unsafe_allow_html=True)
    
    col_algo1, col_algo2 = st.columns(2)
    
    with col_algo1:
        # Bảng so sánh thuật toán
        if 'algorithm' in df.columns:
            algo_stats = df.groupby('algorithm').agg({
                'confidence': ['mean', 'std', 'count'],
                'result': lambda x: (x.isin(['NORMAL', 'Không bệnh'])).mean() * 100
            }).round(2)
            
            algo_stats.columns = ['Độ tin cậy TB', 'Độ lệch chuẩn', 'Số lượng', 'Tỷ lệ bình thường (%)']
            st.subheader("📊 Thống kê theo thuật toán")
            st.dataframe(algo_stats, use_container_width=True)
        else:
            st.info("Không có dữ liệu thuật toán để phân tích")
    
    with col_algo2:
        # Biểu đồ box plot confidence theo thuật toán
        if 'algorithm' in df.columns and len(df['algorithm'].unique()) > 1:
            fig_box = px.box(df, x='algorithm', y='confidence', 
                           title="Phân bố độ tin cậy theo thuật toán",
                           color='algorithm',
                           color_discrete_sequence=['#2196f3', '#4caf50'])
            fig_box.update_layout(showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("Cần ít nhất 2 thuật toán để so sánh")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Phân tích theo mức độ nghiêm trọng
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4 class="section-title">⚠️ Phân tích mức độ nghiêm trọng</h4>', unsafe_allow_html=True)
    
    col_sev1, col_sev2 = st.columns(2)
    
    with col_sev1:
        if 'severity' in df.columns:
            severity_counts = df['severity'].value_counts()
            fig_severity = px.bar(
                x=severity_counts.index, 
                y=severity_counts.values,
                title="Phân bố mức độ nghiêm trọng",
                color=severity_counts.values,
                color_continuous_scale='RdYlBu_r'
            )
            fig_severity.update_xaxis(title="Mức độ")
            fig_severity.update_yaxis(title="Số lượng")
            st.plotly_chart(fig_severity, use_container_width=True)
        else:
            st.info("Không có dữ liệu mức độ nghiêm trọng")
    
    with col_sev2:
        if 'severity' in df.columns:
            # Bảng thống kê chi tiết
            severity_stats = df.groupby('severity').agg({
                'confidence': 'mean',
                'result': 'count'
            }).round(2)
            severity_stats.columns = ['Độ tin cậy TB (%)', 'Số lượng']
            st.subheader("📋 Chi tiết theo mức độ")
            st.dataframe(severity_stats, use_container_width=True)
            
            # Tổng kết
            total_severe = len(df[df['severity'].isin(['Nặng', 'Trung bình'])])
            st.metric("🚨 Tổng ca nghiêm trọng", total_severe)
        else:
            st.info("Không có dữ liệu để phân tích")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Xu hướng theo tuần
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4 class="section-title">📅 Phân tích xu hướng theo tuần</h4>', unsafe_allow_html=True)
    
    # Xử lý dữ liệu theo tuần
    df_copy = df.copy()
    df_copy['week'] = pd.to_datetime(df_copy['created_at']).dt.to_period('W').astype(str)
    df_weekly = df_copy.groupby('week').agg({
        'result': 'count',
        'confidence': 'mean'
    }).reset_index()
    
    df_weekly.columns = ['Tuần', 'Số chẩn đoán', 'Độ tin cậy TB']
    
    # Biểu đồ xu hướng tuần
    fig_weekly = go.Figure()
    
    # Số lượng chẩn đoán
    fig_weekly.add_trace(go.Scatter(
        x=df_weekly['Tuần'],
        y=df_weekly['Số chẩn đoán'],
        mode='lines+markers',
        name='Số chẩn đoán',
        line=dict(color='#2196f3', width=3)
    ))
    
    # Độ tin cậy trung bình (trục phụ)
    fig_weekly.add_trace(go.Scatter(
        x=df_weekly['Tuần'],
        y=df_weekly['Độ tin cậy TB'],
        mode='lines+markers',
        name='Độ tin cậy TB (%)',
        yaxis='y2',
        line=dict(color='#ff9800', width=3)
    ))
    
    fig_weekly.update_layout(
        title="Xu hướng theo tuần",
        xaxis=dict(title="Tuần", tickangle=-45),
        yaxis=dict(title="Số chẩn đoán"),
        yaxis2=dict(
            title="Độ tin cậy (%)",
            overlaying="y",
            side="right"
        ),
        hovermode='x unified',
        template='plotly_white'
    )
    
    st.plotly_chart(fig_weekly, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 4. Phân tích thời gian trong ngày
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4 class="section-title">🕐 Phân tích theo giờ trong ngày</h4>', unsafe_allow_html=True)
    
    col_hour1, col_hour2 = st.columns(2)
    
    with col_hour1:
        # Phân bố theo giờ
        df_copy['hour'] = pd.to_datetime(df_copy['created_at']).dt.hour
        hourly_counts = df_copy['hour'].value_counts().sort_index()
        
        fig_hourly = px.line(
            x=hourly_counts.index,
            y=hourly_counts.values,
            title="Số lượng chẩn đoán theo giờ",
            markers=True
        )
        fig_hourly.update_xaxis(title="Giờ trong ngày")
        fig_hourly.update_yaxis(title="Số lượng chẩn đoán")
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    with col_hour2:
        # Top 5 giờ cao điểm
        top_hours = hourly_counts.nlargest(5)
        st.subheader("🔥 Top 5 giờ cao điểm")
        for hour, count in top_hours.items():
            st.write(f"**{hour:02d}:00 - {hour+1:02d}:00**: {count} lượt")
        
        # Thống kê theo ca
        morning = len(df_copy[(df_copy['hour'] >= 6) & (df_copy['hour'] < 12)])
        afternoon = len(df_copy[(df_copy['hour'] >= 12) & (df_copy['hour'] < 18)])
        evening = len(df_copy[(df_copy['hour'] >= 18) & (df_copy['hour'] < 24)])
        night = len(df_copy[(df_copy['hour'] >= 0) & (df_copy['hour'] < 6)])
        
        st.subheader("📊 Thống kê theo ca")
        st.write(f"🌅 **Sáng (6-12h)**: {morning} lượt")
        st.write(f"☀️ **Chiều (12-18h)**: {afternoon} lượt")
        st.write(f"🌆 **Tối (18-24h)**: {evening} lượt")
        st.write(f"🌙 **Đêm (0-6h)**: {night} lượt")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 5. Phân tích độ chính xác
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4 class="section-title">🎯 Phân tích độ chính xác chi tiết</h4>', unsafe_allow_html=True)
    
    col_acc1, col_acc2, col_acc3 = st.columns(3)
    
    with col_acc1:
        # Phân loại độ chính xác
        high_conf = len(df[df['confidence'] >= 90])
        medium_conf = len(df[(df['confidence'] >= 70) & (df['confidence'] < 90)])
        low_conf = len(df[df['confidence'] < 70])
        
        st.subheader("📊 Phân loại độ tin cậy")
        st.metric("🟢 Cao (≥90%)", high_conf)
        st.metric("🟡 Trung bình (70-90%)", medium_conf)
        st.metric("🔴 Thấp (<70%)", low_conf)
    
    with col_acc2:
        # Histogram độ chính xác
        fig_hist = px.histogram(
            df, x='confidence', 
            nbins=20,
            title="Phân bố độ tin cậy",
            color_discrete_sequence=['#2196f3']
        )
        fig_hist.update_xaxis(title="Độ tin cậy (%)")
        fig_hist.update_yaxis(title="Số lượng")
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col_acc3:
        # Thống kê tổng hợp
        st.subheader("📈 Thống kê tổng hợp")
        st.metric("📊 Trung bình", f"{df['confidence'].mean():.1f}%")
        st.metric("📏 Trung vị", f"{df['confidence'].median():.1f}%")
        st.metric("📐 Độ lệch chuẩn", f"{df['confidence'].std():.1f}%")
        st.metric("⬆️ Cao nhất", f"{df['confidence'].max():.1f}%")
        st.metric("⬇️ Thấp nhất", f"{df['confidence'].min():.1f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 6. Khuyến nghị và kết luận
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4 class="section-title">💡 Khuyến nghị và kết luận</h4>', unsafe_allow_html=True)
    
    # Tính toán các chỉ số để đưa ra khuyến nghị
    total_cases = len(df)
    pneumonia_rate = len(df[df['result'].isin(['PNEUMONIA', 'Có bệnh'])]) / total_cases * 100
    avg_confidence = df['confidence'].mean()
    low_confidence_rate = len(df[df['confidence'] < 70]) / total_cases * 100
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.subheader("🔍 Phân tích tổng quan")
        st.write(f"• **Tổng số chẩn đoán**: {total_cases} ca")
        st.write(f"• **Tỷ lệ viêm phổi**: {pneumonia_rate:.1f}%")
        st.write(f"• **Độ tin cậy trung bình**: {avg_confidence:.1f}%")
        st.write(f"• **Tỷ lệ độ tin cậy thấp**: {low_confidence_rate:.1f}%")
    
    with col_rec2:
        st.subheader("💡 Khuyến nghị")
        
        if pneumonia_rate > 30:
            st.warning("⚠️ Tỷ lệ phát hiện viêm phổi cao, cần theo dõi sát sao")
        else:
            st.success("✅ Tỷ lệ viêm phổi trong mức bình thường")
        
        if avg_confidence >= 85:
            st.success("✅ Độ tin cậy hệ thống tốt")
        elif avg_confidence >= 75:
            st.info("ℹ️ Độ tin cậy hệ thống ở mức khá")
        else:
            st.warning("⚠️ Cần cải thiện độ tin cậy hệ thống")
        
        if low_confidence_rate > 20:
            st.warning("⚠️ Nhiều ca có độ tin cậy thấp, cần xem xét lại")
        else:
            st.success("✅ Tỷ lệ ca độ tin cậy thấp chấp nhận được")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Panel điều khiển
st.markdown('<div class="control-panel">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">🔧 Bộ lọc và điều khiển</h3>', unsafe_allow_html=True)

col_filter1, col_filter2, col_filter3 = st.columns([2, 2, 1])

with col_filter1:
    algorithm_filter = st.selectbox(
        "🤖 Chọn thuật toán:",
        ["Tất cả", "YOLO11", "RF-MobileNet"],
        help="Lọc kết quả theo thuật toán cụ thể"
    )

with col_filter2:
    date_range = st.selectbox(
        "📅 Khoảng thời gian:",
        ["Tất cả", "30 ngày qua", "90 ngày qua", "1 năm qua"],
        help="Lọc dữ liệu theo khoảng thời gian"
    )

with col_filter3:
    if st.button("🔄 Làm mới", use_container_width=True):
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

try:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Xây dựng query động dựa trên filter
    query = """
        SELECT result, severity, confidence, created_at, algorithm
        FROM lich_su_chan_doan 
        WHERE user_id=%s
    """
    params = [st.session_state.user['id']]
    
    # Thêm filter thuật toán
    if algorithm_filter != "Tất cả":
        query += " AND algorithm=%s"
        params.append(algorithm_filter)
    
    # Thêm filter thời gian
    if date_range != "Tất cả":
        if date_range == "30 ngày qua":
            query += " AND created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)"
        elif date_range == "90 ngày qua":
            query += " AND created_at >= DATE_SUB(NOW(), INTERVAL 90 DAY)"
        elif date_range == "1 năm qua":
            query += " AND created_at >= DATE_SUB(NOW(), INTERVAL 1 YEAR)"
    
    query += " ORDER BY created_at DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if rows:
        df = pd.DataFrame(rows)
        
        # Normalize confidence values
        df['confidence'] = df['confidence'].apply(normalize_confidence)
        
        # Metrics tổng quan
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">📈 Tổng quan thống kê</h3>', unsafe_allow_html=True)
        
        col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
        
        total_diagnoses = len(df)
        normal_count = len(df[df['result'].isin(['NORMAL', 'Không bệnh'])])
        pneumonia_count = len(df[df['result'].isin(['PNEUMONIA', 'Có bệnh'])])
        avg_confidence = df['confidence'].mean()
        
        with col_metric1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{total_diagnoses}</div>
                <div class="metric-label">📊 Tổng chẩn đoán</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_metric2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{normal_count}</div>
                <div class="metric-label">✅ Bình thường</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_metric3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{pneumonia_count}</div>
                <div class="metric-label">⚠️ Viêm phổi</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_metric4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{avg_confidence:.1f}%</div>
                <div class="metric-label">🎯 Độ tin cậy TB</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Layout 2 cột cho biểu đồ
        col_chart1, col_chart2 = st.columns([1, 1])
        
        # Biểu đồ tròn - Tỷ lệ NORMAL/PNEUMONIA
        with col_chart1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h4 class="section-title">🥧 Tỷ lệ chẩn đoán</h4>', unsafe_allow_html=True)
            
            pie = px.pie(
                df, 
                names="result", 
                title="",
                color_discrete_sequence=['#4caf50', '#f44336', '#ff9800', '#2196f3']
            )
            pie.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont_size=12
            )
            pie.update_layout(
                font=dict(size=12),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Biểu đồ tròn - Phân bố thuật toán
        with col_chart2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h4 class="section-title">🤖 Phân bố thuật toán</h4>', unsafe_allow_html=True)
            
            if 'algorithm' in df.columns:
                algo_pie = px.pie(
                    df, 
                    names="algorithm", 
                    title="",
                    color_discrete_sequence=['#2196f3', '#4caf50']
                )
                algo_pie.update_traces(
                    textposition='inside', 
                    textinfo='percent+label',
                    textfont_size=12
                )
                algo_pie.update_layout(
                    font=dict(size=12),
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(algo_pie, use_container_width=True)
            else:
                st.info("Không có dữ liệu thuật toán")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Biểu đồ theo thời gian
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h4 class="section-title">📅 Xu hướng theo thời gian</h4>', unsafe_allow_html=True)
        
        # Xử lý dữ liệu theo tháng
        df["month"] = pd.to_datetime(df["created_at"]).dt.to_period("M").astype(str)
        df_monthly = df.groupby("month").agg(
            count=("result", "count"),
            avg_conf=("confidence", "mean"),
            normal_count=("result", lambda x: sum(x.isin(['NORMAL', 'Không bệnh']))),
            pneumonia_count=("result", lambda x: sum(x.isin(['PNEUMONIA', 'Có bệnh'])))
        ).reset_index()

        # Sắp xếp theo thời gian
        df_monthly["month"] = pd.to_datetime(df_monthly["month"])
        df_monthly = df_monthly.sort_values("month")
        df_monthly["month"] = df_monthly["month"].dt.strftime("%Y-%m")

        # Biểu đồ kết hợp
        fig = go.Figure()

        # Cột: số lượng chẩn đoán bình thường
        fig.add_trace(go.Bar(
            x=df_monthly["month"],
            y=df_monthly["normal_count"],
            name="Bình thường",
            marker_color="#4caf50",
            opacity=0.8
        ))

        # Cột: số lượng chẩn đoán viêm phổi
        fig.add_trace(go.Bar(
            x=df_monthly["month"],
            y=df_monthly["pneumonia_count"],
            name="Viêm phổi",
            marker_color="#f44336",
            opacity=0.8
        ))

        # Đường: độ chính xác trung bình
        fig.add_trace(go.Scatter(
            x=df_monthly["month"],
            y=df_monthly["avg_conf"],
            name="Độ tin cậy TB (%)",
            mode="lines+markers",
            yaxis="y2",
            line=dict(color="#ff9800", width=3),
            marker=dict(size=8)
        ))

        # Cấu hình layout
        fig.update_layout(
            title="",
            xaxis=dict(title="Tháng", tickangle=-45),
            yaxis=dict(title="Số lượng chẩn đoán"),
            yaxis2=dict(
                title="Độ tin cậy (%)",
                overlaying="y",
                side="right",
                range=[0, 100],
                tickformat=".1f"
            ),
            barmode='stack',
            legend=dict(
                orientation="h",
                y=-0.2,
                x=0.5,
                xanchor="center"
            ),
            hovermode='x unified',
            template='plotly_white'
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Bảng chi tiết mới nhất
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h4 class="section-title">📋 Lịch sử gần đây</h4>', unsafe_allow_html=True)
        
        # Hiển thị 10 bản ghi mới nhất
        recent_df = df.head(10)[['created_at', 'result', 'algorithm', 'confidence', 'severity']].copy()
        recent_df['confidence'] = recent_df['confidence'].round(1)
        recent_df['created_at'] = pd.to_datetime(recent_df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
        
        st.dataframe(
            recent_df,
            column_config={
                "created_at": "Thời gian",
                "result": "Kết quả",
                "algorithm": "Thuật toán",
                "confidence": st.column_config.NumberColumn("Độ tin cậy (%)", format="%.1f%%"),
                "severity": "Mức độ"
            },
            use_container_width=True,
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Phần xuất dữ liệu
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.markdown('<h4 class="section-title">💾 Xuất dữ liệu</h4>', unsafe_allow_html=True)
        
        col_export1, col_export2, col_export3 = st.columns([1, 1, 1])
        
        with col_export1:
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📄 Tải CSV",
                data=csv_data,
                file_name=f"thong_ke_{st.session_state.user['username']}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_export2:
            if st.button("📊 Xem báo cáo chi tiết", use_container_width=True):
                # Tạo session state để hiển thị báo cáo chi tiết
                st.session_state.show_detailed_report = True
                st.rerun()
        
        with col_export3:
            if st.button("🏠 Về trang chủ", use_container_width=True):
                st.switch_page("app.py")
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Báo cáo chi tiết (hiển thị khi được yêu cầu)
        if st.session_state.get('show_detailed_report', False):
            show_detailed_report(df)

    else:
        st.markdown("""
        <div class="no-data-message">
            <h3>📭 Chưa có dữ liệu</h3>
            <p>Bạn chưa thực hiện chẩn đoán nào hoặc không có dữ liệu phù hợp với bộ lọc đã chọn.</p>
            <p>Hãy thực hiện một số chẩn đoán để xem thống kê tại đây!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Nút hành động khi không có dữ liệu
        col_action1, col_action2 = st.columns([1, 1])
        
        with col_action1:
            if st.button("🩻 Chẩn đoán ngay", use_container_width=True):
                st.switch_page("pages/1_🔍_Chẩn_đoán.py")
        
        with col_action2:
            if st.button("🏠 Về trang chủ", use_container_width=True):
                st.switch_page("app.py")

except Exception as e:
    st.markdown(f"""
    <div class="no-data-message">
        <h3>❌ Lỗi hệ thống</h3>
        <p>Không thể tải dữ liệu thống kê: {str(e)}</p>
        <p>Vui lòng thử lại sau hoặc liên hệ quản trị viên.</p>
    </div>
    """, unsafe_allow_html=True)