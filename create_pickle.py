import pandas as pd
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv("movies.csv")

# Fill empty values
movies["Genre"] = movies["Genre"].fillna("")
movies["Description"] = movies["Description"].fillna("")

# Combine columns
movies["tags"] = movies["Genre"] + " " + movies["Description"]

# Convert text into vectors
cv = CountVectorizer(max_features=5000, stop_words="english")

vectors = cv.fit_transform(movies["tags"]).toarray()

# Calculate similarity
similarity = cosine_similarity(vectors)

# Save pickle files
pickle.dump(movies, open("movies.pkl", "wb"))

pickle.dump(similarity, open("similarity.pkl", "wb"))

print("Pickle files created successfully!")