# Actividad M6-L2 — Instalación y Creación de un Proyecto Django

Proyecto: **mi_sitio**  
App: **principal**

---

## 0) Crear carpeta de trabajo

```bash
mkdir actividad_m6_l2
cd actividad_m6_l2
````

Dentro de esta carpeta se realizará todo el proceso y quedará el proyecto. 

---

## 1) Instalación en entorno virtual

### 1.1 Crear y activar entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

**¿Qué es pip?**
`pip` es el instalador de paquetes de Python. Permite descargar e instalar librerías (por ejemplo, Django) desde repositorios como PyPI.

**¿Qué ventajas ofrece instalar Django dentro de un entorno virtual?**

* Aisla dependencias por proyecto (cada proyecto con sus librerías).
* Evita conflictos de versiones entre proyectos.
* Mantiene el Python global sin “ensuciar” con instalaciones.

La instalación debe hacerse dentro de un entorno virtual. 

---

### 1.2 Actualizar pip e instalar Django

```bash
python -m pip install --upgrade pip
pip install django
```

---

### 1.3 Comprobar la instalación de Django

```bash
django-admin --version
python -m django --version
```

Esto verifica que Django quedó instalado correctamente en el entorno activo. 

---

## 2) Crear el proyecto

### 2.1 Crear el proyecto `mi_sitio`

```bash
django-admin startproject mi_sitio
```

Esto crea una carpeta `mi_sitio/` con el esqueleto del proyecto. 

---

### 2.2 Entrar donde está `manage.py`

```bash
cd mi_sitio
```

---

### 2.3 Estructura inicial generada por Django (copiar y pegar)

Estructura típica al crear el proyecto:

```
mi_sitio/
├─ manage.py
└─ mi_sitio/
   ├─ __init__.py
   ├─ settings.py
   ├─ urls.py
   ├─ asgi.py
   └─ wsgi.py
```

Explicación de cada elemento solicitado: 

#### `manage.py`

Script administrativo del proyecto. Se utiliza para ejecutar comandos como:

* `runserver` (servidor de desarrollo)
* `migrate` (migraciones)
* `startapp` (crear apps)
* `createsuperuser` (usuario admin)
* `help` (ayuda de comandos)

#### `mi_sitio/__init__.py`

Marca el directorio `mi_sitio/` interno como un paquete de Python.

#### `mi_sitio/settings.py`

Archivo central de configuración del proyecto (apps instaladas, middleware, templates, base de datos, etc.).

#### `mi_sitio/urls.py`

Enrutador principal del proyecto. Define qué rutas existen y hacia qué vistas/apps se dirigen.

#### `mi_sitio/asgi.py`

Punto de entrada para servidores ASGI (escenarios async). Se usa en despliegues con servidores ASGI.

#### `mi_sitio/wsgi.py`

Punto de entrada para servidores WSGI (clásico). Se usa en despliegues con servidores WSGI.

---

## 3) Ejecutar el servidor

### 3.1 Correr servidor de desarrollo

```bash
python manage.py runserver
```

---

### 3.2 Verificar en el navegador y capturar evidencia

Abrir:

* `http://127.0.0.1:8000/`

Tomar una captura de pantalla mostrando que el servidor funciona correctamente. 

(Guardar la imagen dentro de `actividad_m6_l2/`)

---

## 4) Crear una aplicación

### 4.1 Crear la app `principal`

En otra terminal (o deteniendo el servidor con CTRL+C):

```bash
python manage.py startapp principal
```

Esto crea la carpeta `principal/` con los archivos base de una app. 

---

### 4.2 Diferencia entre “proyecto” y “aplicación” en Django

* **Proyecto**: contenedor global de configuración (settings, urls, despliegue).
* **Aplicación**: módulo funcional (feature/módulo) que vive dentro del proyecto y agrupa vistas, urls, modelos, etc.

---

### 4.3 Carpetas/archivos que se generan dentro de `principal/`

Estructura típica:

```
principal/
├─ __init__.py
├─ admin.py
├─ apps.py
├─ models.py
├─ tests.py
└─ views.py
```

---

## 5) Configuración del proyecto

### 5.1 Agregar `principal` a `INSTALLED_APPS`

Editar: `mi_sitio/settings.py`

Agregar:

```python
INSTALLED_APPS += [
    "principal",
]
```

Esto es requerido para que Django reconozca la app y sus componentes. 

---

### 5.2 Crear `principal/urls.py`

Crear el archivo: `principal/urls.py`

```python
from django.urls import path

from . import views

app_name = "principal"

urlpatterns = [
    path("", views.inicio, name="inicio"),
]
```

---

### 5.3 Crear una vista simple con HttpResponse

Editar: `principal/views.py`

```python
from django.http import HttpRequest, HttpResponse


def inicio(_: HttpRequest) -> HttpResponse:
    return HttpResponse("¡Bienvenido a mi sitio!")
```

La actividad solicita una vista simple que devuelva ese mensaje con `HttpResponse`. 

---

### 5.4 Configurar enrutamiento del proyecto hacia la app

Editar: `mi_sitio/urls.py`

Agregar:

```python
from django.urls import include, path

urlpatterns += [
    path("", include("principal.urls")),
]
```

Esto hace que la ruta raíz `/` vaya a las URLs de la app `principal`. 

---

## 6) Probar la app configurada

Ejecutar nuevamente:

```bash
python manage.py runserver
```

Abrir:

* `http://127.0.0.1:8000/`

Debe responder:

`¡Bienvenido a mi sitio!`

---

## 7) Entregables

Comprimir en `.zip` la carpeta `actividad_m6_l2` con: 

* `proyecto_django.md` (este documento con comandos y explicación)
* la captura de pantalla del servidor funcionando
* (opcional) el proyecto Django completo funcionando
