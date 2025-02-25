import unittest
from unittest.mock import patch
from src.utilidades import generar_nombre_gdb_unico

class TestUtilidades(unittest.TestCase):
    @patch("arcpy.Exists")
    def test_generar_nombre_gdb_unico(self, mock_exists):
        mock_exists.side_effect = [True, False]  # Simula que el primer nombre existe, el segundo no
        ruta = generar_nombre_gdb_unico("/ruta", "CartoBase")
        self.assertEqual(ruta, "/ruta/CartoBase_2.gdb")

if __name__ == "__main__":
    unittest.main()