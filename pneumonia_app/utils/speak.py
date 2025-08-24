from gtts import gTTS
import os
import streamlit as st

def speak(text: str, lang: str = "vi"):
    """
    Tạo audio từ text và phát bằng Streamlit
    """
    tts = gTTS(text=text, lang=lang)
    audio_file = "diagnosis.mp3"
    tts.save(audio_file)

    # Phát trực tiếp trong Streamlit
    audio_bytes = open(audio_file, "rb").read()
    st.audio(audio_bytes, format="audio/mp3")

    # Xóa file tạm sau khi phát
    if os.path.exists(audio_file):
        os.remove(audio_file)
