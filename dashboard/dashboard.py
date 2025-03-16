import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates

# Konfigurasi Streamlit
st.set_page_config(page_title="📊 Analisis Penyewaan Sepeda", layout="wide")

# Fungsi untuk membaca dataset dengan path relatif
@st.cache_data
def load_data_day():
    file_path = os.path.join(os.path.dirname(__file__), "../data/day.csv")
    if not os.path.exists(file_path):
        st.error(f"⚠ File tidak ditemukan: {file_path}")
        return None
    df = pd.read_csv(file_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

@st.cache_data  
def load_data_hour():
    file_path = os.path.join(os.path.dirname(__file__), "../data/hour.csv")
    if not os.path.exists(file_path):
        st.error(f"⚠ File tidak ditemukan: {file_path}")
        return None
    df = pd.read_csv(file_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

# Load dataset
day_df = load_data_day()
hour_df = load_data_hour()

if day_df is None or hour_df is None:
    st.error("❌ Gagal memuat dataset. Pastikan file CSV ada di folder data/.")
    st.stop()

# Sidebar: Filter Berdasarkan Tanggal
st.sidebar.header("📅 Filter Data berdasarkan Tanggal")
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

selected_date = st.sidebar.date_input("Pilih Tanggal", value=min_date, min_value=min_date, max_value=max_date)
selected_date = pd.to_datetime(selected_date)

day_filtered = day_df[day_df["dteday"] == selected_date]
hour_filtered = hour_df[hour_df["dteday"] == selected_date]

# 📌 1. Tren Penyewaan Sepeda (Harian)
with st.container():
    st.subheader("📌 Tren Jumlah Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10, 4))
    
    ax.plot(day_df['dteday'], day_df['cnt'], label='Total Rentals', color='blue', linewidth=2)
    ax.axvline(selected_date, color='red', linestyle='--', label='Selected Date')
    
    ax.set_title('Tren Jumlah Penyewaan Sepeda', fontsize=12)
    ax.set_xlabel('Tanggal', fontsize=10)
    ax.set_ylabel('Jumlah Penyewaan', fontsize=10)
    
    # Format sumbu X dengan format YY/MM/DD
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y/%m/%d'))
    
    # Mengatur interval label pada sumbu X agar lebih rapi
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    
    plt.xticks(rotation=45, ha="right")  # Rotasi lebih rapi
    ax.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    
    st.pyplot(fig)

# 📌 2. Rata-rata Penyewaan per Jam pada Tanggal Terpilih
with st.container():
    st.subheader(f"📌 Rata-rata Penyewaan Sepeda pada {selected_date.date()}")
    if not hour_filtered.empty:
        hourly_avg = hour_filtered.groupby("hr")["cnt"].mean()
        fig, ax = plt.subplots(figsize=(10, 4))
        
        ax.plot(hourly_avg.index, hourly_avg.values, marker='o', linestyle='-', color='blue', label="Avg Rentals per Hour")
        
        ax.set_title("Rata-rata Penyewaan Sepeda per Jam", fontsize=12)
        ax.set_xlabel("Jam", fontsize=10)
        ax.set_ylabel("Rata-rata Penyewaan", fontsize=10)
        
        plt.xticks(range(0, 24))  # Menampilkan semua jam dari 0-23
        plt.grid(True, linestyle="--", alpha=0.6)
        ax.legend()
        
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data untuk tanggal yang dipilih.")
