# Usa una imagen oficial de Python como imagen base
FROM python:3.10-bullseye

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Establece variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false

ENV DB_HOST=postgres

# Instala dependencias necesarias
RUN apt-get update && \
    apt-get install -y libpq-dev gcc build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Copia solo los archivos necesarios para instalar dependencias
COPY pyproject.toml poetry.lock* /app/

# Instala dependencias usando Poetry
RUN poetry install --no-interaction --no-ansi

# Copia el resto del código fuente del proyecto al contenedor
COPY . /app/

# Copia el script entrypoint.sh
COPY entrypoint.sh /app/

# Da permisos de ejecución al script entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Configura el script entrypoint.sh como el punto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]

# CMD se sobreescribe en el compose, pero puedes definir uno por defecto aquí
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
