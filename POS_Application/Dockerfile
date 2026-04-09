# Gunakan image Python resmi
FROM python:3.11-slim

# Install dependensi sistem yang dibutuhkan untuk mysql-connector dan pandas
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Tentukan direktori kerja di dalam container
WORKDIR /app

# Copy requirements dan install library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode project ke dalam container
COPY . .

# Expose port yang digunakan Flask
EXPOSE 5000

# Jalankan aplikasi
CMD ["python", "app.py"]