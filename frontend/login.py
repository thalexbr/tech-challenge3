import streamlit as st
import requests

def set_open_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    st.session_state["open_api_key_configured"] = True

username = st.text_input(
    'Usuário',
    placeholder='Insira o seu nome de usuário',
    help='Este é o usuário que está cadastrado no banco de dados',
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Digite sua senha",
    help="Esta é a senha cadastrada no banco de dados",  # noqa: E501
)


if st.button('Login'):
    url = f'http://backend:8000/api/v1/token'
    print(f'URL: {url}')
    payload = { 'username' : username, 'password' : password}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    if(response.status_code != 200):
        st.error(data['detail'])
    else:
        set_open_api_key(data['access_token'])
        st.session_state["username"] = username
    st.rerun()