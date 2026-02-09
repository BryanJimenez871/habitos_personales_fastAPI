# Imagen base liviana
FROM python:3.12-slim

# Crea el usuario appuser
RUN useradd -m appuser

# Evita archivos .pyc y buffers raros
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements primero (cache inteligente)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Dar permisos al usuario sobre /app
RUN chown -R appuser:appuser /app

# Cambio al usuario creado
USER appuser

# Exponer el puerto de FastAPI
EXPOSE 8000

# Comando para correr la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]