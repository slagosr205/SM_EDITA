"""
╔══════════════════════════════════════════════════════════════╗
║              SISTEMA DE GESTIÓN - TIENDA CONCEPTO            ║
║                  Prototipo Desktop Elegante                   ║
╚══════════════════════════════════════════════════════════════╝

Ejecución: python main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from install import is_installed, run_installer
from auth import LoginWindow
from main_window import MainWindow

def main():
    print("===============================================")
    print("     SISTEMA DE GESTION - TIENDA CONCEPTO     ")
    print("===============================================")
    print()
    
    if not is_installed():
        print("[*] Primera ejecucion detectada.")
        print("[*] Iniciando instalador...")
        run_installer()
    else:
        print("[*] Base de datos encontrada.")
        print("[*] Iniciando aplicacion...")
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
