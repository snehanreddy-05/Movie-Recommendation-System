import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read dataset
df = pd.read_csv("movies.csv")

# Convert text into numbers
cv = CountVectorizer()

matrix = cv.fit_transform(df["Description"])

# Calculate similarity
similarity = cosine_similarity(matrix)

# Recommendation function
def recommend(movie_name):

    if movie_name not in df["Movie"].values:
        return "Movie not found"

    # Find movie index
    movie_index = df[df["Movie"] == movie_name].index[0]

    # Similarity scores
    scores = list(enumerate(similarity[movie_index]))

    # Sort scores
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    print("\nRecommended Movies:\n")

    # Show top 3 recommendations
    for movie in sorted_scores[1:4]:

        index = movie[0]

        similarity_score = round(movie[1] * 100, 2)

        print(df.iloc[index]["Movie"], "-", similarity_score, "% similar")

# User input
movie = input("Enter movie name: ")

recommend(movie)