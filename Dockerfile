FROM python:3.11-slim

# Instalar LibreOffice para conversión de documentos
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    libreoffice-core \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero (mejor caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Variables de entorno
ENV RENDER=true
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
