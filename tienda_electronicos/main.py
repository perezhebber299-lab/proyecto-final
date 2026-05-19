"""
main.py - Punto de entrada del sistema
CHATARRAS EL PANZON - Sistema de Gestión para Tienda de Electrónicos
Ejecutar: python main.py
Tecnologías: Python, Tkinter, Pandas, Matplotlib
"""
from gui import AplicacionPrincipal

def main():
    print("\n" + "=" * 60)
    print("  🔧 CHATARRAS EL PANZON")
    print("  Sistema de Gestión para Tienda de Electrónicos")
    print("  Tecnologías: Python | Tkinter | Pandas | Matplotlib")
    print("=" * 60)
    print("  Iniciando aplicación...\n")
    app = AplicacionPrincipal()
    app.ejecutar()
    print("\n[TERMINAL] 👋 Aplicación cerrada. ¡Hasta pronto!")

if __name__ == "__main__":
    main()
