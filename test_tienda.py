"""
Archivo de pruebas para la clase Tienda en la raíz del proyecto.
Permite la ejecución directa mediante:
- pytest test_tienda.py
- python test_tienda.py
"""

from tests.test_tienda import (
    TestTiendaBasico,
    TestTiendaExcepciones,
    TestTiendaConFixtures,
    TestTiendaIntegracionCarrito,
)
from tests.test_tienda_doubles import (
    TestTiendaDoblesDePrueba,
    TestTiendaOperacionesBasicasConDobles,
)

if __name__ == "__main__":
    import pytest
    import sys
    sys.exit(pytest.main(["-v", __file__]))
