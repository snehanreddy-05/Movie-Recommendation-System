import streamlit as st
import pandas as pd
import requests

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nltk.stem.porter import PorterStemmer

# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("Movie Recommendation System 🎬")

st.write(
    "AI-powered movie recommendation app using NLP and Machine Learning."
)

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("movies.csv")
st.write(df.head())

st.write(df.columns)

# -----------------------------
# NLP STEMMING
# -----------------------------

ps = PorterStemmer()


def stem(text):

    words = text.split()

    stemmed_words = []

    for word in words:

        stemmed_words.append(ps.stem(word))

    return " ".join(stemmed_words)


# -----------------------------
# CREATE TAGS
# -----------------------------

df["tags"] = df["Genre"] + " " + df["Description"]

df["tags"] = df["tags"].apply(stem)

# -----------------------------
# TF-IDF
# -----------------------------

tfidf = TfidfVectorizer(stop_words="english")

matrix = tfidf.fit_transform(df["tags"])

# -----------------------------
# SIMILARITY
# -----------------------------

similarity = cosine_similarity(matrix)

# -----------------------------
# FETCH POSTER FROM TMDB
# -----------------------------


def fetch_poster(movie_name):

    try:

        api_key = "6748346fc48a05a6d569f35c79943651"

        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        data = response.json()

        if data["results"]:

            poster_path = data["results"][0].get("poster_path")

            if poster_path:

                return (
                    "https://image.tmdb.org/t/p/w500/"
                    + poster_path
                )

    except Exception as e:

        print("TMDB Error:", e)

    return ""


# -----------------------------
# RECOMMEND FUNCTION
# -----------------------------


def recommend(movie_name):

    movie_index = df[df["Movie"] == movie_name].index[0]

    scores = list(enumerate(similarity[movie_index]))

    sorted_scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommended_movies = []

    for item in sorted_scores[1:4]:

        index = item[0]

        similarity_score = round(item[1] * 100, 2)

        movie_title = df.iloc[index]["Movie"]

        poster = ""

        recommended_movies.append(
            (
                movie_title,
                similarity_score,
                poster
            )
        )

    return recommended_movies


# -----------------------------
# SELECT MOVIE
# -----------------------------

movie = st.selectbox(
    "Select Movie",
    df["Movie"].tolist()
)

# -----------------------------
# BUTTON
# -----------------------------

if st.button("Recommend"):

    recommendations = recommend(movie)

    st.success("Top Recommendations")

    cols = st.columns(3)

    for idx, (movie, score, poster) in enumerate(recommendations):

        with cols[idx]:

            if poster:
                st.image(poster, width=150)

            st.write(movie)

            st.write(f"{score}% similar")