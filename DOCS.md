# Aplicación 2: Configuración estructural y modular de un proyecto Django

Proyecto: **config_modular_django**  
App: **estructura**

Este documento describe cada parte usada en el proyecto y su función.

---

## 1) Estructura del proyecto (doble carpeta)

El proyecto se creó con:

```bash
django-admin startproject config_modular_django
````

Eso genera una estructura con doble carpeta:

```
config_modular_django/
└─ config_modular_django/
   ├─ manage.py
   ├─ config_modular_django/
   │  ├─ __init__.py
   │  ├─ settings.py
   │  ├─ urls.py
   │  ├─ asgi.py
   │  └─ wsgi.py
   ├─ estructura/
   │  ├─ models.py
   │  ├─ views.py
   │  ├─ urls.py
   │  └─ ...
   └─ templates/
      ├─ base.html
      └─ estructura/
         ├─ home.html
         └─ mvt.html
```

Roles:

* Carpeta externa: contenedora (y usualmente contiene `venv`).
* Carpeta interna: contiene el proyecto Django y `manage.py`.
* Paquete `config_modular_django/` interno: configuración del proyecto.
* App `estructura/`: módulo funcional.
* `templates/`: templates globales del proyecto.

---

## 2) Entorno virtual (`venv`)

Se creó con:

```bash
python -m venv venv
```

Se activó con:

```bash
venv\Scripts\activate
```

Qué aporta:

* Aisla dependencias del proyecto (Django y librerías) del sistema.
* Evita instalaciones globales y conflictos.
* Permite controlar versiones por proyecto.

Dentro del venv:

* `python` y `pip` apuntan al entorno aislado.
* `pip install django` instala dentro del venv.

---

## 3) Instalación y utilitarios administrativos

### pip

Se usó para instalar Django:

```bash
pip install django
```

`pip` gestiona dependencias en el entorno activo.

---

### django-admin

Se usó para crear el proyecto:

```bash
django-admin startproject config_modular_django
```

`django-admin` es el utilitario general de Django (no ligado a un proyecto específico).

---

### manage.py

Se usó para administrar el proyecto ya creado:

* Ayuda general y por comando:

  * `python manage.py help`
  * `python manage.py <comando> --help`
* Migraciones:

  * `python manage.py migrate`
  * `python manage.py makemigrations estructura`
* Crear app:

  * `python manage.py startapp estructura`
* Servidor:

  * `python manage.py runserver`

`manage.py` está ligado a la configuración del proyecto: usa `settings.py` automáticamente.

---

## 4) Configuración del proyecto (paquete `config_modular_django/` interno)

Estos archivos viven en:

`config_modular_django/config_modular_django/`

---

### `__init__.py`

Marca la carpeta como paquete Python.
Permite imports como:

* `config_modular_django.settings`

---

### `settings.py`

Es la configuración central del proyecto.

En este proyecto se usó para:

#### a) Registrar una app

Se agregó `estructura` en `INSTALLED_APPS`.

Efecto:

* Django carga la app.
* Django encuentra migraciones de la app.
* Django habilita modelos de la app en el ORM.
* Django puede descubrir templates dentro de apps si `APP_DIRS=True`.

#### b) Configuración de templates

Se configuró:

```python
"DIRS": [BASE_DIR / "templates"],
```

Conceptos usados:

* `BASE_DIR` es la ruta base del proyecto (carpeta donde está `manage.py`).
* `pathlib` permite construir rutas sin concatenación manual.
* `DIRS` define carpetas donde Django busca templates globales.
* `APP_DIRS=True` permite buscar templates dentro de `app/templates/` si existieran.

En este proyecto se usó una carpeta global:

`templates/`

---

### `urls.py` (del proyecto)

Define el router principal.

Aquí se conectó la app mediante:

* `include()` para delegar rutas a la app.
* `namespace` para namespacing.

Ejemplo aplicado:

```python
path("", include(("estructura.urls", "estructura"), namespace="estructura"))
```

Qué resuelve:

* El proyecto no define cada ruta de la app manualmente.
* La app controla sus rutas internas.
* El namespace permite distinguir nombres de URLs entre apps.

---

### `wsgi.py` / `asgi.py`

Son puntos de entrada para servidores reales.

* `wsgi.py`: ejecución en servidores WSGI.
* `asgi.py`: ejecución en servidores ASGI (async).

Aquí no se modifican: forman parte del esqueleto estándar.

---

## 5) App `estructura`

Se creó con:

```bash
python manage.py startapp estructura
```

La app contiene los componentes esenciales del patrón MVT:

* `models.py` (Modelo)
* `views.py` (Vista/Controlador)
* `urls.py` (Router de la app)
* Templates (Presentación)

---

## 6) Router de la app (`estructura/urls.py`)

Define rutas internas de la app y su `app_name`:

```python
app_name = "estructura"
```

Rutas usadas:

* `/hola/` → `views.hola`
* `/` → `views.home`
* `/mvt/` → `views.mvt`

Cómo funciona:

* La URL se resuelve primero en el router del proyecto.
* `include()` deriva la resolución al router de la app.

---

## 7) Vistas (`estructura/views.py`)

Las vistas reciben `HttpRequest` y devuelven `HttpResponse`.

Este proyecto usa 2 formas de respuesta:

### a) Respuesta directa (sin templates)

`hola()` usa `HttpResponse` directamente:

```python
return HttpResponse("Hola mundo ...")
```

Esto valida:

* routing funcionando
* view ejecutándose sin depender de templates

---

### b) Render con templates

`home()` y `mvt()` usan:

```python
return render(request, "estructura/home.html", contexto)
```

`render()`:

* carga el template
* mezcla template + contexto
* retorna `HttpResponse` final

---

### c) Interacción ORM + template

`mvt()` consulta el modelo `Componente` y renderiza lista:

* `Componente.objects.count()`
* `bulk_create()` para cargar datos mínimos si no existen
* `order_by()` para devolver en orden estable

Esto conecta:

* Modelo (DB)
* Vista (consulta/seed/contexto)
* Template (presentación)

---

## 8) Modelos (`estructura/models.py`)

Modelo usado: `Componente`

Campos:

* `nombre` (CharField)
* `rol` (CharField)

Meta:

* `ordering = ["id"]` para orden consistente
* `verbose_name` y `verbose_name_plural` para nombre humano

Por qué existe:

* Proveer una tabla simple para demostrar migraciones + ORM.
* Correlacionar archivos/roles (models/views/urls/templates/settings).

---

## 9) Base de datos y migraciones

Se usó SQLite por defecto.

### `migrate`

```bash
python manage.py migrate
```

Aplica migraciones base de Django (auth, admin, sessions, etc.).

### `makemigrations estructura`

```bash
python manage.py makemigrations estructura
```

Genera un archivo de migración para `Componente` a partir de `models.py`.

### `migrate` (segunda vez)

```bash
python manage.py migrate
```

Crea la tabla real en la base de datos:

* `estructura_componente`

---

## 10) Templates (presentación)

Se usó un folder global:

`templates/`

Con:

* `templates/base.html`
* `templates/estructura/home.html`
* `templates/estructura/mvt.html`

### Herencia de templates

`home.html` y `mvt.html` hacen:

```django
{% extends "base.html" %}
```

Esto permite:

* layout común
* navegación compartida
* mantener DRY en HTML

### Tags usados

* `{{ variable }}`: imprime valores del contexto
* `{% if %}`: control condicional
* `{% for %}`: iteración de listas/querysets
* `{% url %}`: genera URLs por nombre usando namespace

---

## 11) Namespaces de URLs

Se configuró:

* `app_name = "estructura"` en la app
* `namespace="estructura"` en el include del proyecto

Eso permite llamar URLs así en templates:

```django
{% url 'estructura:home' %}
{% url 'estructura:hola' %}
{% url 'estructura:mvt' %}
```

Ventaja:

* Evita colisiones de nombres si existieran múltiples apps con rutas `home`, `detail`, etc.

---

## 12) Servidor de desarrollo

Se levantó con:

```bash
python manage.py runserver
```

Rutas usadas:

* `/` → template
* `/hola/` → respuesta directa
* `/mvt/` → ORM + template

---

## 13) Errores comunes asociados a lo usado

### TemplateDoesNotExist

Significa que Django no encuentra el archivo de template en:

* `TEMPLATES[0]["DIRS"]` (filesystem loader)
* templates dentro de apps (app_directories loader, si aplica)

En este proyecto se resuelve validando:

* carpeta `templates/` en la ruta que indica `settings.TEMPLATES[0]["DIRS"]`
* existencia de `templates/estructura/home.html`

---

### no such table: estructura_componente

Significa que el modelo existe, pero la tabla no fue creada.

Se resuelve ejecutando:

* `python manage.py makemigrations estructura`
* `python manage.py migrate`

---

## 14) Qué cubre este proyecto (alcance exacto)

* Creación de app con `startapp`
* Diferencia proyecto vs aplicación (estructura de carpetas)
* Componentes esenciales (models/views/urls/templates)
* Configuración de templates (DIRS, APP_DIRS)
* Configuración de paths con `BASE_DIR` (pathlib)
* Enrutamiento con `path`, `include` y namespaces
* Comandos de ayuda (`help`, `--help`)
* Migraciones + ORM básico para una tabla mínima
* Renderización y herencia de templates (DRY)
