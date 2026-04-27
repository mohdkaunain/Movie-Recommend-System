import streamlit as st
import pandas as pd
import pickle
import requests

API_KEY = "b15cd75df9b36428294e47fe0ca8dcd1"

# Fetch poster + rating safely
def fetch_movie(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        poster = data.get("poster_path")
        rating = round(data.get("vote_average", 0), 1)

        poster_url = (
            f"https://image.tmdb.org/t/p/w500/{poster}"
            if poster
            else "https://via.placeholder.com/500x750?text=No+Poster"
        )

        return poster_url, rating

    except:
        return "https://via.placeholder.com/500x750?text=Error", 0.0


# Recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names, posters, ratings = [], [], []

    for i in distances:
        movie_id = movies.iloc[i[0]].movie_id
        poster, rating = fetch_movie(movie_id)

        names.append(movies.iloc[i[0]].title)
        posters.append(poster)
        ratings.append(rating)

    return names, posters, ratings


# Load files
movies = pd.DataFrame(pickle.load(open('movie_dict.pkl', 'rb')))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# UI
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

if st.button("Show Recommendation"):
    names, posters, ratings = recommend(selected_movie)

    cols = st.columns(5)

    for col, name, poster, rating in zip(cols, names, posters, ratings):
        with col:
            st.image(poster)
            st.caption(name)
            st.caption(f"⭐ {rating}/10")