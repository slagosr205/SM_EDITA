"""
╔══════════════════════════════════════════════════════════════╗
║              SISTEMA DE GESTIÓN - TIENDA CONCEPTO            ║
║                  Prototipo Desktop Elegante                   ║
╚══════════════════════════════════════════════════════════════╝

Ejecución: python main.py
Usuario: admin@tienda.com
Contraseña: admin123
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_database, crear_usuario_admin, seed_data_ejemplo, inicializar_monedas
from auth import LoginWindow
from main_window import MainWindow

def main():
    print("===============================================")
    print("     SISTEMA DE GESTION - TIENDA CONCEPTO     ")
    print("===============================================")
    print()
    print("[*] Inicializando base de datos...")
    
    import os
    if os.path.exists("tienda_concepto.db"):
        os.remove("tienda_concepto.db")
    
    init_database()
    crear_usuario_admin()
    inicializar_monedas()
    seed_data_ejemplo()
    print("[OK] Base de datos lista.")
    print()
    print("[*] Iniciando aplicacion...")
    print()
    print("    +---------------------------------------------+")
    print("    |  Credenciales de prueba:                    |")
    print("    |  Usuario:    admin@tienda.com               |")
    print("    |  Contrasena: admin123                       |")
    print("    +---------------------------------------------+")
    print()
    
    def on_login_success(usuario):
        print(f"\n[OK] Bienvenido, {usuario['nombre']} ({usuario['rol']})")
        app = MainWindow(usuario)
        app.run()
        
    login = LoginWindow(on_login_success)
    login.run()
    
    print("\n[OK] Gracias por usar Tienda Concepto.")

if __name__ == "__main__":
    main()
