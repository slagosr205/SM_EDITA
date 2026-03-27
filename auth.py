"""Módulo de autenticación elegante con control de acceso (RBAC)"""
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from database import get_connection
from styles import ElegantStyles

class LoginWindow:
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        self.S = ElegantStyles
        
        self.window = tk.Tk()
        self.window.title("Tienda Concepto - Iniciar Sesión")
        self.window.geometry("1000x650")
        self.window.resizable(False, False)
        
        self.center_window()
        ElegantStyles.configure_styles(self.window)
        self.create_widgets()
        
    def center_window(self):
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.window.winfo_screenheight() // 2) - (650 // 2)
        self.window.geometry(f"1000x650+{x}+{y}")
        
    def create_widgets(self):
        left_panel = tk.Frame(self.window, bg=self.S.COLORS["primary"], width=450)
        left_panel.pack(side="left", fill="both")
        left_panel.pack_propagate(False)
        
        tk.Label(left_panel, text="", bg=self.S.COLORS["primary"]).pack(expand=True)
        
        tk.Label(left_panel, text="TIENDA\nCONCEPTO", 
                font=("Segoe UI", 42, "bold"), 
                bg=self.S.COLORS["primary"], fg="white").pack(pady=(0, 20))
        
        tk.Label(left_panel, text="Sistema de Gestion Integral", 
                font=("Segoe UI", 14), 
                bg=self.S.COLORS["primary"], fg="#95a5a6").pack(pady=(0, 40))
        
        features = [
            (">", "Gestion de Proveedores"),
            ("[*]", "Control de Inventario"),
            ("[$]", "Punto de Venta"),
            ("[#]", "Reportes y Analytics"),
        ]
        
        for icon, text in features:
            tk.Label(left_panel, text=f"{icon}  {text}", 
                    font=("Segoe UI", 12), 
                    bg=self.S.COLORS["primary"], fg="#bdc3c7").pack(pady=8)
        
        tk.Label(left_panel, text="", bg=self.S.COLORS["primary"]).pack(expand=True)
        
        tk.Label(left_panel, text="v1.0 • 2026", 
                font=("Segoe UI", 9), 
                bg=self.S.COLORS["primary"], fg="#7f8c8d").pack(pady=20)
        
        tk.Button(left_panel, text="Acerca de / Licencia", 
                font=("Segoe UI", 9),
                bg=self.S.COLORS["primary"], fg="#7f8c8d",
                relief="flat", cursor="hand2",
                command=self.mostrar_licencia).pack(pady=5)
        
        right_panel = tk.Frame(self.window, bg=self.S.COLORS["bg_main"])
        right_panel.pack(side="right", fill="both", expand=True)
        
        login_card = tk.Frame(right_panel, bg="white", relief="flat")
        login_card.place(relx=0.5, rely=0.5, anchor="center")
        
        title_frame = tk.Frame(login_card, bg="white")
        title_frame.pack(fill="x", padx=50, pady=(40, 30))
        
        tk.Label(title_frame, text="¡Bienvenido!", 
                font=("Segoe UI", 28, "bold"), 
                bg="white", fg=self.S.COLORS["text_dark"]).pack(anchor="w")
        
        tk.Label(title_frame, text="Ingrese sus credenciales para continuar", 
                font=("Segoe UI", 11), 
                bg="white", fg=self.S.COLORS["text_light"]).pack(anchor="w", pady=(5, 0))
        
        form_frame = tk.Frame(login_card, bg="white")
        form_frame.pack(fill="x", padx=50, pady=20)
        
        tk.Label(form_frame, text="Correo electrónico", 
                font=("Segoe UI", 10, "bold"), 
                bg="white", fg=self.S.COLORS["text_dark"]).pack(anchor="w", pady=(15, 5))
        
        self.entry_usuario = ttk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        self.entry_usuario.pack(fill="x", ipady=10)
        self.entry_usuario.focus()
        
        tk.Label(form_frame, text="Contraseña", 
                font=("Segoe UI", 10, "bold"), 
                bg="white", fg=self.S.COLORS["text_dark"]).pack(anchor="w", pady=(20, 5))
        
        self.entry_password = ttk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        self.entry_password.pack(fill="x", ipady=10)
        self.entry_password.bind("<Return>", lambda e: self.verificar_login())
        
        self.btn_login = tk.Button(form_frame, text="Iniciar Sesion", 
                                  font=("Segoe UI", 13, "bold"),
                                  bg=self.S.COLORS["accent"], fg="white", 
                                  cursor="hand2", relief="flat",
                                  width=30, pady=10,
                                  command=self.verificar_login)
        self.btn_login.pack(pady=30)
        
        info_frame = tk.Frame(login_card, bg="#f8f9fa")
        info_frame.pack(fill="x", padx=50, pady=(0, 40))
        
        tk.Label(info_frame, text="Credenciales de prueba:", 
                font=("Segoe UI", 9), 
                bg="#f8f9fa", fg=self.S.COLORS["text_light"]).pack(pady=5)
        
        tk.Label(info_frame, text="admin@tienda.com / admin123", 
                font=("Segoe UI", 10, "bold"), 
                bg="#f8f9fa", fg=self.S.COLORS["accent"]).pack()
        
    def verificar_login(self):
        email = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        
        if not email or not password:
            self.show_error("Por favor, complete todos los campos")
            return
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_usuario, nombre, email, rol, id_proveedor_fk 
            FROM usuarios 
            WHERE email = ? AND password_hash = ? AND estado = 'activo'
        """, (email, password_hash))
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario:
            self.window.destroy()
            self.on_login_success({
                "id_usuario": usuario["id_usuario"],
                "nombre": usuario["nombre"],
                "email": usuario["email"],
                "rol": usuario["rol"],
                "id_proveedor_fk": usuario["id_proveedor_fk"]
            })
        else:
            self.show_error("Credenciales incorrectas. Verifique e intente nuevamente.")
            self.entry_password.delete(0, tk.END)
            self.entry_password.focus()
            
    def show_error(self, message):
        error_label = tk.Label(self.window, text=f"ERROR: {message}", 
                             font=("Segoe UI", 10), bg="#ffe6e6", 
                             fg="#c0392b", padx=15, pady=8)
        
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Label) and "ERROR:" in widget.cget("text", ""):
                widget.destroy()
                
        error_label.place(relx=0.7, rely=0.92, anchor="center")
        self.window.after(4000, error_label.destroy)
            
    def run(self):
        self.window.mainloop()
    
    def mostrar_licencia(self):
        about = tk.Toplevel(self.window)
        about.title("Acerca de - Tienda Concepto")
        about.geometry("550x450")
        about.configure(bg="white")
        about.transient(self.window)
        about.grab_set()
        
        screen_width = about.winfo_screenwidth()
        screen_height = about.winfo_screenheight()
        x = (screen_width // 2) - (550 // 2)
        y = (screen_height // 2) - (450 // 2)
        about.geometry(f"550x450+{x}+{y}")
        
        header = tk.Frame(about, bg=self.S.COLORS["primary"])
        header.pack(fill="x")
        
        tk.Label(header, text="TIENDA CONCEPTO", font=("Segoe UI", 20, "bold"),
                bg=self.S.COLORS["primary"], fg="white").pack(pady=20)
        tk.Label(header, text="Sistema de Gestion Integral", font=("Segoe UI", 11),
                bg=self.S.COLORS["primary"], fg="#95a5a6").pack(pady=(0, 15))
        
        card = tk.Frame(about, bg="white")
        card.pack(fill="both", expand=True, padx=30, pady=20)
        
        info_text = """
        VERSION
        1.0.0
        
        INFORMACION DEL SOFTWARE
        Tienda Concepto - Sistema de Gestion es un software
        propietario protegido por leyes de propiedad intelectual.
        
        LICENCIA
        Este es un software PROPIETARIO.
        © 2026 Tienda Concepto. Todos los derechos reservados.
        
        RESTRICCIONES DE USO
        • No esta permitido copiar, modificar o distribuir
        • No esta permitida la ingenieria inversa
        • No sublicenciar, arrendar o prestar el software
        • No eliminar los avisos de copyright
        
        CONTACTO
        Para soporte y consultas:
        Email: soporte@tiendaconcepto.com
        """
        
        tk.Label(card, text=info_text, font=("Segoe UI", 10),
                bg="white", fg=self.S.COLORS["text_dark"], justify="left", anchor="nw").pack(fill="both", expand=True)
        
        tk.Button(about, text="Cerrar", font=("Segoe UI", 11, "bold"),
                 bg=self.S.COLORS["primary"], fg="white", relief="flat",
                 cursor="hand2", padx=30, pady=10,
                 command=about.destroy).pack(pady=15)


class UserSession:
    _instance = None
    
    def __init__(self):
        self.usuario_actual = None
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = UserSession()
        return cls._instance
    
    def set_usuario(self, usuario):
        self.usuario_actual = usuario
        
    def get_usuario(self):
        return self.usuario_actual
    
    def get_rol(self):
        return self.usuario_actual["rol"] if self.usuario_actual else None
    
    def puede_acceder(self, modulo):
        rol = self.get_rol()
        permisos = {
            "admin": ["dashboard", "proveedores", "contratos", "espacios", "productos", 
                     "inventario", "surtido", "pos", "clientes", "liquidaciones", 
                     "reportes", "usuarios"],
            "supervisor": ["dashboard", "inventario", "surtido", "pos", "clientes", 
                          "liquidaciones", "reportes"],
            "cajero": ["pos", "inventario", "clientes"],
            "proveedor": ["inventario", "ventas", "liquidaciones"]
        }
        return modulo in permisos.get(rol, [])
    
    def logout(self):
        self.usuario_actual = None
