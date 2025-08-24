import streamlit as st

def show_diagnosis_conclusion(conclusion: str):
    """
    Hiển thị kết luận chuẩn đoán kèm thông điệp mô tả
    """
    if conclusion == "Có bệnh":
        st.info("💡 Chuẩn đoán: Phát hiện dấu hiệu viêm phổi hoặc tổn thương trên X-ray. Vui lòng tham khảo ý kiến bác sĩ.")
    elif conclusion == "Không bệnh":
        st.success("💡 Chuẩn đoán: Không phát hiện dấu hiệu bất thường trên X-ray.")
    elif conclusion == "Không phải X-ray":
        st.warning("💡 Chuẩn đoán: Ảnh tải lên không phải X-ray phổi, vui lòng kiểm tra lại.")
    else:
        st.error("💡 Chuẩn đoán: Không xác định, vui lòng thử lại với ảnh khác.")
