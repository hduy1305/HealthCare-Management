# # Base image
# FROM python:3.11-slim

# # Set working directory
# WORKDIR /app

# # Cài đặt các thư viện cần thiết để build psycopg2 và các gói liên quan
# RUN apt-get update && apt-get install -y \
#     gcc \
#     g++ \
#     libpq-dev \
#     libffi-dev \
#     libssl-dev \
#     default-libmysqlclient-dev \
#     python3-dev \
#     pkg-config \
#     build-essential \
#     default-mysql-client \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements and install dependencies
# COPY requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy source code
# COPY . .

# # Thu thập static files (nếu có)
# RUN python manage.py collectstatic --noinput || echo "No static files to collect"

# # Migrate và chạy server
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Cài đặt các thư viện cần thiết để build psycopg2 và các gói liên quan
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    python3-dev \
    pkg-config \
    build-essential \
    netcat-openbsd \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code và script
COPY . .

# Cấp quyền thực thi cho wait script
RUN chmod +x wait-for-mysql.sh

# Thu thập static files (nếu có)
RUN python manage.py collectstatic --noinput || echo "No static files to collect"

# Migrate và chạy server sau khi DB sẵn sàng
CMD ["sh", "-c", "./wait_for_sql.sh && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
