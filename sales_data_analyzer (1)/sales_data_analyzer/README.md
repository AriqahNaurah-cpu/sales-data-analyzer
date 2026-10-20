# Sales Data Analyzer

Aplikasi web analisis penjualan sederhana menggunakan Python, Pandas, Matplotlib, dan Streamlit.

## Fitur
- Memuat dataset CSV bawaan atau mengunggah CSV sendiri.
- Filter berdasarkan kategori dan rentang tanggal.
- Menghitung total omzet, jumlah transaksi, jumlah produk terjual, dan produk terlaris.
- Grafik omzet per tanggal dan jumlah terjual per produk.
- Ringkasan produk berdasarkan jumlah terjual dan omzet.
- Mengunduh data transaksi hasil filter.

## Format CSV
File CSV harus memiliki kolom:
- `Tanggal` (contoh `2026-09-01`)
- `Produk`
- `Kategori`
- `Jumlah`
- `Harga_Satuan`

Kolom `Jumlah` dan `Harga_Satuan` harus berisi angka. Omzet dihitung dari `Jumlah × Harga_Satuan`.

## Menjalankan di Windows
1. Instal Python 3.10 atau lebih baru dari https://www.python.org/downloads/.
2. Ekstrak folder proyek.
3. Buka Command Prompt/Terminal di folder `sales_data_analyzer`.
4. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
5. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```
6. Buka alamat yang ditampilkan di terminal, biasanya `http://localhost:8501`.

## Studi kasus
Pemilik toko atau kedai perlu memahami omzet, produk yang paling banyak terjual, dan perubahan penjualan dari waktu ke waktu. Aplikasi ini merangkum data transaksi menjadi statistik dan visualisasi agar pola penjualan lebih mudah diperiksa.

## Dataset
`data_penjualan.csv` adalah dataset sintetis untuk demonstrasi, bukan transaksi bisnis nyata. Ganti dengan data yang sah digunakan jika diperlukan.

## Hubungan dengan materi webinar
Proyek ini menerapkan analisis data dan visualisasi. Versi awal ini menggunakan analitik deskriptif, bukan model AI/machine learning terlatih. Jika materi webinar mewajibkan metode AI tertentu, tambahkan metode tersebut setelah memastikan materi yang disampaikan pemateri.

## Sumber dan lisensi
Proyek pembelajaran ini dibuat untuk demonstrasi. Jika mengadaptasi kode atau dataset pihak lain, cantumkan sumbernya dan patuhi lisensi yang berlaku.
