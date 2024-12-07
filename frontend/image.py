
import streamlit as st
import requests

movieId = st.text_input(
        'ID do Filme',
        placeholder='Insira o ID do filme',
        key='movieId',
        help='Usar o ID referente à base do IMDB',
    
    )
if st.button('Get Movie Image'):
    if not st.session_state.get("open_api_key_configured"):
        st.error("Please configure your API Keys!")
    
    url = f"http://localhost:8000/api/v1/movies/image?movieId={movieId}"

    st.image(url)
