"""
Archivo de pruebas para la clase Producto en la raíz del proyecto.
Permite la ejecución directa mediante:
- pytest test_producto.py
- python test_producto.py
- python -m unittest test_producto.py
"""

from tests.test_producto import (
    TestProductoBasico,
    TestProductoActualizarPrecioYExcepciones,
)

if __name__ == "__main__":
    import pytest
    import sys
    sys.exit(pytest.main(["-v", __file__]))
