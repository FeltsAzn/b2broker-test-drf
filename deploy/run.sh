#!/bin/bash


python3 check_db_connection.py

python3 manage.py migrate
python3 manage.py test

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${API_ADMIN_USERNAME}', '${API_ADMIN_MAIL}', '${API_ADMIN_PASSWORD}')" \
  | python manage.py shell

python3 manage.py runserver "${API_HOST}:${API_PORT}"