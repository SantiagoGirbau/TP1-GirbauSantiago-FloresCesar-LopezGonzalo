"""
Módulo de excepciones personalizadas para el Sistema de Gestión de Tienda.

Define las excepciones del dominio del negocio para representar situaciones anómalas
como productos no encontrados, precios negativos y porcentajes de descuento fuera de rango.
"""


class TiendaError(Exception):
    """Excepción base para todos los errores de la tienda."""
    pass


class ProductoNoEncontradoError(TiendaError):
    """
    Lanzada cuando se intenta buscar o eliminar un producto que no existe
    en el inventario de la tienda.
    """
    def __init__(self, nombre: str):
        super().__init__(f"El producto '{nombre}' no se encuentra en el inventario.")
        self.nombre = nombre


class PrecioInvalidoError(ValueError):
    """
    Lanzada cuando se intenta asignar o actualizar el precio de un producto
    a un valor negativo. Hereda de ValueError para mantener compatibilidad semántica.
    """
    def __init__(self, precio: float):
        super().__init__(f"El precio no puede ser negativo: {precio}")
        self.precio = precio


class DescuentoInvalidoError(ValueError):
    """
    Lanzada cuando se intenta aplicar un porcentaje de descuento fuera del rango válido [0, 100].
    Hereda de ValueError.
    """
    def __init__(self, porcentaje: float):
        super().__init__(f"El porcentaje de descuento debe estar entre 0 y 100. Recibido: {porcentaje}%")
        self.porcentaje = porcentaje
