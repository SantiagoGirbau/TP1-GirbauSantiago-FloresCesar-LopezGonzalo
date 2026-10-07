"""
Módulo Producto.

Define la entidad Producto y sus operaciones asociadas, incluyendo
la validación y actualización de su precio unitario.
"""

from excepciones import PrecioInvalidoError


class Producto:
    """
    Representa un producto dentro del catálogo de la tienda.

    Atributos:
        nombre (str): Nombre descriptivo del producto.
        precio (float): Precio unitario actual del producto.
        categoria (str): Categoría a la que pertenece el producto.
    """

    def __init__(self, nombre: str, precio: float, categoria: str):
        """
        Inicializa una nueva instancia de Producto.

        Args:
            nombre (str): Nombre del producto.
            precio (float): Precio unitario inicial (no puede ser negativo).
            categoria (str): Categoría del producto.

        Raises:
            PrecioInvalidoError: Si el precio proporcionado es negativo.
        """
        if precio < 0:
            raise PrecioInvalidoError(precio)
        self.nombre = nombre
        self.precio = float(precio)
        self.categoria = categoria

    def actualizar_precio(self, nuevo_precio: float) -> None:
        """
        Actualiza el precio unitario del producto.

        Args:
            nuevo_precio (float): Nuevo valor monetario a asignar.

        Raises:
            PrecioInvalidoError: Si el nuevo precio es negativo.
        """
        if nuevo_precio < 0:
            raise PrecioInvalidoError(nuevo_precio)
        self.precio = float(nuevo_precio)

    def __repr__(self) -> str:
        return f"Producto(nombre='{self.nombre}', precio={self.precio}, categoria='{self.categoria}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Producto):
            return False
        return (
            self.nombre == other.nombre
            and self.precio == other.precio
            and self.categoria == other.categoria
        )
