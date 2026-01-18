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
