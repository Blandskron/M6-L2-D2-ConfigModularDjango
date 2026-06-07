FROM python:3.12-slim

# Evita que Python escriba archivos .pyc en el disco
ENV PYTHONDONTWRITEBYTECODE=1

# Evita que Python almacene en búfer stdout y stderr
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema y pip requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente del proyecto Django
COPY config_modular_django /app/

# Copiar el script de entrada (Entrypoint)
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Exponer el puerto del servidor de desarrollo de Django
EXPOSE 8000

# Configurar el script de entrada y comando por defecto
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
