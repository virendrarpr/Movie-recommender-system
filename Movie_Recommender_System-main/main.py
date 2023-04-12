import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=6f7398664c3464c1e3457877381c51fc&language=en-US'.format(movie_id)
    )
    data = response.json()
    # st.text(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_idx]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list[1:11]:
        # fetch movie  poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)


if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    for i in range(0,10,5):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[i+0])
            st.image(recommended_movie_posters[i+0])
        with col2:
            st.text(recommended_movie_names[i+1])
            st.image(recommended_movie_posters[i+1])

        with col3:
            st.text(recommended_movie_names[i+2])
            st.image(recommended_movie_posters[i+2])
        with col4:
            st.text(recommended_movie_names[i+3])
            st.image(recommended_movie_posters[i+3])
        with col5:
            st.text(recommended_movie_names[i+4])
            st.image(recommended_movie_posters[i+4])
