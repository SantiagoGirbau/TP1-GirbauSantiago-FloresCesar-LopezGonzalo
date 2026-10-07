"""
Pruebas unitarias para la clase Producto.

Cubre:
- Sección 1: Creación básica y validación de atributos.
- Sección 2: Pruebas con excepciones (actualizar_precio con valores negativos
             e instanciación con precio inválido).
"""

import pytest
from producto import Producto
from excepciones import PrecioInvalidoError


class TestProductoBasico:
    """Pruebas unitarias correspondientes a la Sección 1."""

    def test_creacion_producto(self):
        """Verifica que un producto se instancie con los atributos correctos."""
        producto = Producto(nombre="Auriculares", precio=80.0, categoria="Audio")
        assert producto.nombre == "Auriculares"
        assert producto.precio == 80.0
        assert producto.categoria == "Audio"

    def test_representacion_cadena(self):
        """Verifica que __repr__ devuelva una cadena informativa y legible."""
        producto = Producto(nombre="Mouse", precio=25.0, categoria="Accesorios")
        esperado = "Producto(nombre='Mouse', precio=25.0, categoria='Accesorios')"
        assert repr(producto) == esperado

    def test_igualdad_entre_productos(self):
        """Verifica que dos productos con idénticos atributos sean considerados iguales."""
        p1 = Producto("Teclado", 45.0, "Accesorios")
        p2 = Producto("Teclado", 45.0, "Accesorios")
        p3 = Producto("Teclado Mecánico", 90.0, "Accesorios")

        assert p1 == p2
        assert p1 != p3
        assert p1 != "No soy un producto"


class TestProductoActualizarPrecioYExcepciones:
    """Pruebas unitarias correspondientes a la Sección 2."""

    def test_actualizar_precio_valido(self):
        """Verifica que el precio se actualice correctamente cuando el valor es positivo."""
        producto = Producto(nombre="Monitor", precio=300.0, categoria="Pantallas")
        producto.actualizar_precio(350.0)
        assert producto.precio == 350.0

    def test_actualizar_precio_a_cero(self):
        """Verifica que un precio de 0.0 (gratuito / promoción total) sea admitido."""
        producto = Producto(nombre="Folleto", precio=10.0, categoria="Papelería")
        producto.actualizar_precio(0.0)
        assert producto.precio == 0.0

    def test_actualizar_precio_negativo_lanza_excepcion(self):
        """
        Verifica que se lance PrecioInvalidoError (subclase de ValueError)
        al intentar actualizar a un precio negativo.
        """
        producto = Producto(nombre="Monitor", precio=300.0, categoria="Pantallas")
        with pytest.raises(PrecioInvalidoError) as exc_info:
            producto.actualizar_precio(-50.0)

        assert exc_info.value.precio == -50.0
        assert "El precio no puede ser negativo" in str(exc_info.value)
        # El precio original debe permanecer intacto tras el error
        assert producto.precio == 300.0

    def test_creacion_producto_precio_negativo_lanza_excepcion(self):
        """Verifica que no se permita instanciar un Producto con precio negativo."""
        with pytest.raises(PrecioInvalidoError):
            Producto(nombre="Invalido", precio=-15.0, categoria="General")
