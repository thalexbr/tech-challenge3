import streamlit as st
import pandas as pd 

df = st.session_state.df



lista_completa, selecao = st.tabs(["Todos os filmes", "Filmes selecionados"])


with lista_completa:
    filtro = st.text_input("Filtrar filmes")

    if filtro:
        mask = st.session_state.df.map(lambda x: filtro.lower() in str(x).lower()).any(axis=1)
        df = st.session_state.df[mask]

    disponiveis = st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
    )

    if st.button('Adicionar à lista'):
        filme = disponiveis.selection.rows
        if 'filmes_selecionados' in st.session_state:
            df_original = st.session_state.filmes_selecionados.copy()
            frames = [ df_original, df.iloc[filme]]
            combined_df = pd.concat(frames)
            st.session_state.filmes_selecionados = combined_df.drop_duplicates().sort_values(by='id')
        else:
            st.session_state.filmes_selecionados = df.iloc[filme]

with selecao:
    # st.header("Selected members")
    if 'filmes_selecionados' in st.session_state:
        selecionados = st.dataframe(
            st.session_state.filmes_selecionados,            
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
        )

        if(not st.session_state.filmes_selecionados.empty):
            if st.button('Remover da lista'):
                df_original = st.session_state.filmes_selecionados.copy()

                para_remover = df_original.iloc[selecionados.selection.rows]

                ids = para_remover['id'].to_list()

                df_modificado = df_original[~df_original['id'].isin(ids)]
                
                st.session_state.filmes_selecionados = df_modificado
                st.rerun()



