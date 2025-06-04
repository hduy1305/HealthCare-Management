#!/bin/sh

# Chờ đến khi MySQL container sẵn sàng
echo "Waiting for mysql-appointment..."

while ! nc -z mysql-appointment 3306; do
  sleep 1
done

echo "MySQL-patient started"

# Chạy Django
exec "$@"
