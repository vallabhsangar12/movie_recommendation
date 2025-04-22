import mysql.connector
import streamlit as st

 
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="oneself-movies"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"❌ Could not connect to database: {err}")
        return None
 
def check_db_connection():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            st.success(f"✅ Connected to database: `{db_name}`")
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            st.error(f"❌ Connection test failed: {err}")
            return False
    return False


def register_user(email, username, password):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user (email, username, password) VALUES (%s, %s, %s)",
            (email, username, password)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error while inserting user: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def user_exists(username):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
        return user is not None
    finally:
        cursor.close()
        conn.close()


def validate_login(username, password):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()
        return user is not None
    finally:
        cursor.close()
        conn.close()
