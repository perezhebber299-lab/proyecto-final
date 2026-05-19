"""
models.py - Modelos de datos (Programación Orientada a Objetos)
Sistema de Gestión para Tienda de Electrónicos

Clases:
    - Producto: Representa un producto electrónico en la tienda
    - Cliente: Representa un cliente registrado
    - Venta: Representa una transacción de venta
"""

from datetime import datetime


class Producto:
    """
    Clase que representa un producto electrónico en la tienda.
    
    Atributos:
        id (int): Identificador único del producto
        nombre (str): Nombre del producto
        marca (str): Marca del fabricante
        precio (float): Precio unitario en pesos
        categoria (str): Categoría del producto
        stock (int): Cantidad disponible en inventario
    """
    
    _contador_id = 0  # Contador estático para generar IDs automáticos
    
    def __init__(self, nombre, marca, precio, categoria, stock, id=None):
        if id is not None:
            self.id = id
            if id >= Producto._contador_id:
                Producto._contador_id = id + 1
        else:
            Producto._contador_id += 1
            self.id = Producto._contador_id
        
        self.nombre = nombre
        self.marca = marca
        self.precio = float(precio)
        self.categoria = categoria
        self.stock = int(stock)
    
    def to_dict(self):
        """Convierte el producto a un diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "marca": self.marca,
            "precio": self.precio,
            "categoria": self.categoria,
            "stock": self.stock
        }
    
    def actualizar_stock(self, cantidad):
        """
        Actualiza el stock del producto.
        
        Args:
            cantidad (int): Cantidad a agregar (positivo) o restar (negativo)
        
        Returns:
            bool: True si la operación fue exitosa, False si no hay suficiente stock
        """
        nuevo_stock = self.stock + cantidad
        if nuevo_stock < 0:
            return False
        self.stock = nuevo_stock
        return True
    
    def __str__(self):
        return (f"[ID:{self.id}] {self.nombre} | {self.marca} | "
                f"${self.precio:,.2f} | {self.categoria} | Stock: {self.stock}")
    
    def __repr__(self):
        return f"Producto('{self.nombre}', '{self.marca}', {self.precio}, '{self.categoria}', {self.stock})"


class Cliente:
    """
    Clase que representa un cliente registrado en la tienda.
    
    Atributos:
        id (int): Identificador único del cliente
        nombre (str): Nombre completo del cliente
        contacto (str): Teléfono o email de contacto
        direccion (str): Dirección del cliente
        historial_compras (list): Lista de IDs de ventas realizadas
    """
    
    _contador_id = 0
    
    def __init__(self, nombre, contacto, direccion, id=None):
        if id is not None:
            self.id = id
            if id >= Cliente._contador_id:
                Cliente._contador_id = id + 1
        else:
            Cliente._contador_id += 1
            self.id = Cliente._contador_id
        
        self.nombre = nombre
        self.contacto = contacto
        self.direccion = direccion
        self.historial_compras = []  # Lista de IDs de ventas
    
    def to_dict(self):
        """Convierte el cliente a un diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "contacto": self.contacto,
            "direccion": self.direccion,
            "total_compras": len(self.historial_compras)
        }
    
    def agregar_compra(self, venta_id):
        """
        Agrega una venta al historial de compras del cliente.
        
        Args:
            venta_id (int): ID de la venta realizada
        """
        self.historial_compras.append(venta_id)
    
    def __str__(self):
        return (f"[ID:{self.id}] {self.nombre} | {self.contacto} | "
                f"{self.direccion} | Compras: {len(self.historial_compras)}")
    
    def __repr__(self):
        return f"Cliente('{self.nombre}', '{self.contacto}', '{self.direccion}')"


class Venta:
    """
    Clase que representa una transacción de venta.
    
    Atributos:
        id (int): Identificador único de la venta
        fecha (str): Fecha de la venta (formato YYYY-MM-DD)
        producto_id (int): ID del producto vendido
        producto_nombre (str): Nombre del producto vendido
        cantidad (int): Cantidad vendida
        cliente_id (int): ID del cliente que realizó la compra
        cliente_nombre (str): Nombre del cliente
        precio_unitario (float): Precio unitario al momento de la venta
        total (float): Total de la venta (precio_unitario * cantidad)
        categoria (str): Categoría del producto vendido
    """
    
    _contador_id = 0
    
    def __init__(self, fecha, producto_id, producto_nombre, cantidad,
                 cliente_id, cliente_nombre, precio_unitario, categoria, id=None):
        if id is not None:
            self.id = id
            if id >= Venta._contador_id:
                Venta._contador_id = id + 1
        else:
            Venta._contador_id += 1
            self.id = Venta._contador_id
        
        self.fecha = fecha
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.cantidad = int(cantidad)
        self.cliente_id = cliente_id
        self.cliente_nombre = cliente_nombre
        self.precio_unitario = float(precio_unitario)
        self.total = self.precio_unitario * self.cantidad
        self.categoria = categoria
    
    def to_dict(self):
        """Convierte la venta a un diccionario."""
        return {
            "id": self.id,
            "fecha": self.fecha,
            "producto_id": self.producto_id,
            "producto_nombre": self.producto_nombre,
            "cantidad": self.cantidad,
            "cliente_id": self.cliente_id,
            "cliente_nombre": self.cliente_nombre,
            "precio_unitario": self.precio_unitario,
            "total": self.total,
            "categoria": self.categoria
        }
    
    def __str__(self):
        return (f"[ID:{self.id}] {self.fecha} | {self.producto_nombre} x{self.cantidad} | "
                f"Cliente: {self.cliente_nombre} | Total: ${self.total:,.2f}")
    
    def __repr__(self):
        return (f"Venta('{self.fecha}', {self.producto_id}, '{self.producto_nombre}', "
                f"{self.cantidad}, {self.cliente_id}, '{self.cliente_nombre}', "
                f"{self.precio_unitario}, '{self.categoria}')")
