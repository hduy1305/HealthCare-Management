#!/bin/sh

# Chờ đến khi MySQL container sẵn sàng
echo "Waiting for mysql-patient..."

while ! nc -z mysql-patient 3306; do
  sleep 1
done

echo "MySQL-patient started"

# Chạy Django
exec "$@"
