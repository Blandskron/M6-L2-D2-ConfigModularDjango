# Aplicación 2: Configuración estructural y modular de un proyecto Django

**Proyecto:** `config_modular_django`  
**App:** `estructura`

---

## 1) Crear carpeta contenedora y entrar

```bash
mkdir config_modular_django
cd config_modular_django
````

---

## 2) Crear y activar entorno virtual (Windows)

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3) Instalar Django

```bash
python -m pip install --upgrade pip
pip install django
```

---

## 4) Crear el proyecto (sin punto)

```bash
django-admin startproject config_modular_django
```

---

## 5) Entrar a la carpeta del proyecto (donde está manage.py)

```bash
cd config_modular_django
```

---

## 6) Ver ayuda general de comandos

```bash
python manage.py help
```

---

## 7) Crear la app

```bash
python manage.py startapp estructura
```

---

## 8) Migraciones base

```bash
python manage.py migrate
```

---

## 9) Modificar `config_modular_django/settings.py` (solo cambios)

Agregar la app:

```python
INSTALLED_APPS += [
    "estructura",
]
```

Configurar templates globales (dentro de `TEMPLATES[0]`):

```python
"DIRS": [BASE_DIR / "templates"],
```

---

## 10) Modificar `config_modular_django/urls.py` (solo cambios)

```python
from django.urls import include, path

urlpatterns += [
    path("", include(("estructura.urls", "estructura"), namespace="estructura")),
]
```

---

## 11) Crear `estructura/urls.py`

```python
from django.urls import path

from . import views

app_name = "estructura"

urlpatterns = [
    path("hola/", views.hola, name="hola"),
    path("", views.home, name="home"),
    path("mvt/", views.mvt, name="mvt"),
]
```

---

## 12) Modificar `estructura/models.py` (archivo completo)

```python
from __future__ import annotations

from django.db import models


class Componente(models.Model):
    """
    Modelo mínimo para correlacionar componentes esenciales del proyecto.
    """

    nombre = models.CharField(max_length=80)
    rol = models.CharField(max_length=40)

    class Meta:
        verbose_name = "Componente"
        verbose_name_plural = "Componentes"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.nombre} ({self.rol})"
```

---

## 13) Modificar `estructura/views.py` (archivo completo)

```python
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Componente


def hola(_: HttpRequest) -> HttpResponse:
    """
    Respuesta directa: confirma routing -> view sin templates.
    """
    return HttpResponse("Hola mundo desde estructura (sin template).")


def home(request: HttpRequest) -> HttpResponse:
    """
    Home con template base, demostrando URL -> View -> Template.
    """
    return render(
        request,
        "estructura/home.html",
        {
            "titulo": "Configuración estructural y modular",
        },
    )


def mvt(request: HttpRequest) -> HttpResponse:
    """
    Demostración mínima de MVT: consulta ORM y renderiza lista.
    """
    # Seed mínimo: asegura algunos componentes sin depender de comandos extra.
    if Componente.objects.count() == 0:
        Componente.objects.bulk_create(
            [
                Componente(nombre="models.py", rol="Modelo"),
                Componente(nombre="views.py", rol="Vista"),
                Componente(nombre="urls.py", rol="Router"),
                Componente(nombre="templates/", rol="Template"),
                Componente(nombre="settings.py", rol="Configuración"),
            ]
        )

    componentes = Componente.objects.order_by("id")

    return render(
        request,
        "estructura/mvt.html",
        {
            "titulo": "MVT: Modelo - Vista - Template",
            "componentes": componentes,
        },
    )
