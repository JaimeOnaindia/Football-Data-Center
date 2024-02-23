#!/bin/sh

# Aplicar migraciones de Django
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Iniciar el servidor de desarrollo de Django
python manage.py runserver 0.0.0.0:8000
