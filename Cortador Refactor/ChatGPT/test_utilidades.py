import os
import tempfile
import unittest
from utilidades import get_unique_gdb_name

class TestUtilidades(unittest.TestCase):
    def test_get_unique_gdb_name(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Al no existir ninguna GDB en temp_dir, el nombre único esperado es "CartoBase_1.gdb"
            unique_name = get_unique_gdb_name(temp_dir)
            esperado = os.path.join(temp_dir, "CartoBase_1.gdb")
            self.assertEqual(unique_name, esperado)

if __name__ == '__main__':
    unittest.main()
