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
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "../data/day.csv")
    if not os.path.exists(file_path):
        st.error(f"⚠ File tidak ditemukan: {file_path}")
        return None
    df = pd.read_csv(file_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

# Load dataset
day_df = load_data()
if day_df is None:
    st.stop()

# Sidebar: Filter Rentang Waktu
st.sidebar.header("📅 Filter Data berdasarkan Tanggal")
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

# Pilihan rentang waktu (start_date & end_date)
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
)

# Konversi ke datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter dataset berdasarkan rentang waktu
filtered_df = day_df[(day_df["dteday"] >= start_date) & (day_df["dteday"] <= end_date)]

# 📌 1. Tren Penyewaan Sepeda (Harian)
st.subheader("📌 Tren Jumlah Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(filtered_df['dteday'], filtered_df['cnt'], label='Total Rentals', color='blue', linewidth=2)
ax.set_title('Tren Jumlah Penyewaan Sepeda', fontsize=12)
ax.set_xlabel('Tanggal', fontsize=10)
ax.set_ylabel('Jumlah Penyewaan', fontsize=10)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%y/%m/%d'))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
plt.xticks(rotation=45, ha="right")
ax.legend()
plt.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig)

# 📌 2. Analisis Pola Musiman
st.subheader("📌 Pola Musiman Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 4))
sns.lineplot(x=filtered_df['mnth'], y=filtered_df['cnt'], marker='o', color='blue', label='Total Rentals')
ax.set_title("Pola Musiman Penyewaan Sepeda")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
plt.xticks(range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
plt.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig)

# 📌 3. Korelasi Faktor terhadap Jumlah Penyewaan
st.subheader("📌 Korelasi Faktor terhadap Jumlah Penyewaan")
correlation_matrix = filtered_df.corr(numeric_only=True)
cnt_correlation = correlation_matrix["cnt"].drop("cnt").sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(cnt_correlation.to_frame(), annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f", ax=ax)
ax.set_title("Korelasi Faktor terhadap Jumlah Penyewaan Sepeda")
st.pyplot(fig)

# 📌 4. Jam dengan Penyewaan Tertinggi dan Terendah
st.subheader("📌 Jam dengan Penyewaan Tertinggi dan Terendah")
file_path_hour = os.path.join(os.path.dirname(__file__), "../data/hour.csv")
hour_df = pd.read_csv(file_path_hour)
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Filter data berdasarkan tanggal
hour_filtered = hour_df[(hour_df["dteday"] >= start_date) & (hour_df["dteday"] <= end_date)]

if not hour_filtered.empty:
    hourly_avg = hour_filtered.groupby("hr")["cnt"].mean()
    peak_hour = hourly_avg.idxmax()
    low_hour = hourly_avg.idxmin() 
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(hourly_avg.index, hourly_avg.values, marker='o', linestyle='-', color='blue', label="Avg Rentals per Hour")
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam", fontsize=12)
    ax.set_xlabel("Jam", fontsize=10)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=10)
    plt.xticks(range(0, 24))
    plt.grid(True, linestyle="--", alpha=0.6)
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("Tidak ada data dalam rentang waktu yang dipilih.")
