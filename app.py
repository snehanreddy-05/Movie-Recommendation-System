import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("movies.csv")

# Combine features
df["tags"] = df["Genre"] + " " + df["Description"]

# TF-IDF
cv = TfidfVectorizer(stop_words='english')

matrix = cv.fit_transform(df["tags"])

# Similarity matrix
similarity = cosine_similarity(matrix)
posters = {

    "Interstellar":
    "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg",

    "Inception":
    "https://upload.wikimedia.org/wikipedia/en/7/7f/Inception_ver3.jpg",

    "Doctor Strange":
    "https://upload.wikimedia.org/wikipedia/en/c/c7/Doctor_Strange_poster.jpg",

    "Titanic":
    "https://upload.wikimedia.org/wikipedia/en/2/22/Titanic_poster.jpg",

    "Notebook":
    "https://upload.wikimedia.org/wikipedia/en/8/86/Posternotebook.jpg",

    "John Wick":
    "https://upload.wikimedia.org/wikipedia/en/9/98/John_Wick_TeaserPoster.jpg",

    "Avengers":
    "https://upload.wikimedia.org/wikipedia/en/f/f9/TheAvengers2012Poster.jpg",

    "Batman":
    "https://upload.wikimedia.org/wikipedia/en/8/8a/Dark_Knight.jpg"
}

# Recommendation function
def recommend(movie_name):

    if movie_name not in df["Movie"].values:
        return []

    movie_index = df[df["Movie"] == movie_name].index[0]

    scores = list(enumerate(similarity[movie_index]))

    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommended_movies = []

    for movie in sorted_scores[1:4]:

        index = movie[0]

        similarity_score = round(movie[1] * 100, 2)

        movie_title = df.iloc[index]["Movie"]

        recommended_movies.append(
       (
        movie_title,
        similarity_score,
        posters.get(movie_title, "")
       )
        )

    return recommended_movies


# Streamlit UI
st.write("AI-powered movie recommendation app using NLP and Machine Learning.")
movie = st.selectbox(
    "Select Movie",
    df["Movie"].values
)

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