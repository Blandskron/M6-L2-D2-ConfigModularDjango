from django.test import TestCase
from django.urls import reverse
from .models import Componente


class ComponenteModelTest(TestCase):
    def test_componente_creation(self):
        """Prueba que el modelo Componente se cree correctamente y su representación en string sea adecuada."""
        comp = Componente.objects.create(nombre="test.py", rol="Test")
        self.assertEqual(comp.nombre, "test.py")
        self.assertEqual(comp.rol, "Test")
        self.assertEqual(str(comp), "test.py (Test)")


class EstructuraViewsTest(TestCase):
    def test_vista_hola(self):
        """Prueba que la vista hola (HttpResponse directo) responda con código 200 y el texto esperado."""
        response = self.client.get(reverse('estructura:hola'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hola mundo desde estructura (sin template).")

    def test_vista_home(self):
        """Prueba que la vista home use los templates adecuados y pase el contexto esperado."""
        response = self.client.get(reverse('estructura:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'estructura/home.html')
        self.assertEqual(response.context['titulo'], "Configuración estructural y modular")

    def test_vista_mvt_seeds_and_renders(self):
        """Prueba que la vista mvt cree los datos semilla si no existen y renderice el listado."""
        # Al inicio, la base de datos de pruebas está vacía
        self.assertEqual(Componente.objects.count(), 0)

        response = self.client.get(reverse('estructura:mvt'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'estructura/mvt.html')
        self.assertEqual(response.context['titulo'], "MVT: Modelo - Vista - Template")

        # Verifica que se crearon los 5 componentes semilla
        self.assertEqual(Componente.objects.count(), 5)

        # Comprueba que los nombres y roles de los componentes se muestren en el HTML
        self.assertContains(response, "models.py")
        self.assertContains(response, "views.py")
        self.assertContains(response, "urls.py")
        self.assertContains(response, "templates/")
        self.assertContains(response, "settings.py")

