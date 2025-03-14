import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Konfigurasi Streamlit
st.set_page_config(page_title="📊 Analisis Penyewaan Sepeda", layout="centered")

# Fungsi untuk membaca dataset
@st.cache_data
def load_data_day():
    file_path = "day.csv"
    
    if not os.path.exists(file_path):
        st.error(f"⚠ File tidak ditemukan: {file_path}")
        return None
    
    df = pd.read_csv(file_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

@st.cache_data  
def load_data_hour():
    file_path = "hour.csv"
    
    if not os.path.exists(file_path):
        st.error(f"⚠ File tidak ditemukan: {file_path}")
        return None
    
    df = pd.read_csv(file_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

# Load dataset
day_df = load_data_day()
hour_df = load_data_hour()

# Cek apakah dataset berhasil dimuat
if day_df is None or hour_df is None:
    st.error("❌ Gagal memuat dataset. Pastikan file CSV ada di folder data/.")
    st.stop()

# Header
st.title("📊 Analisis Penyewaan Sepeda")

# 🔹 Fitur Interaktif: Filter Berdasarkan Tanggal
st.sidebar.header("📅 Filter Data berdasarkan Tanggal")
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

selected_date = st.sidebar.date_input("Pilih Tanggal", value=min_date, min_value=min_date, max_value=max_date)

# Konversi ke datetime agar bisa difilter
selected_date = pd.to_datetime(selected_date)
day_filtered = day_df[day_df["dteday"] == selected_date]
hour_filtered = hour_df[hour_df["dteday"] == selected_date]

# 📌 1. Tren Penyewaan Sepeda
with st.container():
    st.subheader("📌 Tren Jumlah Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(day_df['dteday'], day_df['cnt'], label='Total Rentals', color='blue', linewidth=2)
    ax.axvline(selected_date, color='red', linestyle='--', label='Selected Date')
    ax.set_title('Tren Jumlah Penyewaan Sepeda', fontsize=12)
    ax.set_xlabel('Tanggal', fontsize=10)
    ax.set_ylabel('Jumlah Penyewaan', fontsize=10)
    ax.legend()
    plt.xticks(rotation=30)
    plt.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig)

# 📌 2. Rata-rata Penyewaan per Jam pada Tanggal Terpilih
with st.container():
    st.subheader(f"📌 Rata-rata Penyewaan Sepeda pada {selected_date.date()}")
    if not hour_filtered.empty:
        hourly_avg = hour_filtered.groupby("hr")["cnt"].mean()
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(hourly_avg.index, hourly_avg.values, marker='o', linestyle='-', color='blue', label="Avg Rentals per Hour")
        ax.set_title("Rata-rata Penyewaan Sepeda per Jam", fontsize=12)
        ax.set_xlabel("Jam", fontsize=10)
        ax.set_ylabel("Rata-rata Penyewaan", fontsize=10)
        plt.xticks(range(0, 24))  
        plt.grid(True, linestyle="--", alpha=0.6)
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data untuk tanggal yang dipilih.")
