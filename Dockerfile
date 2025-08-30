FROM python:3.12-slim-bullseye 

# Evitar que python escriba .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Evitar que Python almacene en buffer la salida
ENV PYTHONUNBUFFERED 1 

# Establecemos directorio de trabajo
WORKDIR /app 

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python 
COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt 

# Copiar el proyecto
COPY . .

EXPOSE 8000
