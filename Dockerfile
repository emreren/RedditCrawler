# Base image olarak Python kullanın
FROM python:3.11.4

# Çalışma dizinini /app olarak ayarlayın
WORKDIR /app

# Gerekli paketleri kopyalayın
COPY requirements.txt .

# Paketleri yükleyin
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyalayın
COPY . .

# Uygulamayı çalıştırın
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
