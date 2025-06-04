#!/bin/sh

host="$1"
port="$2"
shift 2

echo "Waiting for MySQL at $host:$port..."

while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "MySQL is up!"

exec "$@"
