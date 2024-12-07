import streamlit as st

def unset_open_api_key():
    st.session_state["OPENAI_API_KEY"] = ''
    st.session_state["open_api_key_configured"] = False


def sidebar():
    with st.sidebar:
        if not st.session_state.get("open_api_key_configured"):
            pages = [ 
                        st.Page('login.py', title="Login", icon=":material/recommend:"), 
                    ]
            # Set up navigation 
            pg = st.navigation(pages) 

            pg.run()
        
        else:
            if st.button('Desconectar'):
                unset_open_api_key()
                st.rerun()

        st.markdown("---")
        st.markdown("# Sobre ")
        st.markdown(
            """📖 Tech Challenge 
Machine Learning Engineering"""
        )
        st.markdown("Turma 2")
        st.markdown("""### Integrantes do grupo: 
- Alecrim 
- Diogo Padilha 
- Felipe Bizzo 
- Gabriel Ronny 
- Thales Gomes""")
        st.markdown("---")
