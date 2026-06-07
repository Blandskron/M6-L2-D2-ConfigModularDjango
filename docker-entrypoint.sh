#!/bin/sh

# Detener el script si ocurre algún error
set -e

echo "=== Aplicando migraciones de la Base de Datos ==="
python manage.py migrate --noinput

# Crear superusuario de forma no interactiva e idempotente
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] && [ "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "=== Creando/Verificando Superusuario ($DJANGO_SUPERUSER_USERNAME) ==="
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superusuario creado exitosamente.')
else:
    print('El superusuario ya existe. Omitiendo creación.')
"
else
    echo "=== Credenciales de superusuario no completadas. Omitiendo creación ==="
fi

echo "=== Iniciando el comando principal ==="
exec "$@"
