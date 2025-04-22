import streamlit as st
import mysql.connector
import streamlit.components.v1 as components

 
st.set_page_config(page_title="Login - ONESELF MOVIES", layout="wide", initial_sidebar_state="collapsed")

 
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
    .main-container {
        padding: 2rem;
        font-family: 'Segoe UI', sans-serif;
    }
    .login-title {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        color: #333333;
        margin-bottom: 0.5rem;
    }
    .subheading {
        text-align: center;
        color: #666666;
        font-size: 18px;
        margin-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
        padding: 10px;
        height: 44px;
        border-radius: 6px;
    }
    .stButton > button {
        width: 100%;
        font-size: 16px !important;
        height: 44px;
        padding: 10px 25px;
        border-radius: 6px;
        background-color: #007bff !important;
        color: white;
        border: none;
        margin-top: 10px;
    }
    .stButton > button:hover {
        background-color: #0056b3 !important;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        font-size: 14px;
        color: #999999;
    }
    </style>
""", unsafe_allow_html=True)

 
banner_html = """
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<div id="loginBannerCarousel" class="carousel slide" data-ride="carousel" data-interval="2500" style="margin: 0; border-radius: 0; overflow: hidden;">
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="https://image.tmdb.org/t/p/original/9n2tJBplPbgR2ca05hS5CKXwP2c.jpg" class="d-block w-100" style="height: 280px; object-fit: cover; margin: 0;">
    </div>
    <div class="carousel-item">
      <img src="https://image.tmdb.org/t/p/original/9Gtg2DzBhmYamXBS1hKAhiwbBKS.jpg" class="d-block w-100" style="height: 280px; object-fit: cover; margin: 0;">
    </div>
    <div class="carousel-item">
      <img src="https://image.tmdb.org/t/p/original/t5zCBSB5xMDKcDqe91qahCOUYVV.jpg" class="d-block w-100" style="height: 280px; object-fit: cover; margin: 0;">
    </div>
  </div>
</div>
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
"""
components.html(banner_html, height=280)

 
st.markdown('<div class="main-container">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns([1, 1.5, 4, 1.5, 1])
with col3:
    st.markdown('<div class="login-title">🔐 Login to ONESELF MOVIES</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheading">Enter your credentials to continue</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="oneself-movies"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
                user = cursor.fetchone()
                cursor.close()
                conn.close()

                if user:
                    email = user[1]   
                    st.session_state.is_authenticated = True
                    st.session_state.user_info = {
                 "username": username,
                "email": email
                 }

                    st.success("✅ Login successful!")
                    st.switch_page("pages/recommendation.py")
                else:
                    st.error("Invalid username or password.")
            except Exception as e:
                st.error(f"Database error: {e}")
        else:
            st.warning("Please fill in both fields.")

    st.markdown("**Don't have an account?**")
    if st.button("Register"):
        st.switch_page("pages/register.py")
st.markdown('</div>', unsafe_allow_html=True)

 
st.markdown("""
<div class="footer">
&copy; 2025 ONESELF MOVIES. All rights reserved. Made with ❤️ by <b>Oneself Technologies</b>.
</div>
""", unsafe_allow_html=True)
