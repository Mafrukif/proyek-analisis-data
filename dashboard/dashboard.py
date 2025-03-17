import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.dates as mdates

# Konfigurasi Streamlit
st.set_page_config(page_title="📊 Analisis Penyewaan Sepeda", layout="wide")

# Fungsi untuk membaca dataset
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

# Sidebar: Filter Berdasarkan Rentang Waktu
st.sidebar.header("📅 Filter Data berdasarkan Rentang Waktu")
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

start_date, end_date = st.sidebar.date_input(
    label="Pilih Rentang Waktu", min_value=min_date, max_value=max_date, value=[min_date, max_date]
)
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

day_filtered = day_df[(day_df["dteday"] >= start_date) & (day_df["dteday"] <= end_date)]
hour_filtered = hour_df[(hour_df["dteday"] >= start_date) & (hour_df["dteday"] <= end_date)]

# **1️⃣ Apakah ada pola musiman dalam penyewaan sepeda?**
with st.container():
    st.subheader("📅 Pola Musiman dalam Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10, 4))
    
    sns.lineplot(x=day_filtered['mnth'], y=day_filtered['cnt'], marker='o', color='blue', label='Total Rentals')
    
    ax.set_title("Pola Musiman Penyewaan Sepeda", fontsize=12)
    ax.set_xlabel("Bulan", fontsize=10)
    ax.set_ylabel("Jumlah Penyewaan", fontsize=10)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
    
    plt.grid(True, linestyle="--", alpha=0.6)
    ax.legend()
    
    st.pyplot(fig)

# **2️⃣ Faktor apa yang paling mempengaruhi keterlambatan pengiriman? (Korelasi Faktor)**
with st.container():
    st.subheader("📊 Faktor yang Mempengaruhi Jumlah Penyewaan Sepeda")
    
    correlation_matrix = day_df.corr(numeric_only=True)
    cnt_correlation = correlation_matrix["cnt"].drop("cnt").sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(cnt_correlation.to_frame(), annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f", ax=ax)
    
    ax.set_title("Korelasi Faktor terhadap Jumlah Penyewaan Sepeda")
    
    st.pyplot(fig)

# **3️⃣ Jam berapa penyewaan sepeda paling tinggi dan paling rendah dalam sehari?**
with st.container():
    st.subheader("🕒 Jam Puncak dan Jam Sepi Penyewaan Sepeda")
    
    if not hour_filtered.empty:
        hourly_avg = hour_filtered.groupby("hr")["cnt"].mean()
        fig, ax = plt.subplots(figsize=(10, 4))
        
        sns.lineplot(x=hourly_avg.index, y=hourly_avg.values, marker='o', color='green', label="Avg Rentals per Hour")
        
        ax.set_title("Rata-rata Penyewaan Sepeda per Jam", fontsize=12)
        ax.set_xlabel("Jam", fontsize=10)
        ax.set_ylabel("Rata-rata Penyewaan", fontsize=10)
        
        plt.xticks(range(0, 24))
        plt.grid(True, linestyle="--", alpha=0.6)
        ax.legend()
        
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data untuk rentang waktu yang dipilih.")
