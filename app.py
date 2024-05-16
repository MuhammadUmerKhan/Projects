import streamlit as st
import pandas as pd
import requests
import pickle

movie_dict = pickle.load(open('./pickle files/movie_list.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('./pickle files/similarity.pkl', 'rb'))

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []

    for i in distances[1:6]:
        
        recommended_movie_names.append(movies.iloc[i[0]].title)
    
    return recommended_movie_names

st.header('Movie Recommender System')

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    for movie in recommendations:
        st.write(movie)
