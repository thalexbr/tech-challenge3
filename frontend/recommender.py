import pandas as pd
import streamlit as st
from numpy import random

def getImages(movieList: list):
    
    # payload = {}
    # headers = {
    # 'Authorization': f'Bearer {st.session_state["OPENAI_API_KEY"]}'
    # }

    moviePosters = []
    movieTitles = []

    for movieId in movieList:
        url = f"http://localhost:8000/api/v1/movies/image?movieId={movieId}"
        st.write(url)
        moviePosters.append(url)
        movieTitles.append(st.session_state.df.loc[st.session_state.df['id'] == movieId, 'title'].values[0])

    
    data_df = pd.DataFrame(
        {
            "movieIds": movieList,
            "moviePosters": moviePosters,
            "movieTitle": movieTitles,
        }
    )

    st.data_editor(
        data_df,
        column_config={
            "moviePosters": st.column_config.ImageColumn(
                "Preview Image", help="Movie Poster"
            )
        },
        hide_index=True,
    )

st.title('Filmes Recomendados 🎞️📽️🎬')

if 'df' not in st.session_state:
    st.session_state.df = None

if st.button('Obter recomendações'):
    if not st.session_state.get("open_api_key_configured"):
        st.error("Please configure your API Keys!")
    else:
        st.write('Aqui estão suas recomendações')
        movieIds = st.session_state.df['id'].to_list()
        movieNames = st.session_state.df['title'].to_list()
        random_movie =  random.randint(len(movieIds)-1)
        print(f'ID: {movieIds[random_movie]} :: Filme: {movieNames[random_movie]}')
        print(len(movieIds))
        filmes_aleatorios = st.session_state.df['id'].sample(3).tolist()    
        print(filmes_aleatorios)
        getImages(filmes_aleatorios)
