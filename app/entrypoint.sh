#!/bin/ash

# Collect static files
echo "Collect static files"

echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

if ! python manage.py shell -c "from django.contrib.auth import get_user_model; print(get_user_model().objects.filter(username='admin').exists())" | grep -q "True"; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput --username admin --email admin@example.com --gender male --country Algeria
    
    python manage.py shell -c "from django.contrib.auth import get_user_model; user = get_user_model().objects.get(username='admin'); user.set_password('admin_password'); user.save()"
else
    echo "Superuser already exists."
fi

# Execute the provided command or entrypoint
exec "$@"