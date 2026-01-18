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
