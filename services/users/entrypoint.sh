#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z users-db 5432; do
	sleep 0.1
done

echo "PostgreSQL started"

python manage.py run --host 0.0.0.0 --cert ssl/server.crt --key ssl/server.key