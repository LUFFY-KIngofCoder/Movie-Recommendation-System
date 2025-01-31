import streamlit as st
import pickle
import requests
from streamlit import columns

st.title("Movie Recommendation System")

new_df = pickle.load(open("movies.pkl" ,"rb"))
similarity = pickle.load(open("similarity.pkl" ,"rb"))

movie_list = new_df.title.values

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

def recommendation(movie):
    index = new_df[new_df["title"] == movie].index[0]
    distances = similarity[index]
    top5 = sorted(list(enumerate(distances)), key = lambda x: x[1],reverse=True)[1:6]

    recommended_name = []
    recommended_poster = []
    for i in top5:
        movie_id = new_df.iloc[i[0]].movie_id
        recommended_poster.append(fetch_poster(movie_id))
        recommended_name.append(new_df.iloc[i[0]].title)

    return recommended_poster,recommended_name


option = st.selectbox(
    "Search name of the movie",
    movie_list,
    index=None,
    placeholder="Select contact method...",
)

button = st.button("Recommendations")

if button:
    col1, col2, col3, col4, col5 = st.columns(5 , vertical_alignment="bottom")
    col = [col1, col2, col3, col4, col5]
    recommended_poster,recommended_name = recommendation(option)

    for i in range(5):
        with col[i]:
            st.text(recommended_name[i])
            st.image(recommended_poster[i])





cl1 , cl2 , cl3 , cl4, cl5 = st.columns(5, vertical_alignment="top")
columnss = [cl1 , cl2 , cl3 , cl4, cl5]
for i in range(2):
    rand_movies = new_df["movie_id"].sample(5).values
    for i in range(5):
        with columnss[i]:
            st.text(new_df[new_df["movie_id"] == rand_movies[i]].title.values[0])
            st.image(fetch_poster(rand_movies[i]))
