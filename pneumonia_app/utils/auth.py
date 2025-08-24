import streamlit as st
from utils.db_utils import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads/"
DEFAULT_AVATAR = "default_avatar.png"

def ensure_admin_exists():
    """Đảm bảo luôn có tài khoản admin mặc định"""
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE username='admin'")
        row = cursor.fetchone()
        if not row:
            hashed = generate_password_hash("admin123")
            cursor.execute("""
                INSERT INTO users (username, password, role, full_name, email, avatar)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, ("admin", hashed, "admin", "Quản trị viên", "admin@example.com", DEFAULT_AVATAR))
            conn.commit()
            print("✅ Tài khoản admin mặc định đã được tạo.")
    except Error as e:
        print(f"❌ Lỗi khi tạo admin mặc định: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def register(username, password):
    conn = get_connection()
    if not conn:
        st.error("Không kết nối được tới DB!")
        return False
    try:
        cursor = conn.cursor()
        hashed = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users (username, password) 
            VALUES (%s, %s)
        """, (username, hashed))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Tạo tài khoản thành công!")
        return True
    except Error as e:
        st.error(f"Lỗi khi đăng ký: {e}")
        return False


def login(username, password):
    """Đăng nhập, trả về dict thông tin người dùng nếu thành công"""
    ensure_admin_exists()

    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, username, password, role, full_name, email, phone, address, avatar, created_at
            FROM users WHERE username=%s
        """, (username,))
        row = cursor.fetchone()
        if row and check_password_hash(row["password"], password):
            del row["password"]
            # Lưu thông tin user vào session
            st.session_state["user"] = row
            return row
        return None
    except Error as e:
        st.error(f"Lỗi khi đăng nhập: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
