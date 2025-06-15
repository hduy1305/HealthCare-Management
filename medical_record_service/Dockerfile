# Base image
FROM python:3.11-slim
WORKDIR /app

# Cài các deps
RUN apt-get update && apt-get install -y \
    gcc g++ libpq-dev libffi-dev libssl-dev \
    default-libmysqlclient-dev python3-dev pkg-config \
    build-essential netcat-openbsd default-mysql-client \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements & cài packages
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy script chờ MySQL và source
COPY wait-for-mysql.sh ./wait-for-mysql.sh
RUN chmod +x ./wait-for-mysql.sh
COPY . .

# (Tuỳ chọn) Thu thập static files nếu có
RUN python manage.py collectstatic --noinput || echo "No static files"

# ENTRYPOINT chờ MySQL service 'mysql-appointment'
ENTRYPOINT ["./wait-for-mysql.sh"]

# Sau khi MySQL sẵn sàng, chạy migrate và start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
