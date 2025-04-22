import streamlit as st
import streamlit.components.v1 as components
import requests
import random
import time

 
api_key = "8265bd1679663a7ea12ac168da84d2e8"

 
st.set_page_config(page_title="ONESELF MOVIES", layout="wide")

 
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .main-container {
        background: linear-gradient(120deg, #1f1c2c, #928dab);
        padding: 3rem 2rem;
        border-radius: 20px;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }
    .header-title {
        text-align: center;
        font-size: 48px;
        font-weight: 700;
        color: #F7F7F7;
        margin-bottom: 0.5rem;
    }
    .subheading {
        text-align: center;
        color: #dddddd;
        font-size: 18px;
        margin-bottom: 2rem;
    }
    .login-btn {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .stButton>button {
        font-size: 20px !important;
        padding: 12px 36px;
        border-radius: 10px;
        background-color: #FF6B6B;
        color: white;
        border: none;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FF3B3B;
    }
    .movie-strip {
        display: flex;
        overflow-x: auto;
        gap: 20px;
        padding: 10px 0;
        scroll-behavior: smooth;
        margin-bottom: 40px;
    }
    .movie-strip::-webkit-scrollbar {
        height: 10px;
    }
    .movie-strip::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
    }
    .movie-poster {
        flex: 0 0 auto;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.5);
        transition: transform 0.3s ease;
    }
    .movie-poster:hover {
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

 
def safe_fetch(url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                st.error(f"❌ Error fetching: {e}")
                return None
 
@st.cache_data
def fetch_movies_from_tmdb(category="popular", page=1):
    url = f"https://api.themoviedb.org/3/movie/{category}?api_key={api_key}&language=en-US&page={page}"
    data = safe_fetch(url)
    return data.get("results", []) if data else []


def display_movie_row(movies, title):
    st.markdown(f"### 🎥 {title}")
    posters = ""
    for movie in movies:
        poster_path = movie.get("poster_path")
        if poster_path:
            posters += f"""
                <img src="https://image.tmdb.org/t/p/w500{poster_path}" 
                class="movie-poster" height="300">
            """
    if posters:
        html_code = f"<div class='movie-strip'>{posters}</div>"
        components.html(html_code, height=320)
    else:
        st.warning(f"No posters available for {title}.")


st.markdown('<div class="main-container">', unsafe_allow_html=True)


st.markdown('<div class="header-title">🎬 Welcome to ONESELF MOVIES</div>', unsafe_allow_html=True)
st.markdown('<div class="subheading">Your personal AI-powered movie recommendation platform</div>', unsafe_allow_html=True)


st.markdown('<div class="login-btn">', unsafe_allow_html=True)
if st.button("🚀 PLEASE LOGIN TO WATCH MOVIES"):
    st.switch_page("pages/login.py")
st.markdown('</div>', unsafe_allow_html=True)


popular_movies = fetch_movies_from_tmdb("popular", random.randint(1, 5))
upcoming_movies = fetch_movies_from_tmdb("upcoming", random.randint(1, 5))
top_rated_movies = fetch_movies_from_tmdb("top_rated", random.randint(1, 5))

display_movie_row(popular_movies[:12], "🔥 Trending Now")
display_movie_row(upcoming_movies[:12], "🎞️ Coming Soon")
display_movie_row(top_rated_movies[:12], "🏆 Top Rated")


st.markdown("### 📽️ About ONESELF MOVIES")
st.markdown("""
Welcome to **ONESELF MOVIES** – a cutting-edge movie recommendation platform built to help you discover films you'll truly love.  
Whether you're into action-packed thrillers, heartwarming dramas, or mind-bending sci-fi, we've got something for you.

ONESELF MOVIES is a personalized movie recommendation platform powered by intelligent algorithms and real-time data from TMDB.  
Smart, simple, and engaging — ONESELF MOVIES brings the best suggestions straight to your screen.
""")


st.markdown("### 📞 Contact Us")
st.markdown("""
📞 Contact No: [+918007029012](tel:+918007029012)  
📧 Email: [info.oneselftech@gmail.com](mailto:info.oneselftech@gmail.com)  
🌐 Website: [www.onselfmovies.in](https://www.onselfmovies.in)
""")


st.markdown("""
<div style='text-align: center; color: #bbb; margin-top: 2rem; font-size: 14px;'>
&copy; 2025 ONESELF MOVIES. Made with ❤️ by <b>Oneself Technologies</b>.
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
