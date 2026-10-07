"""
Configuración global de fixtures para pytest.

Define fixtures reutilizables para inicializar instancias de Producto,
Tienda (vacía y con catálogo predefinido), y dobles de prueba (Mocks).
"""

import pytest
from unittest.mock import MagicMock
from producto import Producto
from tienda import Tienda


@pytest.fixture
def producto_laptop():
    """Retorna un producto representativo de alta gama."""
    return Producto(nombre="Laptop", precio=1200.0, categoria="Computación")


@pytest.fixture
def producto_mouse():
    """Retorna un producto representativo de accesorios."""
    return Producto(nombre="Mouse", precio=25.0, categoria="Accesorios")


@pytest.fixture
def producto_teclado():
    """Retorna un producto representativo de periféricos."""
    return Producto(nombre="Teclado", precio=45.0, categoria="Accesorios")


@pytest.fixture
def tienda_vacia():
    """Retorna una instancia nueva de Tienda con inventario vacío."""
    return Tienda()


@pytest.fixture
def tienda_con_productos():
    """
    Fixture principal de la Sección 4.
    Inicializa una tienda con un catálogo variado de productos de ejemplo
    antes de la ejecución de cada prueba para garantizar estado limpio e independiente.
    """
    tienda = Tienda()
    tienda.agregar_producto(Producto("Laptop", 1200.0, "Computación"))
    tienda.agregar_producto(Producto("Mouse", 25.0, "Accesorios"))
    tienda.agregar_producto(Producto("Teclado", 45.0, "Accesorios"))
    tienda.agregar_producto(Producto("Monitor", 300.0, "Pantallas"))
    return tienda


@pytest.fixture
def mock_producto():
    """
    Fixture que provee un 'Test Double' (Mock) simulando a la clase Producto.
    Configura atributos nombre y precio, y un método actualizar_precio espiable.
    """
    mock = MagicMock(spec=Producto)
    mock.nombre = "ProductoMock"
    mock.precio = 100.0
    mock.categoria = "Pruebas"
    return mock
