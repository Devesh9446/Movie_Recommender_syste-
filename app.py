import streamlit as st
import pickle
import pandas as pd
import requests

movie_dict=pickle.load(open('movies.pkl','rb'))
movie_list=pd.DataFrame(movie_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e82cf836032436784a2bfb687e43c527&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommender(option):
    movie_index=movie_list[movie_list['title']==option].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_posters= []
    for i in movies_list:
        recommended_movies.append((movie_list.iloc[i[0]].title))
        recommended_posters.append(fetch_poster(movie_list.iloc[i[0]].id))
    return recommended_movies,recommended_posters

st.title('Movie Recommender System')
option = st.selectbox(
    'select movie',
    movie_list['title'].values)
st.write('You selected:', option)

if st.button("Recommend", type="primary"):
    names,posters=recommender(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])