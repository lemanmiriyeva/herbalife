FROM python:3.12-slim

# Sistem paketləri
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# İş qovluğu
WORKDIR /app

# Əvvəlcə requirements — layer cache üçün
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Qalan bütün fayllar
COPY . .

# Port
EXPOSE 8000