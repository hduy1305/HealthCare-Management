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
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements và cài đặt Python packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code
COPY . .

# Thêm script chờ MySQL
COPY wait-for-mysql.sh /wait-for-mysql.sh
RUN chmod +x /wait-for-mysql.sh

# Thu thập static files (nếu có)
RUN python manage.py collectstatic --noinput || echo "No static files to collect"

# Chạy script đợi MySQL rồi mới migrate + runserver
CMD ["/wait-for-mysql.sh", "mysql-doctor", "3306", "python", "manage.py", "runserver", "0.0.0.0:8000"]