```

---

## 14) Crear carpetas de templates (desde donde está manage.py)

```bash
mkdir templates
mkdir templates\estructura
```

---

## 15) Crear `templates/base.html`

```html
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>{% block title %}Django Modular{% endblock %}</title>
    <style>
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 0; }
      header, main { max-width: 980px; margin: 0 auto; padding: 16px; }
      header { border-bottom: 1px solid #e5e7eb; }
      nav a { margin-right: 12px; text-decoration: none; }
      code { background: #f3f4f6; padding: 2px 6px; border-radius: 6px; }
      .card { border: 1px solid #e5e7eb; border-radius: 12px; padding: 12px; margin: 12px 0; }
      .muted { color: #6b7280; }
    </style>
  </head>

  <body>
    <header>
      <div class="muted">Aplicación 2 — Configuración estructural y modular</div>
      <h1 style="margin: 8px 0;">{% block h1 %}Django Modular{% endblock %}</h1>

      <nav>
        <a href="{% url 'estructura:home' %}">Home</a>
        <a href="{% url 'estructura:hola' %}">Hola</a>
        <a href="{% url 'estructura:mvt' %}">MVT</a>
      </nav>
    </header>

    <main>
      {% block content %}{% endblock %}
    </main>
  </body>
</html>
```

---

## 16) Crear `templates/estructura/home.html`

```html
{% extends "base.html" %}

{% block title %}Home | Estructura{% endblock %}
{% block h1 %}Home{% endblock %}

{% block content %}
  <div class="card">
    <p><strong>{{ titulo }}</strong></p>
    <p class="muted">Rutas:</p>
    <ul>
      <li><code>/hola/</code></li>
      <li><code>/mvt/</code></li>
    </ul>
  </div>
{% endblock %}
```

---

## 17) Crear `templates/estructura/mvt.html`

```html
{% extends "base.html" %}

{% block title %}MVT | Estructura{% endblock %}
{% block h1 %}MVT{% endblock %}

{% block content %}
  <div class="card">
    <p><strong>{{ titulo }}</strong></p>
    <p class="muted">Listado desde ORM:</p>
  </div>

  <div class="card">
    {% if componentes %}
      <ul>
        {% for c in componentes %}
          <li><strong>{{ c.nombre }}</strong> — <span class="muted">{{ c.rol }}</span></li>
        {% endfor %}
      </ul>
    {% else %}
      <p class="muted">No hay componentes.</p>
    {% endif %}
  </div>
{% endblock %}
```

---

## 18) Crear y aplicar migraciones de la app

```bash
python manage.py makemigrations estructura
python manage.py migrate
```

---

## 19) Levantar el servidor

```bash
python manage.py runserver
```

Rutas:

* `http://127.0.0.1:8000/` → Home (template)
* `http://127.0.0.1:8000/hola/` → Hola (HttpResponse directo)
* `http://127.0.0.1:8000/mvt/` → MVT (ORM + template)

---

## 20) Comandos de ayuda (referencia)

```bash
python manage.py <comando> --help
python manage.py runserver --help
python manage.py startapp --help
```

---

## 21) Soluciones rápidas si aparece `TemplateDoesNotExist`

Si al abrir `/` aparece:

`TemplateDoesNotExist: estructura/home.html`

### 1) Verifica que estás en la carpeta correcta (donde está manage.py)

```bash
dir
```

Debes ver `manage.py`.

### 2) Verifica que la carpeta exista

```bash
dir templates
dir templates\estructura
```

Debe existir:

* `templates\base.html`
* `templates\estructura\home.html`
* `templates\estructura\mvt.html`

### 3) Confirma que Django está buscando en esa carpeta

```bash
python manage.py shell
```

Luego:

```python
from django.conf import settings
settings.TEMPLATES[0]["DIRS"]
```

Debe mostrar una ruta que termina en:

`...\config_modular_django\templates`

### 4) Si los archivos existen pero no se cargan, reinicia el servidor

```bash
# CTRL + C
python manage.py runserver
```

---

## 22) Solución rápida si aparece `no such table: estructura_componente`

Si al abrir `/mvt/` aparece:

`OperationalError: no such table: estructura_componente`

Ejecuta:

```bash
python manage.py makemigrations estructura
python manage.py migrate
```

Para confirmar:

```bash
python manage.py showmigrations estructura
```

---

## 23) Salir del entorno virtual

```bash
deactivate
```
