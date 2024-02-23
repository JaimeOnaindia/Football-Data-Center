#!/bin/sh

# Esperar a que PostgreSQL esté listo
# Ejemplo usando wait-for-it o similar

# Aplicar migraciones de Django
python django_quickstart/manage.py migrate

# Recopilar archivos estáticos
python django_quickstart/manage.py collectstatic --noinput

# Iniciar el servidor de desarrollo de Django
exec python django_quickstart/manage.py runserver 0.0.0.0:8000
