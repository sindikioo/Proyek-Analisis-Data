import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

st.set_page_config(page_title= "Bike Sharing ", page_icon="🚲", layout="wide")

st.title("Bike Sharing Dashboard 🚲")

try:
    data = pd.read_csv('D:/submission/dashboard/dataset_proyek.csv')
except FileNotFoundError:
    st.error('Data not found. Please upload data first.')

def create_yearly_rentals_df(df):
    yearly_rentals_df = df.groupby('yr')['cnt'].sum().reset_index()
    yearly_rentals_df.rename(columns={'cnt': 'total_rentals'}, inplace=True)
    return yearly_rentals_df
yearly_rentals_df = create_yearly_rentals_df(data)
print(yearly_rentals_df)

def create_monthly_rentals_df(df):
    monthly_rentals_df = df.groupby('mnth')['cnt'].sum().reset_index()
    monthly_rentals_df.rename(columns={'cnt': 'total_rentals'}, inplace=True)
    return monthly_rentals_df
monthly_rentals_df = create_monthly_rentals_df(data)
print(monthly_rentals_df)

def create_season_rentals_df(df):
    season_rentals_df = df.groupby('season')['cnt'].agg(['min','max']).reset_index()
    return season_rentals_df
season_rentals_df = create_season_rentals_df(data)
print(season_rentals_df)

def create_daily_rentals_df(df):
    daily_rentals_df = df.groupby('weekday')['cnt'].agg(['min', 'max']).reset_index()
    return daily_rentals_df
daily_rentals_df = create_daily_rentals_df(data)
print(daily_rentals_df)

def create_hourly_rentals_df(df):
    hourly_rentals = df.groupby('hr')['cnt'].sum().reset_index()
    hourly_rentals.rename(columns={'cnt': 'total_rentals'}, inplace=True)
    max_hour = hourly_rentals.loc[hourly_rentals['total_rentals'].idxmax()]['hr']
    min_hour = hourly_rentals.loc[hourly_rentals['total_rentals'].idxmin()]['hr']
    return hourly_rentals, max_hour + 1, min_hour + 1
hourly_rentals = create_hourly_rentals_df(data)
print(hourly_rentals) 

def create_correlation_matrix(df):
    correlation_matrix = df[['temp', 'hum', 'windspeed', 'cnt']].corr()
    return correlation_matrix
correlation_matrix = create_correlation_matrix(data)
print(correlation_matrix)

# Menambahkan sidebar
with st.sidebar:
    st.image("https://github.com/sindikioo/gambar/blob/main/Rentals.png?raw=true")

# Menambahkan tab
tab1, tab2 = st.tabs(["Berdasarkan Rentang Waktu", "Berdasarkan Musim"])
 
with tab1:
#Membuat visualisasi jumlah penyewa dalam tahun
    yearly_rentals_df = data[['yr', 'cnt']].groupby('yr').sum().reset_index()
    yearly_rentals = {'2011': yearly_rentals_df['cnt'][0], '2012': yearly_rentals_df['cnt'][1]}
    # Fungsi untuk membuat plot pie chart
    def plot_pie_chart(df):
        years = df['yr']
        rentals = df['cnt']
        plt.figure(figsize=(8, 8))
        plt.pie(rentals, labels=yearly_rentals, autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'skyblue'])
        plt.title('Distribusi Jumlah Penyewa Sepeda Tiap Tahun')
        st.pyplot(plt)
    
    st.subheader('Visualisasi Jumlah Penyewa Sepeda')
    plot_pie_chart(yearly_rentals_df)
    
