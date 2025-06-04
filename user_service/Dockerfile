# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Cài đặt các thư viện cần thiết để build mysqlclient và mysql client tools
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    python3-dev \
    pkg-config \
    build-essential \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Thu thập static files (nếu có)
RUN python manage.py collectstatic --noinput || echo "No static files to collect"

# Chạy migrate + runserver
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
