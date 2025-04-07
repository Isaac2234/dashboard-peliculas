import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
nba_data = pd.read_csv("datasets/nba_all_elo.csv")

# Título de la app
st.title("🏀 Dashboard de la NBA")

# Barra lateral con selectores
st.sidebar.header("🎯 Filtros")

# Selector de año
years = sorted(nba_data['year_id'].unique())
selected_year = st.sidebar.selectbox("Selecciona un año", years, index=0)

# Selector de equipo
teams = sorted(nba_data['team_id'].unique())
selected_team = st.sidebar.selectbox("Selecciona un equipo", teams, index=0)

# Selector de tipo de juego
tipo_juego = st.sidebar.radio(
    "Selecciona tipo de juegos",
    ("Temporada regular", "Playoffs", "Ambos"),
    horizontal=True
)

# Aplicar filtros
df_filtered = nba_data[
    (nba_data['year_id'] == selected_year) &
    (nba_data['team_id'] == selected_team)
]

if tipo_juego == "Temporada regular":
    df_filtered = df_filtered[df_filtered['is_playoffs'] == 0]
elif tipo_juego == "Playoffs":
    df_filtered = df_filtered[df_filtered['is_playoffs'] == 1]

# Verificamos si hay datos
if df_filtered.empty:
    st.warning("⚠️ No hay datos disponibles para los filtros seleccionados.")
else:
    # Ordenar por número de juego en la temporada
    df_filtered = df_filtered.sort_values(by='seasongame')

    # Crear columnas para acumulado
    df_filtered['Ganados'] = (df_filtered['game_result'] == 'W').cumsum()
    df_filtered['Perdidos'] = (df_filtered['game_result'] == 'L').cumsum()

    # Gráfica de líneas
    st.subheader(f"📈 Juegos Ganados vs Perdidos - {selected_team} en {selected_year}")
    fig_line, ax = plt.subplots()
    ax.plot(df_filtered['seasongame'], df_filtered['Ganados'], label='Ganados', color='green')
    ax.plot(df_filtered['seasongame'], df_filtered['Perdidos'], label='Perdidos', color='red')
    ax.set_xlabel("Juego de la temporada")
    ax.set_ylabel("Acumulado")
    ax.set_title(f"Ganados vs Perdidos - {selected_team}")
    ax.legend()
    st.pyplot(fig_line)

    # Gráfica de pastel
    st.subheader("📊 Porcentaje de Juegos Ganados vs Perdidos")

    won_games = (df_filtered['game_result'] == 'W').sum()
    lost_games = (df_filtered['game_result'] == 'L').sum()
    total_games = won_games + lost_games

    if total_games > 0:
        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(
            [won_games, lost_games],
            labels=['Ganados', 'Perdidos'],
            autopct='%1.1f%%',
            colors=['green', 'red']
        )
        ax_pie.set_title("Distribución de resultados")
        st.pyplot(fig_pie)
    else:
        st.warning("No hay datos suficientes para mostrar la gráfica de pastel.")
