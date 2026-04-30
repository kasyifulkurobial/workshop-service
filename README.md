# Workshop Service Management System (Odoo 17)

Repositori ini berisi modul kustom Odoo 17 yang dirancang untuk mengelola operasional bengkel atau pusat servis. Modul ini mengintegrasikan alur kerja dari pendaftaran servis hingga otomatisasi dokumen penjualan (*Sales*) dan pergudangan (*Inventory*).

## 🚀 Fitur Utama

*   **Service Order Management**: Pencatatan data kendaraan, estimasi waktu servis, dan teknisi penanggung jawab.
*   **Automated Calculations**: Perhitungan otomatis Subtotal, Pajak (11%), Grand Total, serta durasi hari servis menggunakan *compute fields*.
*   **Smart Validation**: Validasi cerdas untuk mencegah konfirmasi tanpa baris servis atau pembuatan dokumen ganda.
*   **Sales Integration**: Konversi otomatis baris servis menjadi *Sale Order Quotation* hanya dengan satu klik.
*   **Stock Picking Filter**: Otomatisasi pembuatan dokumen pengiriman barang (*Stock Picking*) yang secara cerdas hanya menarik item bertipe *Spare Part*.

## 🛠️ Tech Stack

*   **ERP Framework**: Odoo 17 (Community/Enterprise).
*   **Language**: Python 3.10+.
*   **UI/UX**: XML, OWL Framework.
*   **Database**: PostgreSQL.

## 📋 Prasyarat Sistem

Sebelum menginstal, pastikan modul berikut sudah terpasang di database Odoo Anda:
1.  `sale_management`.
2.  `stock` (Inventory).

## 🔧 Cara Instalasi

1.  **Clone Repositori**:
    ```bash
    cd /path/to/your/odoo/custom_addons
    git clone [https://github.com/kasyifulkurobial/workshop-service.git](https://github.com/kasyifulkurobial/workshop-service.git)
    ```
2.  **Update Addons Path**: Pastikan direktori `custom_addons` sudah terdaftar di file `odoo.conf` Anda.
3.  **Restart Service**:
    ```bash
    ./odoo-bin -c odoo.conf -u workshop_service
    ```
4.  **Aktivasi**: Masuk ke menu **Apps**, cari `workshop_service`, lalu klik **Activate**.

## 📖 Skenario Pengujian (UAT)

Untuk memverifikasi fungsi modul, Anda dapat mengikuti langkah-langkah berikut:
1.  Buat **Service Order** baru dan isi detail kendaraan serta teknisi.
2.  Tambahkan baris servis dengan tipe **Labor** dan **Spare Part**.
3.  Klik **Confirm** untuk memvalidasi data.
4.  Klik **Create Sale Order** untuk membuat penawaran penjualan.
5.  Klik **Create Stock Picking** untuk memproses pengeluaran barang dari gudang (Hanya baris Spare Part yang akan masuk).

---
**Kontak Pengembang:**
Kasyiful Kurobi Alqorrosyai - Junior Odoo Developer
