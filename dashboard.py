import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard Barbearia", layout="wide")

np.random.seed(42)

# Generate one year of data (2025)
dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")

appointments = []

for date in dates:
    month = date.month

    # Seasonal adjustment
    if month in [1, 2]:  # Janeiro/Fevereiro - movimento menor
        weekday_range = (2, 6)
        weekend_range = (6, 12)
    elif month in [7, 12]:  # Julho e Dezembro - mais movimento
        weekday_range = (5, 11)
        weekend_range = (12, 22)
    else:  # Demais meses - normal
        weekday_range = (3, 8)
        weekend_range = (8, 18)

    if date.weekday() == 6:  # Domingo fechado
        appointments.append(0)
    elif date.weekday() in [4, 5]:  # Sexta e Sábado
        appointments.append(np.random.randint(*weekend_range))
    else:  # Segunda a Quinta
        appointments.append(np.random.randint(*weekday_range))

df = pd.DataFrame({
    "Day": dates.day,
    "Month": dates.month,
    "Week": ((dates.dayofyear - 1) // 7 + 1),
    "Weekday": dates.day_name(locale="pt_BR"),
    "Appointments": appointments,
    "Date": dates
})

# Metrics
total_appointments = df["Appointments"].sum()
daily_avg = int(round(df["Appointments"].mean()))
weekly_avg = int(round(df.groupby("Week")["Appointments"].sum().mean()))
busiest_day = df.loc[df["Appointments"].idxmax()]
busiest_weekday = df.groupby("Weekday")["Appointments"].mean().idxmax()

# Header
st.markdown("<h1 style='text-align: center; color:#FFFFFF;'>Dashboard Barbearia</h1>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de atendimentos", f"{total_appointments}")
col2.metric("Média diária", f"{daily_avg}")
col3.metric("Média semanal", f"{weekly_avg}")
col4.metric("Dia mais movimentado", f"{busiest_day['Date'].strftime('%d/%m/%Y')} ({busiest_day['Weekday']}) - {busiest_day['Appointments']}")
col5.metric("Dia da semana mais movimentado", f"{busiest_weekday}")

# View selector
view = st.radio("", ["Dia", "Semana", "Mês"], horizontal=True, label_visibility="collapsed")

if view == "Dia":
    plot_df = df.copy()
    plot_df["Tooltip"] = plot_df.apply(
        lambda row: f"{row['Date'].strftime('%d/%m/%Y')} ({row['Weekday']})<br>Atendimentos: {row['Appointments']}", axis=1
    )
    x_col = "Date"
    y_col = "Appointments"
    hover_col = "Tooltip"
    title = "Atendimentos por dia"
    x_label = "Dias"
elif view == "Semana":
    plot_df = df.groupby("Week")["Appointments"].sum().reset_index()
    plot_df["Tooltip"] = plot_df.apply(lambda row: f"Semana {row['Week']}<br>Atendimentos: {row['Appointments']}", axis=1)
    plot_df["Week"] = plot_df["Week"].apply(lambda x: f"Semana {x}")
    x_col = "Week"
    y_col = "Appointments"
    hover_col = "Tooltip"
    title = "Atendimentos por semana"
    x_label = "Semanas"
elif view == "Mês":
    plot_df = df.groupby("Month")["Appointments"].sum().reset_index()
    plot_df["Tooltip"] = plot_df.apply(lambda row: f"Mês {row['Month']}<br>Atendimentos: {row['Appointments']}", axis=1)
    plot_df["Month"] = plot_df["Month"].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%B'))
    x_col = "Month"
    y_col = "Appointments"
    hover_col = "Tooltip"
    title = "Atendimentos por mês"
    x_label = "Meses"

# Só um gráfico agora
fig_line = px.line(
    plot_df,
    x=x_col,
    y=y_col,
    title=title,
    hover_data={hover_col: True},
    labels={y_col: "Atendimentos"},
)

fig_line.update_traces(
    line=dict(color="#9467bd", width=3, shape='spline'),
    mode="lines+markers",
    marker=dict(size=8, color="#FFFFFF", line=dict(width=2, color="#9467bd")),
    hovertemplate='%{customdata[0]}<extra></extra>'
)

fig_line.update_layout(
    template="plotly_dark",
    title=dict(text=title, x=0.5, font=dict(size=22, color="white")),
    font=dict(size=14, color="white"),
    margin=dict(l=50, r=50, t=80, b=50),
    xaxis=dict(showgrid=False, linecolor="#555", tickfont=dict(size=12, color="white"),
               title=dict(text=x_label, font=dict(size=14, color="white"))),
    yaxis=dict(showgrid=True, gridcolor="#333", zeroline=False, tickfont=dict(size=12, color="white"),
               title=dict(text="Atendimentos", font=dict(size=14, color="white")))
)

st.plotly_chart(fig_line, use_container_width=True)
