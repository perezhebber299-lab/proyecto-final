"""
database.py - Capa de datos y almacenamiento
Sistema de Gestión para Tienda de Electrónicos

Conectado a Supabase para persistencia de datos.

# ============================================================================
# INSTRUCCIONES PARA USAR ESTE ARCHIVO:
# ============================================================================
# 1. Instalar dependencias:
#       pip install supabase python-dotenv
#
# 2. Crear un archivo .env en la raíz del proyecto con:
#       SUPABASE_URL=https://yorrfotcdlzaigxhjqzx.supabase.co
#       SUPABASE_KEY=eyJ...  <-- tu anon key del dashboard de Supabase
#
# 3. En Supabase (Settings → API) copia la "anon public" key
#
# 4. Crear las tablas en Supabase con este SQL (SQL Editor):
#
# CREATE TABLE productos (
#     id SERIAL PRIMARY KEY,
#     nombre VARCHAR(100) NOT NULL,
#     marca VARCHAR(50) NOT NULL,
#     precio DECIMAL(10,2) NOT NULL,
#     categoria VARCHAR(50) NOT NULL,
#     stock INTEGER DEFAULT 0
# );
#
# CREATE TABLE clientes (
#     id SERIAL PRIMARY KEY,
#     nombre VARCHAR(100) NOT NULL,
#     contacto VARCHAR(100),
#     direccion VARCHAR(200)
# );
#
# CREATE TABLE ventas (
#     id SERIAL PRIMARY KEY,
#     fecha DATE NOT NULL,
#     producto_id INTEGER REFERENCES productos(id),
#     producto_nombre VARCHAR(100),
#     cantidad INTEGER NOT NULL,
#     cliente_id INTEGER REFERENCES clientes(id),
#     cliente_nombre VARCHAR(100),
#     precio_unitario DECIMAL(10,2),
#     total DECIMAL(10,2),
#     categoria VARCHAR(50)
# );
# ============================================================================
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from models import Producto, Cliente, Venta
from datetime import datetime, timedelta

# Cargar variables de entorno desde .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Faltan SUPABASE_URL o SUPABASE_KEY en el archivo .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class BaseDatos:
    """
    Clase que gestiona el almacenamiento de datos de la tienda.
    Conectada a Supabase para persistencia real de datos.
    """

    def __init__(self):
        print("=" * 60)
        print("  CONECTANDO CON SUPABASE...")
        print("=" * 60)
        self._cargar_datos_iniciales_si_vacio()

    # ========================================================================
    # DATOS INICIALES (solo se insertan si las tablas están vacías)
    # ========================================================================

    def _cargar_datos_iniciales_si_vacio(self):
        """Inserta datos de ejemplo en Supabase solo si las tablas están vacías."""

        productos_existentes = supabase.table("productos").select("id").execute()

        if productos_existentes.data:
            print(f"  → Base de datos ya tiene datos. No se insertan datos iniciales.")
            print("=" * 60)
            return

        print("  → Tablas vacías. Insertando datos iniciales...")

        # --- 8 Productos iniciales ---
        productos_iniciales = [
            {"nombre": "Laptop",                "marca": "HP",       "precio": 12999.00, "categoria": "Computadoras",   "stock": 15},
            {"nombre": "Mouse Gamer",            "marca": "Logitech", "precio": 899.00,   "categoria": "Periféricos",    "stock": 50},
            {"nombre": "Teclado Mecánico",       "marca": "Razer",    "precio": 1499.00,  "categoria": "Periféricos",    "stock": 30},
            {"nombre": "Monitor",                "marca": "Samsung",  "precio": 5499.00,  "categoria": "Pantallas",      "stock": 20},
            {"nombre": "Audífonos Inalámbricos", "marca": "Sony",     "precio": 2299.00,  "categoria": "Audio",          "stock": 25},
            {"nombre": "Memoria USB",            "marca": "Kingston", "precio": 199.00,   "categoria": "Almacenamiento", "stock": 100},
            {"nombre": "Disco Duro Externo",     "marca": "Seagate",  "precio": 1299.00,  "categoria": "Almacenamiento", "stock": 35},
            {"nombre": "Smartphone",             "marca": "Samsung",  "precio": 8999.00,  "categoria": "Móviles",        "stock": 18},
        ]
        supabase.table("productos").insert(productos_iniciales).execute()

        # --- 5 Clientes iniciales ---
        clientes_iniciales = [
            {"nombre": "Carlos García López",      "contacto": "carlos@email.com",  "direccion": "Av. Reforma 123, CDMX"},
            {"nombre": "María Fernández Ruiz",     "contacto": "maria@email.com",   "direccion": "Calle Juárez 456, Guadalajara"},
            {"nombre": "José Martínez Hernández",  "contacto": "jose@email.com",    "direccion": "Blvd. Independencia 789, Monterrey"},
            {"nombre": "Ana López Castillo",       "contacto": "ana@email.com",     "direccion": "Calle 5 de Mayo 101, Puebla"},
            {"nombre": "Roberto Sánchez Díaz",     "contacto": "roberto@email.com", "direccion": "Av. Universidad 202, Querétaro"},
        ]
        supabase.table("clientes").insert(clientes_iniciales).execute()

        # Obtener IDs reales asignados por Supabase
        prods = supabase.table("productos").select("id,nombre").execute().data
        clientes = supabase.table("clientes").select("id,nombre").execute().data

        prod_map = {p["nombre"]: p["id"] for p in prods}
        cli_map  = {c["nombre"]: c["id"] for c in clientes}

        hoy = datetime.now()
        ventas_iniciales = [
            {"fecha": (hoy - timedelta(days=28)).strftime("%Y-%m-%d"), "producto_id": prod_map["Laptop"],                "producto_nombre": "Laptop",                "cantidad": 2,  "cliente_id": cli_map["Carlos García López"],     "cliente_nombre": "Carlos García López",     "precio_unitario": 12999.00, "total": 25998.00, "categoria": "Computadoras"},
            {"fecha": (hoy - timedelta(days=25)).strftime("%Y-%m-%d"), "producto_id": prod_map["Mouse Gamer"],           "producto_nombre": "Mouse Gamer",           "cantidad": 5,  "cliente_id": cli_map["María Fernández Ruiz"],    "cliente_nombre": "María Fernández Ruiz",    "precio_unitario": 899.00,   "total": 4495.00,  "categoria": "Periféricos"},
            {"fecha": (hoy - timedelta(days=22)).strftime("%Y-%m-%d"), "producto_id": prod_map["Teclado Mecánico"],      "producto_nombre": "Teclado Mecánico",      "cantidad": 3,  "cliente_id": cli_map["Carlos García López"],     "cliente_nombre": "Carlos García López",     "precio_unitario": 1499.00,  "total": 4497.00,  "categoria": "Periféricos"},
            {"fecha": (hoy - timedelta(days=20)).strftime("%Y-%m-%d"), "producto_id": prod_map["Audífonos Inalámbricos"],"producto_nombre": "Audífonos Inalámbricos","cantidad": 4,  "cliente_id": cli_map["José Martínez Hernández"], "cliente_nombre": "José Martínez Hernández", "precio_unitario": 2299.00,  "total": 9196.00,  "categoria": "Audio"},
            {"fecha": (hoy - timedelta(days=18)).strftime("%Y-%m-%d"), "producto_id": prod_map["Smartphone"],            "producto_nombre": "Smartphone",            "cantidad": 1,  "cliente_id": cli_map["Ana López Castillo"],      "cliente_nombre": "Ana López Castillo",      "precio_unitario": 8999.00,  "total": 8999.00,  "categoria": "Móviles"},
            {"fecha": (hoy - timedelta(days=15)).strftime("%Y-%m-%d"), "producto_id": prod_map["Monitor"],               "producto_nombre": "Monitor",               "cantidad": 2,  "cliente_id": cli_map["María Fernández Ruiz"],    "cliente_nombre": "María Fernández Ruiz",    "precio_unitario": 5499.00,  "total": 10998.00, "categoria": "Pantallas"},
            {"fecha": (hoy - timedelta(days=12)).strftime("%Y-%m-%d"), "producto_id": prod_map["Memoria USB"],           "producto_nombre": "Memoria USB",           "cantidad": 10, "cliente_id": cli_map["Roberto Sánchez Díaz"],    "cliente_nombre": "Roberto Sánchez Díaz",    "precio_unitario": 199.00,   "total": 1990.00,  "categoria": "Almacenamiento"},
            {"fecha": (hoy - timedelta(days=10)).strftime("%Y-%m-%d"), "producto_id": prod_map["Disco Duro Externo"],    "producto_nombre": "Disco Duro Externo",    "cantidad": 3,  "cliente_id": cli_map["José Martínez Hernández"], "cliente_nombre": "José Martínez Hernández", "precio_unitario": 1299.00,  "total": 3897.00,  "categoria": "Almacenamiento"},
            {"fecha": (hoy - timedelta(days=8)).strftime("%Y-%m-%d"),  "producto_id": prod_map["Laptop"],                "producto_nombre": "Laptop",                "cantidad": 1,  "cliente_id": cli_map["Roberto Sánchez Díaz"],    "cliente_nombre": "Roberto Sánchez Díaz",    "precio_unitario": 12999.00, "total": 12999.00, "categoria": "Computadoras"},
            {"fecha": (hoy - timedelta(days=5)).strftime("%Y-%m-%d"),  "producto_id": prod_map["Mouse Gamer"],           "producto_nombre": "Mouse Gamer",           "cantidad": 8,  "cliente_id": cli_map["Carlos García López"],     "cliente_nombre": "Carlos García López",     "precio_unitario": 899.00,   "total": 7192.00,  "categoria": "Periféricos"},
            {"fecha": (hoy - timedelta(days=3)).strftime("%Y-%m-%d"),  "producto_id": prod_map["Teclado Mecánico"],      "producto_nombre": "Teclado Mecánico",      "cantidad": 2,  "cliente_id": cli_map["Ana López Castillo"],      "cliente_nombre": "Ana López Castillo",      "precio_unitario": 1499.00,  "total": 2998.00,  "categoria": "Periféricos"},
            {"fecha": (hoy - timedelta(days=1)).strftime("%Y-%m-%d"),  "producto_id": prod_map["Smartphone"],            "producto_nombre": "Smartphone",            "cantidad": 3,  "cliente_id": cli_map["María Fernández Ruiz"],    "cliente_nombre": "María Fernández Ruiz",    "precio_unitario": 8999.00,  "total": 26997.00, "categoria": "Móviles"},
        ]
        supabase.table("ventas").insert(ventas_iniciales).execute()

        print(f"  → 8 productos, 5 clientes y 12 ventas insertados correctamente.")
        print("=" * 60)

    # ========================================================================
    # CRUD DE PRODUCTOS
    # ========================================================================

    def agregar_producto(self, nombre, marca, precio, categoria, stock):
        """Agrega un nuevo producto en Supabase."""
        data = supabase.table("productos").insert({
            "nombre": nombre,
            "marca": marca,
            "precio": precio,
            "categoria": categoria,
            "stock": stock
        }).execute()
        p = data.data[0]
        producto = Producto(p["nombre"], p["marca"], p["precio"], p["categoria"], p["stock"], id=p["id"])
        print(f"[TERMINAL] ✅ Producto agregado: {producto}")
        return producto

    def obtener_productos(self):
        """Retorna todos los productos desde Supabase."""
        data = supabase.table("productos").select("*").execute()
        return [Producto(p["nombre"], p["marca"], p["precio"], p["categoria"], p["stock"], id=p["id"]) for p in data.data]

    def obtener_producto_por_id(self, producto_id):
        """Busca un producto por su ID en Supabase."""
        data = supabase.table("productos").select("*").eq("id", producto_id).execute()
        if data.data:
            p = data.data[0]
            return Producto(p["nombre"], p["marca"], p["precio"], p["categoria"], p["stock"], id=p["id"])
        return None

    def actualizar_producto(self, producto_id, nombre=None, marca=None,
                            precio=None, categoria=None, stock=None):
        """Actualiza los datos de un producto en Supabase."""
        updates = {}
        if nombre:           updates["nombre"]    = nombre
        if marca:            updates["marca"]     = marca
        if precio:           updates["precio"]    = precio
        if categoria:        updates["categoria"] = categoria
        if stock is not None: updates["stock"]   = stock

        if updates:
            supabase.table("productos").update(updates).eq("id", producto_id).execute()
            print(f"[TERMINAL] ✏️ Producto {producto_id} actualizado: {updates}")
            return True
        return False

    def eliminar_producto(self, producto_id):
        """Elimina un producto por su ID en Supabase."""
        producto = self.obtener_producto_por_id(producto_id)
        if producto:
            supabase.table("productos").delete().eq("id", producto_id).execute()
            print(f"[TERMINAL] 🗑️ Producto eliminado: {producto.nombre}")
            return True
        return False

    # ========================================================================
    # CRUD DE CLIENTES
    # ========================================================================

    def agregar_cliente(self, nombre, contacto, direccion):
        """Agrega un nuevo cliente en Supabase."""
        data = supabase.table("clientes").insert({
            "nombre": nombre,
            "contacto": contacto,
            "direccion": direccion
        }).execute()
        c = data.data[0]
        cliente = Cliente(c["nombre"], c["contacto"], c["direccion"], id=c["id"])
        print(f"[TERMINAL] ✅ Cliente agregado: {cliente}")
        return cliente

    def obtener_clientes(self):
        """Retorna todos los clientes desde Supabase."""
        data = supabase.table("clientes").select("*").execute()
        return [Cliente(c["nombre"], c["contacto"], c["direccion"], id=c["id"]) for c in data.data]

    def obtener_cliente_por_id(self, cliente_id):
        """Busca un cliente por su ID en Supabase."""
        data = supabase.table("clientes").select("*").eq("id", cliente_id).execute()
        if data.data:
            c = data.data[0]
            return Cliente(c["nombre"], c["contacto"], c["direccion"], id=c["id"])
        return None

    def actualizar_cliente(self, cliente_id, nombre=None, contacto=None, direccion=None):
        """Actualiza los datos de un cliente en Supabase."""
        updates = {}
        if nombre:    updates["nombre"]    = nombre
        if contacto:  updates["contacto"]  = contacto
        if direccion: updates["direccion"] = direccion

        if updates:
            supabase.table("clientes").update(updates).eq("id", cliente_id).execute()
            print(f"[TERMINAL] ✏️ Cliente {cliente_id} actualizado: {updates}")
            return True
        return False

    def eliminar_cliente(self, cliente_id):
        """Elimina un cliente por su ID en Supabase."""
        cliente = self.obtener_cliente_por_id(cliente_id)
        if cliente:
            supabase.table("clientes").delete().eq("id", cliente_id).execute()
            print(f"[TERMINAL] 🗑️ Cliente eliminado: {cliente.nombre}")
            return True
        return False

    # ========================================================================
    # GESTIÓN DE VENTAS
    # ========================================================================

    def registrar_venta(self, producto_id, cantidad, cliente_id):
        """Registra una nueva venta en Supabase y actualiza el stock."""
        producto = self.obtener_producto_por_id(producto_id)
        cliente  = self.obtener_cliente_por_id(cliente_id)

        if not producto:
            print(f"[TERMINAL] ❌ Error: Producto con ID {producto_id} no encontrado")
            return None
        if not cliente:
            print(f"[TERMINAL] ❌ Error: Cliente con ID {cliente_id} no encontrado")
            return None
        if producto.stock < cantidad:
            print(f"[TERMINAL] ❌ Error: Stock insuficiente. Disponible: {producto.stock}, Solicitado: {cantidad}")
            return None

        total = producto.precio * cantidad
        fecha = datetime.now().strftime("%Y-%m-%d")

        # Insertar venta
        data = supabase.table("ventas").insert({
            "fecha":           fecha,
            "producto_id":     producto_id,
            "producto_nombre": producto.nombre,
            "cantidad":        cantidad,
            "cliente_id":      cliente_id,
            "cliente_nombre":  cliente.nombre,
            "precio_unitario": producto.precio,
            "total":           total,
            "categoria":       producto.categoria
        }).execute()

        # Actualizar stock en Supabase
        nuevo_stock = producto.stock - cantidad
        supabase.table("productos").update({"stock": nuevo_stock}).eq("id", producto_id).execute()

        v = data.data[0]
        venta = Venta(v["fecha"], v["producto_id"], v["producto_nombre"], v["cantidad"],
                      v["cliente_id"], v["cliente_nombre"], v["precio_unitario"], v["categoria"], id=v["id"])

        print(f"[TERMINAL] 💰 Venta registrada: {venta}")
        print(f"[TERMINAL]    Stock actualizado de '{producto.nombre}': {producto.stock} → {nuevo_stock}")
        return venta

    def obtener_ventas(self):
        """Retorna todas las ventas desde Supabase ordenadas por fecha."""
        data = supabase.table("ventas").select("*").order("fecha", desc=True).execute()
        return [Venta(v["fecha"], v["producto_id"], v["producto_nombre"], v["cantidad"],
                      v["cliente_id"], v["cliente_nombre"], v["precio_unitario"], v["categoria"], id=v["id"])
                for v in data.data]

    # ========================================================================
    # GESTIÓN DE INVENTARIO
    # ========================================================================

    def entrada_inventario(self, producto_id, cantidad):
        """Registra una entrada de inventario (aumenta stock) en Supabase."""
        producto = self.obtener_producto_por_id(producto_id)
        if producto:
            nuevo_stock = producto.stock + cantidad
            supabase.table("productos").update({"stock": nuevo_stock}).eq("id", producto_id).execute()
            print(f"[TERMINAL] 📦 Entrada de inventario: {producto.nombre} | {producto.stock} → {nuevo_stock} (+{cantidad})")
            return True
        return False

    def salida_inventario(self, producto_id, cantidad):
        """Registra una salida de inventario (disminuye stock) en Supabase."""
        producto = self.obtener_producto_por_id(producto_id)
        if producto:
            if producto.stock < cantidad:
                print(f"[TERMINAL] ❌ Error: Stock insuficiente para salida")
                return False
            nuevo_stock = producto.stock - cantidad
            supabase.table("productos").update({"stock": nuevo_stock}).eq("id", producto_id).execute()
            print(f"[TERMINAL] 📤 Salida de inventario: {producto.nombre} | {producto.stock} → {nuevo_stock} (-{cantidad})")
            return True
        return False

    def obtener_categorias(self):
        """Retorna una lista de categorías únicas de productos desde Supabase."""
        data = supabase.table("productos").select("categoria").execute()
        categorias = set(p["categoria"] for p in data.data)
        return sorted(list(categorias))

    # ========================================================================
    # BÚSQUEDA AVANZADA
    # ========================================================================

    def buscar_productos(self, termino="", campo="nombre"):
        """Búsqueda avanzada de productos en Supabase."""
        if campo == "precio":
            try:
                data = supabase.table("productos").select("*").lte("precio", float(termino)).execute()
            except ValueError:
                return []
        else:
            data = supabase.table("productos").select("*").ilike(campo, f"%{termino}%").execute()

        resultados = [Producto(p["nombre"], p["marca"], p["precio"], p["categoria"], p["stock"], id=p["id"]) for p in data.data]
        print(f"[TERMINAL] 🔍 Búsqueda de productos - Campo: {campo}, Término: '{termino}' → {len(resultados)} resultados")
        return resultados

    def buscar_clientes(self, termino=""):
        """Busca clientes por nombre en Supabase."""
        data = supabase.table("clientes").select("*").ilike("nombre", f"%{termino}%").execute()
        resultados = [Cliente(c["nombre"], c["contacto"], c["direccion"], id=c["id"]) for c in data.data]
        print(f"[TERMINAL] 🔍 Búsqueda de clientes - Término: '{termino}' → {len(resultados)} resultados")
        return resultados

    def buscar_ventas_por_cliente(self, cliente_id):
        """Retorna todas las ventas de un cliente específico desde Supabase."""
        data = supabase.table("ventas").select("*").eq("cliente_id", cliente_id).execute()
        return [Venta(v["fecha"], v["producto_id"], v["producto_nombre"], v["cantidad"],
                      v["cliente_id"], v["cliente_nombre"], v["precio_unitario"], v["categoria"], id=v["id"])
                for v in data.data]
