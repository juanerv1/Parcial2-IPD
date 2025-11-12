# Usamos Python 3.11 como base
FROM python:3.11-slim

# Crear directorio de la app
WORKDIR /app

# Copiar archivos necesarios
COPY app.py /app
COPY requirements.txt /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 5000

# Comando para iniciar la app
CMD ["python", "app.py"]