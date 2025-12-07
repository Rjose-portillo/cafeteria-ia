# 1. Usamos Python ligero (Slim) para que la imagen pese poco
FROM python:3.10-slim

# 2. Evitamos que Python genere archivos .pyc y bufferee logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos y instalamos dependencias PRIMERO (para usar caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto del código (main.py, models.py, etc.)
COPY . .

# 6. Definimos el puerto por defecto (Cloud Run usa 8080)
ENV PORT=8080

# 7. Comando de arranque: Uvicorn escuchando en 0.0.0.0 (necesario para contenedores)
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT
