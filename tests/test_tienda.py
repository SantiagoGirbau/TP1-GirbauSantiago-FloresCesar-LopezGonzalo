"""
Suite de pruebas para la clase Tienda.

Abarca:
- Sección 1: Configuración Inicial y Pruebas Básicas (agregar, buscar, eliminar).
- Sección 2: Pruebas con Excepciones (buscar/eliminar producto inexistente).
- Sección 4: Uso de Fixtures para Reutilización de Datos e Independencia.
- Sección 5: Pruebas de Integración y Flujo Completo del Carrito de Compras.
"""

import pytest
from producto import Producto
from tienda import Tienda
from excepciones import ProductoNoEncontradoError


# ==============================================================================
# SECCIÓN 1: Configuración Inicial y Pruebas Básicas
# ==============================================================================
class TestTiendaBasico:
    """
    Pruebas básicas sobre operaciones CRUD del inventario sin fixtures compartidos,
    demostrando la configuración manual tradicional.
    """

    def test_agregar_producto(self):
        """Verifica que un producto nuevo se agregue al inventario de la tienda."""
        tienda = Tienda()
        producto = Producto("Webcam", 50.0, "Accesorios")
        tienda.agregar_producto(producto)

        assert len(tienda.inventario) == 1
        assert producto in tienda.inventario

    def test_buscar_producto_existente(self):
        """Verifica que buscar un producto existente retorne la instancia correcta."""
        tienda = Tienda()
        producto = Producto("Impresora", 200.0, "Oficina")
        tienda.agregar_producto(producto)

        resultado = tienda.buscar_producto("Impresora")
        assert resultado == producto
        assert resultado.precio == 200.0

    def test_eliminar_producto_existente(self):
        """Verifica que eliminar un producto existente lo remueva del inventario."""
        tienda = Tienda()
        producto = Producto("Tablet", 400.0, "Computación")
        tienda.agregar_producto(producto)

        resultado = tienda.eliminar_producto("Tablet")
        assert resultado is True
        assert len(tienda.inventario) == 0


# ==============================================================================
# SECCIÓN 2: Pruebas con Excepciones
# ==============================================================================
class TestTiendaExcepciones:
    """
    Verifica que la tienda lance las excepciones de dominio correctas
    ante situaciones anómalas o estados inexistentes.
    """

    def test_buscar_producto_inexistente_lanza_excepcion(self):
        """Verifica que buscar un producto que no existe lance ProductoNoEncontradoError."""
        tienda = Tienda()
        with pytest.raises(ProductoNoEncontradoError) as exc_info:
            tienda.buscar_producto("Consola")

        assert exc_info.value.nombre == "Consola"
        assert "no se encuentra en el inventario" in str(exc_info.value)

    def test_eliminar_producto_inexistente_lanza_excepcion(self):
        """Verifica que intentar eliminar un producto que no existe lance ProductoNoEncontradoError."""
        tienda = Tienda()
        with pytest.raises(ProductoNoEncontradoError) as exc_info:
            tienda.eliminar_producto("Smartwatch")

        assert exc_info.value.nombre == "Smartwatch"
        assert "no se encuentra en el inventario" in str(exc_info.value)


# ==============================================================================
# SECCIÓN 4: Uso de Fixtures para Reutilización de Datos
# ==============================================================================
class TestTiendaConFixtures:
    """
    Reutiliza el fixture tienda_con_productos para verificar agregar, buscar,
    eliminar y comprobar el aislamiento entre pruebas individuales.
    """

    def test_buscar_producto_con_fixture(self, tienda_con_productos):
        """Verifica la búsqueda de productos precargados mediante el fixture."""
        laptop = tienda_con_productos.buscar_producto("Laptop")
        mouse = tienda_con_productos.buscar_producto("Mouse")

        assert laptop.precio == 1200.0
        assert laptop.categoria == "Computación"
        assert mouse.precio == 25.0

    def test_agregar_producto_con_fixture(self, tienda_con_productos):
        """Verifica que se pueda agregar un nuevo producto sobre la tienda precargada."""
        inicial = len(tienda_con_productos.inventario)
        nuevo = Producto("Parlante", 75.0, "Audio")
        tienda_con_productos.agregar_producto(nuevo)

        assert len(tienda_con_productos.inventario) == inicial + 1
        assert tienda_con_productos.buscar_producto("Parlante") == nuevo

    def test_eliminar_producto_con_fixture(self, tienda_con_productos):
        """Verifica que se pueda eliminar un producto existente precargado por el fixture."""
        inicial = len(tienda_con_productos.inventario)
        resultado = tienda_con_productos.eliminar_producto("Mouse")

        assert resultado is True
        assert len(tienda_con_productos.inventario) == inicial - 1
        with pytest.raises(ProductoNoEncontradoError):
            tienda_con_productos.buscar_producto("Mouse")

    def test_aislamiento_de_fixtures(self, tienda_con_productos):
        """
        Verifica que la prueba anterior no haya alterado el estado de este test.
        'Mouse' debe seguir existiendo gracias al scope por función de pytest.
        """
        mouse = tienda_con_productos.buscar_producto("Mouse")
        assert mouse is not None
        assert len(tienda_con_productos.inventario) == 4


# ==============================================================================
# SECCIÓN 5: Pruebas de Integración y Carrito de Compras
# ==============================================================================
class TestTiendaIntegracionCarrito:
    """
    Pruebas de integración que validan el flujo completo del sistema:
    inventario precargado, aplicación de descuentos, carga del carrito y cálculo total.
    """

    def test_calcular_total_carrito_vacio(self, tienda_con_productos):
        """Un carrito vacío debe arrojar un costo total de 0.0."""
        total = tienda_con_productos.calcular_total_carrito([])
        assert total == 0.0

    def test_calcular_total_carrito_sin_descuentos(self, tienda_con_productos):
        """Calcula el total con precios de lista para múltiples productos."""
        carrito = ["Laptop", "Mouse", "Monitor"]
        # Precios: Laptop (1200.0) + Mouse (25.0) + Monitor (300.0) = 1525.0
        total = tienda_con_productos.calcular_total_carrito(carrito)
        assert total == 1525.0

    def test_calcular_total_carrito_con_descuentos_integracion_completa(
        self, tienda_con_productos
    ):
        """
        Flujo de Integración Completo:
        1. Tienda inicializada con productos base vía fixture.
        2. Se aplica un 10% de descuento a 'Laptop' (1200 -> 1080.0).
        3. Se aplica un 20% de descuento a 'Mouse' (25 -> 20.0).
        4. Se arma un carrito con ['Laptop', 'Mouse', 'Teclado'].
        5. Teclado mantiene su precio de lista (45.0).
        6. Total esperado: 1080.0 + 20.0 + 45.0 = 1145.0.
        """
        tienda_con_productos.aplicar_descuento("Laptop", 10.0)
        tienda_con_productos.aplicar_descuento("Mouse", 20.0)

        carrito = ["Laptop", "Mouse", "Teclado"]
        total = tienda_con_productos.calcular_total_carrito(carrito)

        assert total == 1145.0

    def test_calcular_total_carrito_producto_inexistente_lanza_excepcion(
        self, tienda_con_productos
    ):
        """Verifica que si el carrito contiene un producto inexistente, se lance excepción."""
        carrito = ["Laptop", "ProductoFantasma"]
        with pytest.raises(ProductoNoEncontradoError) as exc_info:
            tienda_con_productos.calcular_total_carrito(carrito)

        assert exc_info.value.nombre == "ProductoFantasma"
