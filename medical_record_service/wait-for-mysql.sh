#!/bin/sh

# Chờ đến khi MySQL container sẵn sàng
echo "Waiting for mysql-medical-record..."

while ! nc -z mysql-medical-record 3306; do
  sleep 1
done

echo "MySQL-medical-record started"

# Chạy Django
exec "$@"
