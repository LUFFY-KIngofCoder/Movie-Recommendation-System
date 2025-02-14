import streamlit as st
import pickle
import requests
import os
import gdown

fileid = "1R7cPEZ2H7jCKIbT3qmJV2n5FhG_xaRH8"
savepath = "similarity.pkl"

if not os.path.exists(savepath):
    gdown.download(id=fileid, output=savepath, quiet=False)
    
# Set up page title
st.title("Movie Recommendation System")

# Load movie data and similarity matrix
new_df = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Extract the list of movie titles
movie_list = new_df.title.values


# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMGI1ZmU4Mjk2NmY5Nzk3ZDM2ODhjYzBiZTIwMjE1NyIsIm5iZiI6MTczODI1NDQzOS40MDgsInN1YiI6IjY3OWJhODY3YjAwZDNiYWQ5MmJkODlmZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.D6gTuVG_5C6etdkQe4cAqz1RGNwps2S6uSEyCwRLp3I"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    poster_path = data['poster_path']
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"


# Function to recommend movies based on the selected movie
def recommendation(movie):
    index = new_df[new_df["title"] == movie].index[0]
    distances = similarity[index]
    top5 = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommended_names = []
    recommended_posters = []

    for i in top5:
        movie_id = new_df.iloc[i[0]].movie_id
        recommended_posters.append(fetch_poster(movie_id))
        recommended_names.append(new_df.iloc[i[0]].title)

    return recommended_posters, recommended_names


# User input: Select a movie from the list
option = st.selectbox(
    "Search name of the movie",
    movie_list,
    placeholder="Select a movie...",
)

# Button to trigger recommendations
button = st.button("Get Recommendations")

if button:
    # Layout for displaying recommended movies
    col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment="bottom")
    cols = [col1, col2, col3, col4, col5]
    recommended_posters, recommended_names = recommendation(option)

    # Display recommended movies
    for i in range(5):
        with cols[i]:
            st.text(recommended_names[i])
            st.image(recommended_posters[i])

# Layout for displaying random movies
cl1, cl2, cl3, cl4, cl5 = st.columns(5, vertical_alignment="top")
columns_random = [cl1, cl2, cl3, cl4, cl5]

for i in range(2):
    rand_movies = new_df["movie_id"].sample(5).values
    for j in range(5):
        with columns_random[j]:
            st.text(new_df[new_df["movie_id"] == rand_movies[j]].title.values[0])
            st.image(fetch_poster(rand_movies[j]))
