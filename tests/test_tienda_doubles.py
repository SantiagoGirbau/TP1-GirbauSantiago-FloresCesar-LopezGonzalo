"""
Suite de pruebas utilizando Dobles de Prueba (Test Doubles / Mocks).

Corresponde a la Sección 3:
- Uso de unittest.mock.MagicMock para aislar la unidad bajo prueba (Tienda).
- Verificación del cálculo de descuento sin requerir una instancia real de Producto.
- Verificación de la llamada e interacción exacta hacia actualizar_precio.
- Pruebas opcionales de agregar, buscar y eliminar con dobles (Dummy y Stub).
"""

import pytest
from unittest.mock import MagicMock, call
from tienda import Tienda
from producto import Producto
from excepciones import ProductoNoEncontradoError, DescuentoInvalidoError


class TestTiendaDoblesDePrueba:
    """
    Pruebas unitarias que aíslan la clase Tienda reemplazando la dependencia
    Producto por dobles de prueba (Mocks / Stubs / Dummies).
    """

    def test_aplicar_descuento_calcula_precio_y_llama_actualizar_precio(self):
        """
        Actividad práctica obligatoria Sección 3:
        Verifica que aplicar_descuento calcula correctamente el nuevo precio (150.0)
        a partir de un precio base (200.0) y un descuento (25%), e invoca
        actualizar_precio del producto sin usar una instancia real.
        """
        tienda = Tienda()

        # Doble de prueba: Mock que reemplaza a la clase Producto
        producto_mock = MagicMock(spec=Producto)
        producto_mock.nombre = "Monitor Gamer"
        producto_mock.precio = 200.0

        tienda.agregar_producto(producto_mock)

        # Ejecutamos la unidad bajo prueba
        tienda.aplicar_descuento("Monitor Gamer", 25.0)

        # Verificamos que se llamó exactamente una vez al método del doble con 150.0
        producto_mock.actualizar_precio.assert_called_once_with(150.0)

    @pytest.mark.parametrize(
        "precio_base, porcentaje, precio_esperado",
        [
            (100.0, 10.0, 90.0),
            (100.0, 50.0, 50.0),
            (100.0, 0.0, 100.0),    # Sin descuento
            (100.0, 100.0, 0.0),    # Descuento total (gratis)
            (33.33, 15.0, 28.33),   # Caso con decimales y redondeo
        ],
    )
    def test_aplicar_descuento_diferentes_porcentajes_con_mock(
        self, precio_base, porcentaje, precio_esperado
    ):
        """
        Verifica diversos porcentajes y cálculos de descuento con dobles parametrizados.
        """
        tienda = Tienda()
        mock_p = MagicMock(spec=Producto)
        mock_p.nombre = "ArticuloPrueba"
        mock_p.precio = precio_base

        tienda.agregar_producto(mock_p)
        tienda.aplicar_descuento("ArticuloPrueba", porcentaje)

        mock_p.actualizar_precio.assert_called_once_with(precio_esperado)

    def test_aplicar_descuento_porcentaje_invalido_no_modifica_producto(self):
        """
        Verifica que ante porcentajes inválidos (<0 o >100) se lance DescuentoInvalidoError
        y NO se invoque actualizar_precio en el producto simulado.
        """
        tienda = Tienda()
        mock_p = MagicMock(spec=Producto)
        mock_p.nombre = "Pendrive"
        mock_p.precio = 50.0
        tienda.agregar_producto(mock_p)

        with pytest.raises(DescuentoInvalidoError):
            tienda.aplicar_descuento("Pendrive", -10.0)

        with pytest.raises(DescuentoInvalidoError):
            tienda.aplicar_descuento("Pendrive", 150.0)

        # actualizar_precio nunca debió ser llamado
        mock_p.actualizar_precio.assert_not_called()

    def test_aplicar_descuento_producto_inexistente_lanza_excepcion(self):
        """
        Verifica que si el producto no existe en el inventario se lance excepción
        sin interactuar con ningún producto.
        """
        tienda = Tienda()
        with pytest.raises(ProductoNoEncontradoError):
            tienda.aplicar_descuento("Inexistente", 10.0)


# ==============================================================================
# ACTIVIDAD OPCIONAL SECCIÓN 3: Dobles para agregar, buscar y eliminar
# ==============================================================================
class TestTiendaOperacionesBasicasConDobles:
    """
    Demostración opcional del uso de dobles (Dummy / Stub) para verificar que
    Tienda gestiona el inventario independientemente de la implementación real de Producto.
    """

    def test_agregar_producto_con_dummy(self):
        """
        Utiliza un objeto simulado 'Dummy' (solo para ocupar espacio y ser almacenado).
        """
        tienda = Tienda()
        dummy_producto = MagicMock()
        dummy_producto.nombre = "ObjetoDummy"

        tienda.agregar_producto(dummy_producto)

        assert len(tienda.inventario) == 1
        assert tienda.inventario[0] is dummy_producto

    def test_buscar_producto_con_stub(self):
        """
        Utiliza un 'Stub' que responde con valores prefijados cuando se consulta.
        """
        tienda = Tienda()
        stub_producto = MagicMock()
        stub_producto.nombre = "ProductoStub"
        stub_producto.precio = 999.0

        tienda.agregar_producto(stub_producto)
        encontrado = tienda.buscar_producto("ProductoStub")

        assert encontrado is stub_producto
        assert encontrado.nombre == "ProductoStub"
        assert encontrado.precio == 999.0

    def test_eliminar_producto_con_double(self):
        """
        Verifica la eliminación utilizando un doble de prueba.
        """
        tienda = Tienda()
        double_producto = MagicMock()
        double_producto.nombre = "ParaEliminar"

        tienda.agregar_producto(double_producto)
        assert len(tienda.inventario) == 1

        resultado = tienda.eliminar_producto("ParaEliminar")
        assert resultado is True
        assert len(tienda.inventario) == 0
