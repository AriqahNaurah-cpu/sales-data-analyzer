import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Sales Data Analyzer", page_icon="🛍️", layout="wide")
st.title("🛍️ Sales Data Analyzer")
st.write("Dashboard sederhana untuk memahami performa penjualan toko atau kedai.")

DEFAULT_DATA = Path(__file__).parent / "data_penjualan.csv"
REQUIRED = {"Tanggal", "Produk", "Kategori", "Jumlah", "Harga_Satuan"}

@st.cache_data
def read_default_csv(path):
    return pd.read_csv(path)

uploaded = st.sidebar.file_uploader("Unggah data penjualan (CSV)", type=["csv"])
if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f"File tidak dapat dibaca: {exc}")
        st.stop()
else:
    try:
        df = read_default_csv(DEFAULT_DATA)
        st.sidebar.caption("Menggunakan dataset contoh.")
    except Exception as exc:
        st.error(f"Dataset contoh gagal dibaca: {exc}")
        st.stop()

missing = REQUIRED - set(df.columns)
if missing:
    st.error("Kolom wajib tidak ditemukan: " + ", ".join(sorted(missing)))
    st.info("Kolom wajib: Tanggal, Produk, Kategori, Jumlah, Harga_Satuan.")
    st.stop()

df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
for col in ["Jumlah", "Harga_Satuan"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["Tanggal", "Produk", "Kategori", "Jumlah", "Harga_Satuan"])
df = df[(df["Jumlah"] > 0) & (df["Harga_Satuan"] >= 0)].copy()
if df.empty:
    st.warning("Tidak ada baris data yang valid.")
    st.stop()

df["Omzet"] = df["Jumlah"] * df["Harga_Satuan"]

st.sidebar.header("Filter")
categories = sorted(df["Kategori"].astype(str).unique().tolist())
selected_categories = st.sidebar.multiselect("Kategori produk", categories, default=categories)
min_date = df["Tanggal"].min().date()
max_date = df["Tanggal"].max().date()
date_range = st.sidebar.date_input("Periode tanggal", value=(min_date, max_date), min_value=min_date, max_value=max_date)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

filtered = df[
    df["Kategori"].astype(str).isin(selected_categories)
    & df["Tanggal"].dt.date.between(start_date, end_date)
].copy()

if filtered.empty:
    st.warning("Tidak ada transaksi pada filter yang dipilih. Coba ubah filter.")
    st.stop()

total_revenue = filtered["Omzet"].sum()
total_units = filtered["Jumlah"].sum()
total_transactions = len(filtered)
best_product = filtered.groupby("Produk")["Jumlah"].sum().idxmax()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total omzet", f"Rp {total_revenue:,.0f}".replace(",", "."))
c2.metric("Jumlah transaksi", f"{total_transactions:,}".replace(",", "."))
c3.metric("Produk terjual", f"{total_units:,.0f}".replace(",", "."))
c4.metric("Produk terlaris", best_product)

st.subheader("Data Transaksi")
display_cols = ["Tanggal", "Produk", "Kategori", "Jumlah", "Harga_Satuan", "Omzet"]
st.dataframe(
    filtered[display_cols].sort_values("Tanggal", ascending=False),
    use_container_width=True,
    hide_index=True
)

left, right = st.columns(2)
with left:
    st.subheader("Omzet per Tanggal")
    daily = filtered.groupby(filtered["Tanggal"].dt.date)["Omzet"].sum().sort_index()
    fig, ax = plt.subplots()
    ax.plot([str(d) for d in daily.index], daily.values, marker="o")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Omzet (Rp)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Jumlah Terjual per Produk")
    product_units = filtered.groupby("Produk")["Jumlah"].sum().sort_values()
    fig, ax = plt.subplots()
    product_units.plot(kind="barh", ax=ax)
    ax.set_xlabel("Jumlah terjual")
    ax.set_ylabel("Produk")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.subheader("Ringkasan Analisis")
product_summary = filtered.groupby("Produk").agg(
    Jumlah_Terjual=("Jumlah", "sum"),
    Omzet=("Omzet", "sum")
).sort_values("Jumlah_Terjual", ascending=False)
top_name = product_summary.index[0]
top_qty = product_summary.iloc[0]["Jumlah_Terjual"]
revenue_top_product = product_summary["Omzet"].idxmax()
st.write(f"- Produk dengan jumlah terjual terbanyak: **{top_name}** ({top_qty:g} unit).")
st.write(f"- Produk dengan omzet tertinggi: **{revenue_top_product}**.")
st.write(f"- Rata-rata omzet per transaksi: **Rp {total_revenue / total_transactions:,.0f}**.".replace(",", "."))

st.caption("Dataset bawaan adalah data contoh/sintetis untuk pembelajaran, bukan catatan transaksi toko nyata.")
csv_bytes = filtered[display_cols].to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Unduh data hasil filter (CSV)", data=csv_bytes, file_name="hasil_analisis_penjualan.csv", mime="text/csv")