#Membuat visualisasi tren penyewa sepeda dalam bulan
monthly_rentals_df = data[['mnth', 'cnt']].groupby('mnth').sum().reset_index()
# Fungsi untuk membuat plot bar
def plot_bar_chart(df):
    plt.figure(figsize=(12, 6))
    plt.bar(df['mnth'], df['cnt'], color='lightcoral')
    plt.title('Distribusi Jumlah Penyewa Sepeda Tiap Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penyewa')
    plt.xticks(ticks=df['mnth'], labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
    st.pyplot(plt)# Fungsi untuk membuat scatter plot
def plot_scatter(x_col, y_col, title, xlabel, ylabel):
    plt.figure(figsize=(8, 6))
    plt.scatter(data[x_col], data[y_col])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    st.pyplot(plt)
plot_bar_chart(monthly_rentals_df)

# menampilkan visualisasi tren penyewa sepeda dalam hari
weekday_rentals_df = data.groupby('weekday')['cnt'].agg(['min', 'max']).reset_index()
# Fungsi untuk membuat grafik batang horizontal
def plot_weekday_rentals(df):
    plt.figure(figsize=(20, 12))
    plt.barh(df['weekday'], df['min'], height=0.3, label='Min Rentals', color='lightcoral', align='center')
    plt.barh(df['weekday'], df['max'], height=0.3, label='Max Rentals', color='skyblue', left=df['min'], align='center')

    # Menambahkan nilai minimum dan maksimum di samping setiap bar
    for i, row in df.iterrows():
        plt.text(row['min'] - 10, i, str(row['min']), color='black', va='center')
        plt.text(row['min'] + row['max'] + 5, i, str(row['max']), color='black', va='center')

    plt.title('Tren Penyewa Sepeda Berdasarkan Hari')
    plt.xlabel('Jumlah Penyewa Sepeda')
    plt.ylabel('Hari')
    plt.yticks(ticks=df['weekday'], labels=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
    plt.legend()
    st.pyplot(plt)

st.subheader('Distribusi Penyewa Sepeda Berdasarkan Hari')
plot_weekday_rentals(weekday_rentals_df)

with tab2:
    # Membuat visualisasi hubungan faktor lingkungan dengan penyewa
    st.subheader('Analisis Hubungan Faktor Lingkungan dengan Jumlah Penyewa')
    variable = st.selectbox('Pilih Variabel', ['temperature', 'humidity', 'windspeed'])
    # Menampilkan plot berdasarkan pilihan
    if variable == 'temp':
        plot_scatter('temp', 'cnt', 'Hubungan Suhu dengan Jumlah Penyewa', 'Suhu', 'Jumlah Penyewa')
    elif variable == 'hum':
        plot_scatter('hum', 'cnt', 'Hubungan Kelembapan dengan Jumlah Penyewa', 'Kelembapan', 'Jumlah Penyewa')
    else:
        plot_scatter('windspeed', 'cnt', 'Hubungan Kecepatan Angin dengan Jumlah Penyewa', 'Kecepatan Angin', 'Jumlah Penyewa')

    #Membuat visualisasi penyewa berdasarkan musim 
    season_rentals_df = data.groupby('season')['cnt'].agg(['min', 'max']).reset_index()
    # Fungsi untuk membuat grafik batang vertikal
    def plot_season_rentals_vertical(df):
        plt.figure(figsize=(16, 8))
        x = season_rentals_df.index
        plt.bar(x - 0.2, df['min'], width=0.4, label='Min Rentals', color='lightcoral')
        plt.bar(x + 0.2, df['max'], width=0.4, label='Max Rentals', color='skyblue')

        # Menambahkan nilai minimum dan maksimum di atas setiap batang
        for i, row in df.iterrows():
            plt.text(i - 0.2, row['min'] + 50, str(row['min']), ha='center', va='bottom')
            plt.text(i + 0.2, row['max'] + 50, str(row['max']), ha='center', va='bottom')

        plt.title('Tren Penyewa Sepeda Berdasarkan Musim')
        plt.xlabel('Musim')
        plt.ylabel('Jumlah Penyewa Sepeda')
        plt.xticks(ticks=x, labels=['Spring', 'Summer', 'Fall', 'Winter'])
        plt.legend()
        st.pyplot(plt)

    st.subheader('Distribusi Tren Penyewa Sepeda Berdasarkan Musim')
    plot_season_rentals_vertical(season_rentals_df)