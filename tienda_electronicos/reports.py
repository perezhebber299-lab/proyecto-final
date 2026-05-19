"""
reports.py - Generación de reportes con Pandas
Sistema de Gestión para Tienda de Electrónicos

Genera reportes que se muestran en la terminal de Visual Studio Code:
    - Productos más vendidos
    - Productos con bajo stock
    - Clientes con mayor número de compras
"""

import pandas as pd


class GeneradorReportes:
    """
    Clase para generar reportes de la tienda usando Pandas.
    
    Todos los reportes se imprimen en la terminal y retornan DataFrames
    para su uso en la interfaz gráfica.
    
    Atributos:
        db: Instancia de BaseDatos con los datos de la tienda
    """
    
    def __init__(self, db):
        """
        Inicializa el generador de reportes.
        
        Args:
            db: Instancia de BaseDatos
        """
        self.db = db
    
    def productos_mas_vendidos(self, top_n=10):
        """
        Genera un reporte de los productos más vendidos.
        
        Args:
            top_n (int): Número de productos a mostrar en el ranking
            
        Returns:
            pd.DataFrame: DataFrame con el ranking de productos más vendidos
        """
        ventas = self.db.obtener_ventas()
        
        if not ventas:
            print("\n[TERMINAL] ⚠️ No hay ventas registradas para generar el reporte.")
            return pd.DataFrame()
        
        # Crear DataFrame de ventas
        datos = [v.to_dict() for v in ventas]
        df = pd.DataFrame(datos)
        
        # Agrupar por producto y sumar cantidades
        reporte = df.groupby("producto_nombre").agg(
            total_vendido=("cantidad", "sum"),
            ingresos_totales=("total", "sum"),
            numero_ventas=("id", "count")
        ).sort_values("total_vendido", ascending=False).head(top_n)
        
        # Formatear ingresos
        reporte["ingresos_totales"] = reporte["ingresos_totales"].apply(lambda x: f"${x:,.2f}")
        
        # Renombrar columnas para mejor lectura
        reporte.columns = ["Unidades Vendidas", "Ingresos Totales", "Nº Ventas"]
        reporte.index.name = "Producto"
        
        # Imprimir en terminal
        print("\n" + "=" * 70)
        print("  📊 REPORTE: PRODUCTOS MÁS VENDIDOS")
        print("=" * 70)
        print(reporte.to_string())
        print("=" * 70)
        
        return reporte
    
    def productos_bajo_stock(self, umbral=10):
        """
        Genera un reporte de productos con stock bajo.
        
        Args:
            umbral (int): Cantidad mínima de stock para considerar "bajo"
            
        Returns:
            pd.DataFrame: DataFrame con productos de bajo stock
        """
        productos = self.db.obtener_productos()
        
        if not productos:
            print("\n[TERMINAL] ⚠️ No hay productos registrados.")
            return pd.DataFrame()
        
        # Crear DataFrame de productos
        datos = [p.to_dict() for p in productos]
        df = pd.DataFrame(datos)
        
        # Filtrar por stock bajo
        reporte = df[df["stock"] <= umbral][["nombre", "marca", "categoria", "stock", "precio"]]
        reporte = reporte.sort_values("stock", ascending=True)
        
        # Formatear precio
        reporte["precio"] = reporte["precio"].apply(lambda x: f"${x:,.2f}")
        
        # Renombrar columnas
        reporte.columns = ["Producto", "Marca", "Categoría", "Stock", "Precio"]
        reporte = reporte.reset_index(drop=True)
        reporte.index = reporte.index + 1  # Empezar índice desde 1
        
        # Imprimir en terminal
        print("\n" + "=" * 70)
        print(f"  ⚠️ REPORTE: PRODUCTOS CON BAJO STOCK (≤ {umbral} unidades)")
        print("=" * 70)
        if reporte.empty:
            print("  ✅ Todos los productos tienen stock suficiente.")
        else:
            print(reporte.to_string())
        print("=" * 70)
        
        return reporte
    
    def clientes_top(self, top_n=10):
        """
        Genera un reporte de los clientes con mayor número de compras.
        
        Args:
            top_n (int): Número de clientes a mostrar
            
        Returns:
            pd.DataFrame: DataFrame con el ranking de clientes
        """
        ventas = self.db.obtener_ventas()
        
        if not ventas:
            print("\n[TERMINAL] ⚠️ No hay ventas registradas para generar el reporte.")
            return pd.DataFrame()
        
        # Crear DataFrame de ventas
        datos = [v.to_dict() for v in ventas]
        df = pd.DataFrame(datos)
        
        # Agrupar por cliente
        reporte = df.groupby("cliente_nombre").agg(
            total_compras=("id", "count"),
            total_gastado=("total", "sum"),
            unidades_compradas=("cantidad", "sum")
        ).sort_values("total_compras", ascending=False).head(top_n)
        
        # Formatear valores monetarios
        reporte["total_gastado"] = reporte["total_gastado"].apply(lambda x: f"${x:,.2f}")
        
        # Renombrar columnas
        reporte.columns = ["Nº Compras", "Total Gastado", "Unidades Compradas"]
        reporte.index.name = "Cliente"
        
        # Imprimir en terminal
        print("\n" + "=" * 70)
        print("  👥 REPORTE: CLIENTES CON MAYOR NÚMERO DE COMPRAS")
        print("=" * 70)
        print(reporte.to_string())
        print("=" * 70)
        
        return reporte
    
    def resumen_general(self):
        """
        Genera un resumen general de la tienda.
        
        Returns:
            dict: Diccionario con estadísticas generales
        """
        productos = self.db.obtener_productos()
        clientes = self.db.obtener_clientes()
        ventas = self.db.obtener_ventas()
        
        total_productos = len(productos)
        total_clientes = len(clientes)
        total_ventas = len(ventas)
        
        ingresos_totales = sum(v.total for v in ventas)
        unidades_vendidas = sum(v.cantidad for v in ventas)
        valor_inventario = sum(p.precio * p.stock for p in productos)
        
        resumen = {
            "total_productos": total_productos,
            "total_clientes": total_clientes,
            "total_ventas": total_ventas,
            "ingresos_totales": ingresos_totales,
            "unidades_vendidas": unidades_vendidas,
            "valor_inventario": valor_inventario
        }
        
        print("\n" + "=" * 70)
        print("  📋 RESUMEN GENERAL DE LA TIENDA")
        print("=" * 70)
        print(f"  Productos registrados:    {total_productos}")
        print(f"  Clientes registrados:     {total_clientes}")
        print(f"  Ventas realizadas:        {total_ventas}")
        print(f"  Ingresos totales:         ${ingresos_totales:,.2f}")
        print(f"  Unidades vendidas:        {unidades_vendidas}")
        print(f"  Valor del inventario:     ${valor_inventario:,.2f}")
        print("=" * 70)
        
        return resumen
