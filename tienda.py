"""
Módulo Tienda.

Gestiona el inventario de productos y las operaciones comerciales
de la tienda: altas, bajas, búsquedas, aplicación de descuentos
y cálculo del total del carrito de compras.
"""

from typing import List
from producto import Producto
from excepciones import ProductoNoEncontradoError, DescuentoInvalidoError


class Tienda:
    """
    Clase que maneja el inventario y las operaciones de la tienda.

    Atributos:
        inventario (list): Lista de productos disponibles en la tienda.
    """

    def __init__(self):
        """Inicializa una tienda con un inventario vacío."""
        self.inventario: List[Producto] = []

    def agregar_producto(self, producto: Producto) -> None:
        """
        Agrega un producto al inventario de la tienda.

        Args:
            producto (Producto): Objeto producto a agregar.
        """
        self.inventario.append(producto)

    def buscar_producto(self, nombre: str) -> Producto:
        """
        Busca un producto en el inventario por su nombre.

        Args:
            nombre (str): Nombre del producto a buscar.

        Returns:
            Producto: El producto encontrado en el inventario.

        Raises:
            ProductoNoEncontradoError: Si el producto no se encuentra en el inventario.
        """
        for producto in self.inventario:
            if producto.nombre == nombre:
                return producto
        raise ProductoNoEncontradoError(nombre)

    def eliminar_producto(self, nombre: str) -> bool:
        """
        Elimina un producto del inventario por su nombre.

        Args:
            nombre (str): Nombre del producto a eliminar.

        Returns:
            bool: True si el producto fue eliminado exitosamente.

        Raises:
            ProductoNoEncontradoError: Si se intenta eliminar un producto que no existe.
        """
        for producto in self.inventario:
            if producto.nombre == nombre:
                self.inventario.remove(producto)
                return True
        raise ProductoNoEncontradoError(nombre)

    def aplicar_descuento(self, nombre: str, porcentaje: float) -> None:
        """
        Aplica un porcentaje de descuento a un producto existente en el inventario,
        calculando su nuevo precio e invocando su método actualizar_precio.

        Args:
            nombre (str): Nombre del producto al que se aplicará el descuento.
            porcentaje (float): Porcentaje de descuento (entre 0 y 100).

        Raises:
            ProductoNoEncontradoError: Si el producto no se encuentra en el inventario.
            DescuentoInvalidoError: Si el porcentaje está fuera del rango [0, 100].
        """
        if porcentaje < 0 or porcentaje > 100:
            raise DescuentoInvalidoError(porcentaje)

        producto = self.buscar_producto(nombre)
        descuento = producto.precio * (porcentaje / 100.0)
        nuevo_precio = round(producto.precio - descuento, 2)
        producto.actualizar_precio(nuevo_precio)

    def calcular_total_carrito(self, nombres_productos: List[str]) -> float:
        """
        Calcula el precio total de una lista de nombres de productos (el carrito).

        Args:
            nombres_productos (List[str]): Lista con los nombres de los productos.

        Returns:
            float: Suma total de los precios de los productos en el carrito (a 2 decimales).

        Raises:
            ProductoNoEncontradoError: Si alguno de los productos indicados no se encuentra en la tienda.
        """
        total = 0.0
        for nombre in nombres_productos:
            producto = self.buscar_producto(nombre)
            total += producto.precio
        return round(total, 2)
