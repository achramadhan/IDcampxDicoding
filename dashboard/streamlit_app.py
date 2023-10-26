import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

df = pd.read_csv("submission/hour.csv")


def kategori_jam(row):
    if 1 <= row <= 11:
        return "pagi"
    elif 12 <= row <= 14:
        return "siang"
    elif 15 <= row <= 18:
        return "sore"
    else:
        return "malam"


df['jam_kategori'] = df['hr'].apply(kategori_jam)


datetime_columns = ["dteday"]
df.sort_values(by="dteday", inplace=True)
df.reset_index(inplace=True)

for column in datetime_columns:
    df[column] = pd.to_datetime(df[column])

min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df["dteday"] >= str(start_date)) &
             (df["dteday"] <= str(end_date))]


st.title('Dashboard :blue[Sepeda]')

st.subheader('Info Tabel')

head = df.head(5)
head
grouped_jam = main_df.groupby('jam_kategori')[['casual', 'registered']].sum()


st.subheader('Riders Info')
col1, col2, col3 = st.columns(3)


with col1:
    total = main_df.cnt.sum()
    st.metric("Total Riders", value=total)
with col2:
    registered = main_df.registered.sum()
    st.metric("Registered", value=(registered))
with col3:
    casual = main_df.casual.sum()
    st.metric("Casual", value=casual)


st.subheader("Aktivitas Sepeda")

col1, col2 = st.columns(2)

with col1:
    st.line_chart(grouped_jam)

with col2:
    st.line_chart(data=main_df, x='dteday', y='cnt', color="#ffaa00")

st.bar_chart(main_df, x='weekday', y='cnt', color="#ffaa00")
st.caption(
    'X Axis menunjukkan hari, angka 0 adalah hari minggu dan angka 6 adalah hari sabtu')
