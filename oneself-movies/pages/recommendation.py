import streamlit as st
import pickle
import requests
import mysql.connector
import streamlit.components.v1 as components

 
st.set_page_config(page_title="Recommendation - ONESELF MOVIES", layout="wide", initial_sidebar_state="collapsed")

 
st.markdown("""<style>
html, body, [data-testid="stAppViewContainer"] {
    margin: 0; padding: 0;
}
[data-testid="stSidebar"] { display: none; }
.main-container { padding: 1rem 2rem; font-family: 'Segoe UI', sans-serif; }
.header-title { font-size: 30px; font-weight: 700; color: #fff; margin-bottom: 1rem; }
.stTextInput > div > div > input { font-size: 16px; padding: 10px; height: 44px; border-radius: 6px; }
.stButton > button {
    font-size: 16px !important; height: 44px; padding: 10px 25px;
    border-radius: 6px; background-color: #007bff !important; color: white;
    border: none; margin-top: 10px;
}
.stButton > button:hover { background-color: #0056b3 !important; }
.user-box {
    background-color: #f8f9fa; padding: 1rem; border-radius: 10px; color: #333;
    box-shadow: 0 0 5px rgba(0,0,0,0.1);
}
.footer {
    margin-top: 2rem; text-align: center; color: #888;
    font-size: 14px; padding: 1rem 0; border-top: 1px solid #eaeaea;
}
</style>""", unsafe_allow_html=True)
 
if "is_authenticated" not in st.session_state or not st.session_state["is_authenticated"]:
    st.warning("Please log in to access this page.")
    st.stop()

user = st.session_state.get("user_info", {})
username = user.get("username", "Guest")
email = user.get("email", "guest@example.com")

 
menu_col1, menu_col2 = st.columns([4, 1])
with menu_col2:
    st.markdown(f"<h5 style='text-align:right;'>👋 Welcome, <span style='color:#00C9FF'>{username.capitalize()}</span></h5>", unsafe_allow_html=True)
    menu_option = st.selectbox("👤 Menu", ["Select Option", "User Info", "Update Password", "Logout"], index=0)

    if menu_option == "User Info":
        st.markdown(f"<div class='user-box'><b>Username:</b> {username}<br><b>Email:</b> {email}</div>", unsafe_allow_html=True)

    elif menu_option == "Update Password":
        st.markdown("<div class='user-box'><b>🔐 Update Password</b><br><br>", unsafe_allow_html=True)
        old_pass = st.text_input("Enter old password", type="password")
        new_pass = st.text_input("Enter new password", type="password")
        if st.button("Update Password"):
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="", database="oneself-movies")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user WHERE username=%s AND password=%s", (username, old_pass))
                if cursor.fetchone():
                    cursor.execute("UPDATE user SET password=%s WHERE username=%s", (new_pass, username))
                    conn.commit()
                    st.success("Password updated successfully.")
                else:
                    st.error("Old password is incorrect.")
                cursor.close()
                conn.close()
            except Exception as e:
                st.error(f"Error updating password: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu_option == "Logout":
        st.session_state.clear()
        st.success("✅ You have been logged out. Redirecting to login page...")
        st.markdown(
            """
            <meta http-equiv="refresh" content="2; url=/login" />
            """,
            unsafe_allow_html=True
        )
        st.stop()
 
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
 
st.markdown("<div class='header-title'>🎬 Find Movies You'll Love</div>", unsafe_allow_html=True)
try:
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movie_list = movies['title'].values
    selected_movie = st.selectbox("Search or choose a movie", movie_list)
    show_rec = st.button("SEARCH")
except Exception as e:
    st.error(f"Error loading movie data: {e}")
    st.stop()

 
components.html("""
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<div id="bannerCarousel" class="carousel slide" data-ride="carousel" data-interval="2500" style="border-radius: 10px; overflow: hidden;">
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="https://image.tmdb.org/t/p/original/8UlWHLMpgZm9bx6QYh0NFoq67TZ.jpg" class="d-block w-100" style="height: 240px; object-fit: cover;">
    </div>
    <div class="carousel-item">
      <img src="https://image.tmdb.org/t/p/original/qNBAXBIQlnOThrVvA6mA2B5ggV6.jpg" class="d-block w-100" style="height: 240px; object-fit: cover;">
    </div>
    <div class="carousel-item">
      <img src="https://image.tmdb.org/t/p/original/9Gtg2DzBhmYamXBS1hKAhiwbBKS.jpg" class="d-block w-100" style="height: 240px; object-fit: cover;">
    </div>
  </div>
</div>
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
""", height=240)

 
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Image"
    except:
        return "https://via.placeholder.com/300x450?text=No+Image"

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        names, posters = [], []
        for i in distances[1:7]:
            movie_id = movies.iloc[i[0]].movie_id
            names.append(movies.iloc[i[0]].title)
            posters.append(fetch_poster(movie_id))
        return names, posters
    except Exception as e:
        st.error(f"Recommendation failed: {e}")
        return [], []

if show_rec:
    names, posters = recommend(selected_movie)
    if names:
        st.markdown("<h4 style='margin-top: 2rem;'>📽️ Recommended Movies</h4>", unsafe_allow_html=True)
        for i in range(0, len(names), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(names):
                    with cols[j]:
                        st.image(posters[i + j], use_column_width=True)
                        st.markdown(f"<p style='text-align:center; font-size:16px; font-weight:500;'>{names[i + j]}</p>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


st.markdown("""<div class="footer">
&copy; 2025 ONESELF MOVIES. All rights reserved. Made with ❤️ by <b>Oneself Technologies</b>.
</div>""", unsafe_allow_html=True)
