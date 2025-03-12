import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Konfigurasi Streamlit
st.set_page_config(page_title="📊 Analisis Penyewaan Sepeda", layout="centered")

# Dapatkan path absolut ke direktori script ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Fungsi untuk membaca dataset
@st.cache_data
def load_data_day():
    file_path = "D:/dicoding/Submission/data/day.csv"
    
    if not os.path.exists(file_path):
        st.error(f"⚠️ File tidak ditemukan: {file_path}")
        return None
    
    df = pd.read_csv(file_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

@st.cache_data  
def load_data_hour():
    file_path = "D:/dicoding/Submission/data/hour.csv"
    
    if not os.path.exists(file_path):
        st.error(f"⚠️ File tidak ditemukan: {file_path}")
        return None
    
    df = pd.read_csv(file_path)
    return df

# Load dataset
day_df = load_data_day()
hour_df = load_data_hour()

# Cek apakah dataset berhasil dimuat
if day_df is None or hour_df is None:
    st.error("❌ Gagal memuat dataset. Pastikan file CSV ada di folder `data/`.")
    st.stop()  # Hentikan eksekusi jika dataset tidak ditemukan

# Header
st.title("📊 Analisis Penyewaan Sepeda")

# 📌 1. Tren Penyewaan Sepeda
with st.container():
    st.subheader("📌 Tren Jumlah Penyewaan Sepeda")

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(day_df['dteday'], day_df['cnt'], label='Total Rentals', color='blue', linewidth=2)
    ax.set_title('Tren Jumlah Penyewaan Sepeda', fontsize=12)
    ax.set_xlabel('Tanggal', fontsize=10)
    ax.set_ylabel('Jumlah Penyewaan', fontsize=10)
    ax.legend()
    plt.xticks(rotation=30)
    plt.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig)

# 📌 2. Rata-rata Penyewaan per Jam
with st.container():
    st.subheader("📌 Rata-rata Penyewaan Sepeda per Jam")

    hourly_avg = hour_df.groupby("hr")["cnt"].mean()

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(hourly_avg.index, hourly_avg.values, marker='o', linestyle='-', color='blue', label="Avg Rentals per Hour")
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam", fontsize=12)
    ax.set_xlabel("Jam", fontsize=10)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=10)
    plt.xticks(range(0, 24))  
    plt.grid(True, linestyle="--", alpha=0.6)
    ax.legend()
    st.pyplot(fig)

# 📌 3. Penyewaan Sepeda Berdasarkan Jam
with st.container():
    st.subheader("📌 Penyewaan Sepeda Berdasarkan Jam")

    hourly_rentals = hour_df.groupby("hr")["cnt"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 3))
    sns.barplot(x=hourly_rentals.index, y=hourly_rentals.values, palette="viridis", ax=ax)
    ax.set_title("Penyewaan Sepeda Berdasarkan Jam", fontsize=12)
    ax.set_xlabel("Jam", fontsize=10)
    ax.set_ylabel("Total Penyewaan", fontsize=10)
    st.pyplot(fig)
        
# 📌 4. Korelasi Faktor terhadap Penyewaan
with st.container():
    st.subheader("📌 Korelasi Faktor terhadap Penyewaan Sepeda")

    numeric_df = hour_df.drop(columns=['dteday'])  
    corr_matrix = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax, linewidths=0.5)
    ax.set_title("Matriks Korelasi Penyewaan Sepeda", fontsize=12)
    st.pyplot(fig)

# 📌 5. Faktor yang Mempengaruhi Penyewaan Sepeda
with st.container():
    st.subheader("📌 Faktor yang Mempengaruhi Penyewaan Sepeda")

    important_factors = corr_matrix["cnt"].sort_values(ascending=False)[1:]  

    fig, ax = plt.subplots(figsize=(8, 3))
    sns.barplot(x=important_factors.index, y=important_factors.values, palette="Reds_r", ax=ax)
    ax.set_title("Faktor yang Mempengaruhi Penyewaan Sepeda", fontsize=12)
    ax.set_xlabel("Fitur", fontsize=10)
    ax.set_ylabel("Korelasi dengan Penyewaan Sepeda", fontsize=10)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 📌 6. Histogram Distribusi Data
with st.container():
    st.subheader("📌 Distribusi Data Penyewaan Sepeda")

    fig, ax = plt.subplots(figsize=(8, 5))
    hour_df.hist(ax=ax, bins=20, color='skyblue', edgecolor='black', grid=False)
    plt.tight_layout()
    st.pyplot(fig)

# Kesimpulan dalam expander
with st.expander("🔍 Kesimpulan"):
    st.write("""
    - Faktor dengan korelasi tertinggi terhadap jumlah penyewaan sepeda adalah fitur yang memiliki nilai korelasi mendekati 1.
    - Penyewaan sepeda tertinggi terjadi pada jam-jam tertentu, yang bisa dimanfaatkan untuk strategi bisnis.
    - Distribusi data penyewaan sepeda menunjukkan pola yang bisa digunakan untuk memprediksi tren ke depan.
    """)
