import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar el dataset NBA (ajustar la ruta si es necesario)
nba_data = pd.read_csv("datasets/nba_dataset.csv")

# Barra lateral para seleccionar el año
year_list = sorted(nba_data['year_id'].unique())
year_selected = st.sidebar.selectbox("Seleccionar Año", year_list)

# Barra lateral para seleccionar equipo
team_list = sorted(nba_data['team_id'].unique())
team_selected = st.sidebar.selectbox("Seleccionar Equipo", team_list)

# Barra lateral para seleccionar el tipo de juegos
game_type = st.sidebar.radio("Seleccionar tipo de juegos", ['Temporada Regular', 'Playoffs', 'Todos'])

# Filtrar los datos según el año, el equipo y el tipo de juego
filtered_data = nba_data[(nba_data['year_id'] == year_selected) & (nba_data['team_id'] == team_selected)]

# Filtrar según tipo de juego (si es "Playoffs", "Temporada Regular" o "Todos")
if game_type == 'Temporada Regular':
    filtered_data = filtered_data[filtered_data['is_playoffs'] == 0]
elif game_type == 'Playoffs':
    filtered_data = filtered_data[filtered_data['is_playoffs'] == 1]

# Gráfica acumulada de juegos ganados y perdidos por temporada
filtered_data['win'] = filtered_data['game_result'] == 'W'
filtered_data['loss'] = filtered_data['game_result'] == 'L'

games_won = filtered_data.groupby('year_id')['win'].cumsum()
games_lost = filtered_data.groupby('year_id')['loss'].cumsum()

# Crear la gráfica de líneas
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(filtered_data['gameorder'], games_won, label="Juegos Ganados", color='g')
ax.plot(filtered_data['gameorder'], games_lost, label="Juegos Perdidos", color='r')

ax.set_xlabel('Número de Juego')
ax.set_ylabel('Acumulado de Juegos')
ax.set_title(f'Acumulado de Juegos Ganados y Perdidos en {year_selected} para el Equipo {team_selected}')
ax.legend()

st.pyplot(fig)

# Gráfica de pastel de porcentaje de juegos ganados y perdidos
total_games = len(filtered_data)
won_games = filtered_data['win'].sum()
lost_games = filtered_data['loss'].sum()

# Crear la gráfica de pastel
fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
ax_pie.pie([won_games, lost_games], labels=['Juegos Ganados', 'Juegos Perdidos'], autopct='%1.1f%%', colors=['g', 'r'])
ax_pie.set_title(f'Porcentaje de Juegos Ganados y Perdidos en {year_selected} para el Equipo {team_selected}')

st.pyplot(fig_pie)
