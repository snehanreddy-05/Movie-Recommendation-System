import streamlit as st
import pickle
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

session.mount("https://", HTTPAdapter(max_retries=retry))

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)
st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.main {
    background-color: #0E1117;
}

h1 {
    color: #E50914;
    text-align: center;
    font-size: 55px;
}

.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 200px;
    font-size: 20px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #ff4b4b;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ---------------- #

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movies_list = movies["Movie"].values

# ---------------- TMDB API ---------------- #

api_key = "6748346fc48a05a6d569f35c79943651"
headers = {
    "User-Agent": "Mozilla/5.0"
}

trending_url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}"


@st.cache_data(ttl=3600)
def fetch_movie_details(movie_name):

    try:

        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"

        response = session.get(
    search_url,
    headers=headers,
    timeout=10
)

        data = response.json()

        results = data.get("results")

        if results and len(results) > 0:

            movie = results[0]

            poster_path = movie.get("poster_path")

            rating = movie.get("vote_average", "N/A")

            release_date = movie.get("release_date", "Unknown")

            year = release_date[:4] if release_date != "Unknown" else "N/A"

            if poster_path:

                poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path

            else:

                poster_url = "https://via.placeholder.com/300x450?text=No+Poster"

            overview = movie.get("overview", "No description available.")

            return poster_url, rating, year, overview

        return (
    "https://via.placeholder.com/300x450?text=No+Poster",
    "N/A",
    "N/A",
    "No description available."
)

    except Exception as e:
        st.error(f"TMDB Request Failed: {e}")

        return (
    "https://via.placeholder.com/300x450?text=Error",
    "N/A",
    "N/A",
    "Could not fetch description."
)

import requests

@st.cache_data(ttl=3600)
def fetch_trending_movies():
    try:
        response = session.get(
    trending_url,
    headers=headers,
    timeout=10
)
        response.raise_for_status()
        data = response.json()

        trend_names = []
        trend_posters = []

        for movie in data.get("results", [])[:5]:
            trend_names.append(movie.get("title", "Unknown"))
            poster_path = movie.get("poster_path")

            if poster_path:
                trend_posters.append("https://image.tmdb.org/t/p/w500/" + poster_path)
            else:
                trend_posters.append("https://via.placeholder.com/300x450")

        return trend_names, trend_posters

    except Exception as e:
        print("API Error:", e)
        return [], []
# ---------------- RECOMMEND FUNCTION ---------------- #

def recommend(movie):
    try:
        movie_index = movies[movies["Movie"] == movie].index[0]
        distances = similarity[movie_index]

        movie_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:6]

        recommended_movies = []
        recommended_posters = []
        recommended_ratings = []
        recommended_years = []
        recommended_overviews = []

        for i in movie_list:
            name = movies.iloc[i[0]].Movie

            poster, rating, year, overview = fetch_movie_details(name)
            recommended_overviews.append(overview)

            recommended_movies.append(name)
            recommended_posters.append(poster)
            recommended_ratings.append(rating)
            recommended_years.append(year)

        return (
    recommended_movies,
    recommended_posters,
    recommended_ratings,
    recommended_years,
    recommended_overviews
)

    except Exception as e:
        print("Recommendation Error:", e)
        return [], [], [], []


# ---------------- TITLE ---------------- #

st.markdown("""
<h1>
🎬 NETFLIX MOVIE RECOMMENDER
</h1>
""", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align:center;'>Find movies similar to your favorites 🍿</h3>",
    unsafe_allow_html=True
)

st.markdown("---")
st.write("")

# ---------------- SELECT MOVIE ---------------- #
st.subheader("🔥 Trending Movies")

trend_names, trend_posters = fetch_trending_movies()

if trend_names and trend_posters:
    cols = st.columns(5)

    for i in range(min(5, len(trend_names))):
        with cols[i]:
            st.image(trend_posters[i], width="stretch")
            st.caption(trend_names[i])
else:
    st.warning("Trending movies not available right now.")

st.markdown("---")
selected_movie = st.selectbox(
    "🔍 Search your favorite movie",
    sorted(movies_list)
)

# ---------------- BUTTON ---------------- #

if st.button("🚀 Recommend"):

    with st.spinner("Finding awesome movies for you... 😎"):

       names, posters, ratings, years, overviews = recommend(selected_movie)

    st.write("")
    st.subheader("Recommended Movies 🍿")

    cols = st.columns(5)

    for i in range(min(len(names), len(posters), len(ratings), len(years))):

       with cols[i]:

          st.image(
    posters[i],
    width="stretch"
)

          st.markdown(
            f"<h4 style='text-align:center; color:white;'>{names[i]}</h4>",
            unsafe_allow_html=True
         )

          st.write(f"⭐ Rating: {ratings[i]}")

          st.write(f"📅 Year: {years[i]}")
          st.markdown(
    f"<p style='font-size:13px; color:#cccccc;'>{overviews[i][:120]}...</p>",
    unsafe_allow_html=True
)