FROM python:3.11.4

# Gerekli paketleri yükleyin
RUN apt-get update
RUN apt-get install -y  \
    libnss3 \
    libatk-bridge2.0-0 \
    libgbm-dev \
    libgtk-3-0 \
    libasound2 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxrender1 \
    libxtst6 \
    libfontconfig1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libgio2.0-cil \
    libglib2.0-cil \
    libdbus-glib-1-2 \
    libdbus-1-3 \
    libxcb-shm0 \
    libx11-xcb1 \
    libxcb1 \
    libxcursor1 \
    libxi6

# Çalışma dizinini /app olarak ayarlayın
WORKDIR /app

# Gerekli paketleri kopyalayın
COPY requirements.txt .

# Paketleri yükleyin
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install
# Proje dosyalarını kopyalayın
COPY . .

# Uygulamayı çalıştırın
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

