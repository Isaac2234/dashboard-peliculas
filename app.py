import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("datasets/nba_all_elo.csv")

# Asegurarse de que las fechas estén en formato datetime
df["date_game"] = pd.to_datetime(df["date_game"])


st.title("Dashboard de Juegos NBA")


with st.sidebar:
    st.header("Filtros")

    
    year = st.selectbox("Selecciona el año", sorted(df["year_id"].unique(), reverse=True))

    
    equipos_disponibles = df[df["year_id"] == year]["team_id"].unique()
    equipo = st.selectbox("Selecciona el equipo", sorted(equipos_disponibles))

    
    tipo_juego = st.pills("Tipo de juego", ["Temporada Regular", "Playoffs", "Ambos"])


if tipo_juego == "Temporada Regular":
    df_filtrado = df[(df["year_id"] == year) & (df["team_id"] == equipo) & (df["is_playoffs"] == 0)]
elif tipo_juego == "Playoffs":
    df_filtrado = df[(df["year_id"] == year) & (df["team_id"] == equipo) & (df["is_playoffs"] == 1)]
else:
    df_filtrado = df[(df["year_id"] == year) & (df["team_id"] == equipo)]


df_filtrado = df_filtrado.sort_values("date_game")


df_filtrado["Wins"] = (df_filtrado["game_result"] == "W").cumsum()
df_filtrado["Losses"] = (df_filtrado["game_result"] == "L").cumsum()

# --- Gráfica de líneas (por fecha) ---
fig_linea, ax = plt.subplots()

if tipo_juego == "Ambos":
    reg = df_filtrado[df_filtrado["is_playoffs"] == 0]
    po = df_filtrado[df_filtrado["is_playoffs"] == 1]

    ax.plot(reg["date_game"], reg["Wins"], label="Ganados (Reg)", color="green", marker="o")
    ax.plot(reg["date_game"], reg["Losses"], label="Perdidos (Reg)", color="red", marker="o")

    ax.plot(po["date_game"], po["Wins"], label="Ganados (Playoffs)", color="darkgreen", linestyle="--", marker="x")
    ax.plot(po["date_game"], po["Losses"], label="Perdidos (Playoffs)", color="darkred", linestyle="--", marker="x")
else:
    ax.plot(df_filtrado["date_game"], df_filtrado["Wins"], label="Ganados", color="green", marker="o")
    ax.plot(df_filtrado["date_game"], df_filtrado["Losses"], label="Perdidos", color="red", marker="o")

ax.set_title(f"Acumulado de Juegos Ganados y Perdidos ({tipo_juego})")
ax.set_xlabel("Fecha del Juego")
ax.set_ylabel("Cantidad")
ax.legend()
ax.grid(True)
fig_linea.autofmt_xdate()  

st.pyplot(fig_linea)

# --- Gráfica de pastel ---
total_wins = (df_filtrado["game_result"] == "W").sum()
total_losses = (df_filtrado["game_result"] == "L").sum()

fig_pie, ax_pie = plt.subplots()
ax_pie.pie([total_wins, total_losses], labels=["Ganados", "Perdidos"], autopct='%1.1f%%',
           colors=["green", "red"], startangle=90)
ax_pie.set_title(f"Porcentaje de Juegos Ganados y Perdidos ({tipo_juego})")

st.pyplot(fig_pie)