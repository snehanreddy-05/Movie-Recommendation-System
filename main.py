import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read dataset
df = pd.read_csv("movies.csv")

# Combine features
df["tags"] = df["Genre"] + " " + df["Description"]

# Convert text to vectors
cv = TfidfVectorizer(stop_words='english')

matrix = cv.fit_transform(df["tags"])

# Similarity matrix
similarity = cosine_similarity(matrix)

# Recommendation function
def recommend(movie_name):

    if movie_name not in df["Movie"].values:
        return "Movie not found"

    movie_index = df[df["Movie"] == movie_name].index[0]

    scores = list(enumerate(similarity[movie_index]))

    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    print("\nRecommended Movies:\n")

    for movie in sorted_scores[1:4]:

        index = movie[0]

        score = round(movie[1] * 100, 2)

        print(df.iloc[index]["Movie"], "-", score, "% similar")

# User input
movie = input("Enter movie name: ")

recommend(movie)