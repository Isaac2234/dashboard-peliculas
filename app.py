import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

movies_data = pd.read_csv("datasets/movies.csv")

# valores unicos para cada componente en la barra lateral
score_rating = movies_data['score'].unique().tolist()
genre_list = movies_data['genre'].unique().tolist()
year_list = movies_data['year'].unique().tolist()

with st.sidebar:
    st.write("Seleccionar un valor para el score de la pelicula \
            dentro del rango del slider")
    
    # slider para score de usuario
    new_score_rating = st.slider(
            label = "Seleccionar valor:",
            min_value = 1.0,
            max_value = 10.0,
            value = (3.0,4.0))
    
    # widget de multiseleccion para el genero
    new_genre_list = st.multiselect(
            'Seleccionar genero:',
            genre_list, default = ['Animation', 'Horror',  'Fantasy', 'Romance'])

    # caja de seleccion para el año
    year = st.selectbox('Seleccionar año', year_list, 0)

# filtro para los scores del slider
score_info = (movies_data['score'].between(*new_score_rating))

# filtro para el genero y año
new_genre_year = (movies_data['genre'].isin(new_genre_list)) & (movies_data['year'] == year)

# gráficas
col1, col2 = st.columns([2,3])
with col1:
    st.write("""#### Peliculas filtradas por año y genero """)

    dataframe_genre_year = movies_data[new_genre_year].groupby(['name',  'genre'])['year'].sum()
    dataframe_genre_year = dataframe_genre_year.reset_index()
    
    st.dataframe(dataframe_genre_year, width = 400)

with col2:
    st.write("""#### Year vs. Budget """)
    
    df = movies_data[score_info]

    df_score = df.groupby("year")["budget"].mean()
    df_score = df_score.reset_index().fillna(0)
    
    fig = plt.figure(figsize = (12, 10))
    
    plt.plot(df_score["year"], df_score["budget"], 'r-')
    plt.xlabel('year')
    plt.ylabel('budget')
    
    st.pyplot(fig)
