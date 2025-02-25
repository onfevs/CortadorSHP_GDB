"""
Módulo de pruebas unitarias para las funciones del explorador.
"""

import os
import shutil
import tempfile
import unittest
from explorador import listar_contenido, generar_arbol_principal

class TestExplorador(unittest.TestCase):
    def setUp(self) -> None:
        # Crear un directorio temporal para pruebas
        self.test_dir = tempfile.mkdtemp()
        # Crear estructura de carpetas y archivos de prueba
        os.makedirs(os.path.join(self.test_dir, "Carpeta1"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "Carpeta2"), exist_ok=True)
        with open(os.path.join(self.test_dir, "archivo.txt"), "w") as f:
            f.write("Contenido")
        # Crear un archivo con extensión excluida
        with open(os.path.join(self.test_dir, "imagen.jpg"), "w") as f:
            f.write("Imagen")
        # Crear un archivo dentro de Carpeta1 para probar recursión
        with open(os.path.join(self.test_dir, "Carpeta1", "subarchivo.txt"), "w") as f:
            f.write("Contenido subarchivo")

    def tearDown(self) -> None:
        # Eliminar el directorio temporal
        shutil.rmtree(self.test_dir)

    def test_listar_contenido_no_recursion(self):
        # Probar listar_contenido sin recursión
        lineas = listar_contenido(self.test_dir, "", no_recursion=True)
        # Verificar que se listan Carpeta1 pero no se incluyen sus contenidos internos
        self.assertTrue(any("Carpeta1" in linea for linea in lineas))
        self.assertFalse(any("subarchivo.txt" in linea for linea in lineas))

    def test_generar_arbol_principal(self):
        # Probar generar_arbol_principal
        arbol = generar_arbol_principal(self.test_dir)
        self.assertTrue(any("Carpeta1" in linea for linea in arbol))
        self.assertTrue(any("Carpeta2" in linea for linea in arbol))

if __name__ == "__main__":
    unittest.main()
