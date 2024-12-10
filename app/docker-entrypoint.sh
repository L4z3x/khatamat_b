#!/bin/bash
cd /app

echo "Waiting for Postgres DB"
while ! pg_isready -h db > /dev/null 2>&1;
do
  echo -n "."
  sleep 1
done
echo "Postgres DB is ready"
python manage.py collectstatic --noinput 

# create tables
echo "Updating Database Tables"
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py spectacular --file schema.yml
echo "The Database has been updated"

echo "Superuser..."
if [ "$(hostname)" = "django-app" ]; then
  cat create_superuser.py | python3 manage.py shell
fi
# run the server
echo "Starting the server..."
python3 manage.py runserver 0.0.0.0:8000