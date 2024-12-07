"""Python file to serve as the frontend"""
import sys
import os

sys.path.append(os.path.abspath('.'))

from frontend.components.sidebar import sidebar
# from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import streamlit as st
import os
import requests

backend : str = os.getenv('BACKEND_HOST')

if not backend:
    backend = 'localhost'

if ('df' not in st.session_state):
    filename = 'frontend/data/moviedata.json'
    if os.path.exists(filename):
        st.session_state.df = pd.read_json(filename, orient='records', lines=True)
    else:
        url = f"http://{backend}:8000/api/v1/movies"
        payload = {}
        headers = {
        'Authorization': f'Bearer {st.session_state["OPENAI_API_KEY"]}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        st.session_state.df = pd.DataFrame(response.json())
        st.session_state.df.to_json(filename, orient='records', lines=True)

st.set_page_config(
    page_title="FIAP - MLE Tech Challenge - 2MLET",
    layout="wide"
)

sidebar()


if not st.session_state.get("open_api_key_configured"):
    st.error("Faça sua autenticação antes de usar!")
else:
    st.markdown(f"# Olá, {st.session_state.get("username")}!")

    pages = [ 
                st.Page('recommender.py', title="Recomendações", icon=":material/recommend:"), 
                st.Page('image.py', title="Pesquisar Imagens", icon=":material/image:"), 
                st.Page('settings.py', title="Preferências", icon=":material/settings:"), 
            ]

    # Set up navigation 
    pg = st.navigation(pages) 

    pg.run()
