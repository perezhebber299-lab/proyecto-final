"""
charts.py - Generación de gráficos con Matplotlib
Sistema de Gestión para Tienda de Electrónicos

Genera gráficos de análisis de datos:
    - Ventas por categoría de productos (gráfico de barras)
    - Tendencia de ventas a lo largo del tiempo (gráfico de líneas)
"""

import matplotlib
matplotlib.use('TkAgg')  # Backend compatible con Tkinter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd 
from datetime import datetime


class GeneradorGraficos:
    """
    Clase para generar gráficos de análisis de datos con Matplotlib.
    
    Los gráficos se muestran en ventanas emergentes de Matplotlib
    con estilos profesionales.
    
    Atributos:
        db: Instancia de BaseDatos con los datos de la tienda
    """
    
    def __init__(self, db):
        """
        Inicializa el generador de gráficos.
        
        Args:
            db: Instancia de BaseDatos
        """
        self.db = db
        # Estilo global para los gráficos
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def ventas_por_categoria(self):
        """
        Genera un gráfico de barras con las ventas agrupadas por categoría.
        
        Muestra:
            - Ingresos totales por categoría
            - Cantidad de unidades vendidas por categoría
        """
        ventas = self.db.obtener_ventas()
        
        if not ventas:
            print("[TERMINAL] ⚠️ No hay ventas para graficar.")
            return
        
        # Crear DataFrame
        datos = [v.to_dict() for v in ventas]
        df = pd.DataFrame(datos)
        
        # Agrupar por categoría
        por_categoria = df.groupby("categoria").agg(
            ingresos=("total", "sum"),
            unidades=("cantidad", "sum")
        ).sort_values("ingresos", ascending=True)
        
        # Crear figura con dos subgráficos
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle("📊 Análisis de Ventas por Categoría", fontsize=16, fontweight="bold", y=1.02)
        
        # Colores personalizados
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
        
        # --- Gráfico 1: Ingresos por categoría (barras horizontales) ---
        barras1 = ax1.barh(por_categoria.index, por_categoria["ingresos"], 
                           color=colores[:len(por_categoria)], edgecolor='white', linewidth=0.5)
        ax1.set_xlabel("Ingresos ($)", fontsize=11)
        ax1.set_title("Ingresos Totales por Categoría", fontsize=13, fontweight="bold", pad=10)
        
        # Etiquetas de valor en las barras
        for barra, valor in zip(barras1, por_categoria["ingresos"]):
            ax1.text(barra.get_width() + max(por_categoria["ingresos"]) * 0.01,
                     barra.get_y() + barra.get_height() / 2,
                     f"${valor:,.0f}", va="center", fontsize=9, fontweight="bold")
        
        ax1.set_xlim(0, max(por_categoria["ingresos"]) * 1.2)
        
        # --- Gráfico 2: Unidades por categoría (gráfico circular) ---
        wedges, texts, autotexts = ax2.pie(
            por_categoria["unidades"], 
            labels=por_categoria.index,
            autopct='%1.1f%%',
            colors=colores[:len(por_categoria)],
            startangle=90,
            explode=[0.05] * len(por_categoria),
            shadow=True
        )
        ax2.set_title("Distribución de Unidades Vendidas", fontsize=13, fontweight="bold", pad=10)
        
        # Estilo de los textos del pie
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight("bold")
        
        plt.tight_layout()
        
        print("[TERMINAL] 📊 Gráfico de ventas por categoría generado exitosamente.")
        plt.show()
    
    def tendencia_ventas(self):
        """
        Genera un gráfico de líneas con la tendencia de ventas en el tiempo.
        
        Muestra:
            - Ingresos diarios
            - Línea de tendencia
            - Promedio de ventas
        """
        ventas = self.db.obtener_ventas()
        
        if not ventas:
            print("[TERMINAL] ⚠️ No hay ventas para graficar.")
            return
        
        # Crear DataFrame
        datos = [v.to_dict() for v in ventas]
        df = pd.DataFrame(datos)
        df["fecha"] = pd.to_datetime(df["fecha"])
        
        # Agrupar por fecha
        por_fecha = df.groupby("fecha").agg(
            ingresos=("total", "sum"),
            unidades=("cantidad", "sum"),
            num_ventas=("id", "count")
        ).sort_index()
        
        # Crear figura con dos subgráficos
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        fig.suptitle("📈 Tendencia de Ventas a lo Largo del Tiempo", 
                     fontsize=16, fontweight="bold", y=1.02)
        
        # --- Gráfico 1: Ingresos en el tiempo ---
        ax1.fill_between(por_fecha.index, por_fecha["ingresos"], alpha=0.3, color='#4ECDC4')
        ax1.plot(por_fecha.index, por_fecha["ingresos"], 
                color='#4ECDC4', linewidth=2.5, marker='o', markersize=8, 
                markerfacecolor='white', markeredgecolor='#4ECDC4', markeredgewidth=2,
                label="Ingresos diarios")
        
        # Línea promedio
        promedio = por_fecha["ingresos"].mean()
        ax1.axhline(y=promedio, color='#FF6B6B', linestyle='--', linewidth=1.5, 
                    label=f"Promedio: ${promedio:,.0f}")
        
        ax1.set_ylabel("Ingresos ($)", fontsize=11)
        ax1.set_title("Ingresos Diarios", fontsize=13, fontweight="bold")
        ax1.legend(loc="upper left", fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Etiquetas de valor en puntos
        for fecha, ingreso in zip(por_fecha.index, por_fecha["ingresos"]):
            ax1.annotate(f"${ingreso:,.0f}", (fecha, ingreso),
                        textcoords="offset points", xytext=(0, 12),
                        fontsize=8, ha="center", fontweight="bold", color="#333")
        
        # --- Gráfico 2: Unidades vendidas ---
        ax2.bar(por_fecha.index, por_fecha["unidades"], 
               color='#45B7D1', alpha=0.7, width=0.8, edgecolor='white')
        ax2.set_xlabel("Fecha", fontsize=11)
        ax2.set_ylabel("Unidades Vendidas", fontsize=11)
        ax2.set_title("Unidades Vendidas por Día", fontsize=13, fontweight="bold")
        ax2.grid(True, alpha=0.3)
        
        # Etiquetas en barras
        for fecha, unidad in zip(por_fecha.index, por_fecha["unidades"]):
            ax2.text(fecha, unidad + 0.2, str(int(unidad)),
                    ha="center", fontsize=9, fontweight="bold", color="#333")
        
        # Formato de fechas
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        print("[TERMINAL] 📈 Gráfico de tendencia de ventas generado exitosamente.")
        plt.show()
    
    def comparativa_productos(self):
        """
        Genera un gráfico de barras comparando todos los productos por ingresos.
        """
        ventas = self.db.obtener_ventas()
        
        if not ventas:
            print("[TERMINAL] ⚠️ No hay ventas para graficar.")
            return
        
        # Crear DataFrame
        datos = [v.to_dict() for v in ventas]
        df = pd.DataFrame(datos)
        
        # Agrupar por producto
        por_producto = df.groupby("producto_nombre").agg(
            ingresos=("total", "sum"),
            unidades=("cantidad", "sum")
        ).sort_values("ingresos", ascending=True)
        
        # Crear gráfico
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
                   '#DDA0DD', '#98D8C8', '#F7DC6F']
        
        barras = ax.barh(por_producto.index, por_producto["ingresos"],
                        color=colores[:len(por_producto)], edgecolor='white', linewidth=0.5)
        
        # Etiquetas
        for barra, valor, unidades in zip(barras, por_producto["ingresos"], por_producto["unidades"]):
            ax.text(barra.get_width() + max(por_producto["ingresos"]) * 0.01,
                    barra.get_y() + barra.get_height() / 2,
                    f"${valor:,.0f} ({int(unidades)} uds)", 
                    va="center", fontsize=9, fontweight="bold")
        
        ax.set_xlabel("Ingresos Totales ($)", fontsize=11)
        ax.set_title("📊 Comparativa de Ingresos por Producto", fontsize=14, fontweight="bold")
        ax.set_xlim(0, max(por_producto["ingresos"]) * 1.25)
        
        plt.tight_layout()
        
        print("[TERMINAL] 📊 Gráfico comparativo de productos generado exitosamente.")
        plt.show()
