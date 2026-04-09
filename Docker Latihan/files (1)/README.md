# NexDrive — File Sharing Application

Aplikasi file sharing MVP menggunakan Flask, MySQL, dan MinIO S3.

## Fitur
- ✅ Registrasi & Login akun
- ✅ Upload file (drag & drop / pilih file)
- ✅ Buat, rename, hapus folder dengan warna
- ✅ Rename & hapus file
- ✅ Download file
- ✅ Preview gambar, video, audio, PDF
- ✅ Tandai file berbintang (starred)
- ✅ Berbagi file via link publik
- ✅ Search file
- ✅ Filter file berdasarkan tipe
- ✅ View grid/list
- ✅ Activity log
- ✅ Storage quota per user
- ✅ Pengaturan & ganti password
- ✅ Responsive (mobile-friendly)

## Prasyarat
- Python 3.9+
- MySQL 8.0+
- MinIO Server

## Setup

### 1. Clone & Install
```bash
cd fileshare
pip install -r requirements.txt
```

### 2. Konfigurasi .env
```bash
cp .env.example .env
# Edit .env sesuai konfigurasi Anda
```

### 3. Buat Database MySQL
```sql
CREATE DATABASE fileshare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Jalankan MinIO
```bash
# Docker
docker run -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  quay.io/minio/minio server /data --console-address ":9001"
```

### 5. Inisialisasi Database
```bash
python init_db.py
```

### 6. Jalankan Aplikasi
```bash
python app.py
```

Buka http://localhost:5000

## Struktur Folder
```
fileshare/
├── app.py              # Flask app factory
├── config.py           # Konfigurasi
├── init_db.py          # Script init database
├── requirements.txt
├── .env.example
├── routes/
│   ├── auth.py         # Register, login, logout
│   └── dashboard.py    # File management routes
├── services/
│   ├── db.py           # MySQL connection pool
│   ├── minio_service.py # MinIO S3 operations
│   ├── auth_service.py  # User management
│   └── file_service.py  # File & folder operations
├── templates/
│   ├── base.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── dashboard/
│   │   ├── layout.html  # Sidebar layout
│   │   ├── index.html   # Main dashboard
│   │   ├── starred.html
│   │   ├── recent.html
│   │   ├── settings.html
│   │   ├── shared.html  # Public share page
│   │   └── not_found.html
│   └── partials/
│       └── file_actions.html
└── static/
    ├── css/style.css
    └── js/app.js
```
