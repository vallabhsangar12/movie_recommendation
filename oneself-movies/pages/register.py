import streamlit as st
import time
import sys
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="Register - ONESELF MOVIES", layout="wide", initial_sidebar_state="collapsed")

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
<div id="registerBannerCarousel" class="carousel slide" data-ride="carousel" data-interval="2500" style="margin: 0; border-radius: 0; overflow: hidden;">
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="https://image.tmdb.org/t/p/original/8Y43POKjjKDGI9MH89NW0NAzzp8.jpg" class="d-block w-100" style="height: 280px; object-fit: cover; margin: 0;">
    </div>
    <div class="carousel-item">
      <img src="https://image.tmdb.org/t/p/original/hZkgoQYus5vegHoetLkCJzb17zJ.jpg" class="d-block w-100" style="height: 280px; object-fit: cover; margin: 0;">
    </div>
    <div class="carousel-item">
      <img src="https://image.tmdb.org/t/p/original/6Wdl9N6dL0Hi0T1qJLWSz6gMLbd.jpg" class="d-block w-100" style="height: 280px; object-fit: cover; margin: 0;">
    </div>
  </div>
</div>
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
"""
components.html(banner_html, height=280)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import register_user, user_exists


st.markdown('<div class="main-container">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns([1, 1.5, 4, 1.5, 1])
with col3:
    st.markdown('<div class="login-title">👤 Register a New Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheading">Create your account to explore ONESELF MOVIES</div>', unsafe_allow_html=True)

    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not email or not username or not password:
            st.warning("Please fill in all fields.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif user_exists(username):
            st.error("Username already exists.")
            st.info("If you already have an account, please log in below.")
            if st.button("Go to Login"):
                st.switch_page("pages/login.py")
        else:
            success = register_user(email, username, password)
            if success:
                st.success("✅ Registration successful! Redirecting to login page...")
                time.sleep(2)
                st.switch_page("pages/login.py")
            else:
                st.error("Something went wrong. Please try again.")

    st.markdown("---")
    st.markdown("**Already have an account?**")
    if st.button("Login"):
        st.switch_page("pages/login.py")

st.markdown('</div>', unsafe_allow_html=True)


st.markdown("""
<div class="footer">
&copy; 2025 ONESELF MOVIES. All rights reserved. Made with ❤️ by <b>Oneself Technologies</b>.
</div>
""", unsafe_allow_html=True)
