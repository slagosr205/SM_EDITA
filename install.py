"""Instalador del Sistema Tienda Concepto"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tienda_concepto.db")

COLORS = {
    "primary": "#1e3a5f",
    "primary_light": "#2d5a87",
    "success": "#059669",
    "danger": "#dc2626",
    "warning": "#d97706",
    "bg_main": "#f1f5f9",
    "text_dark": "#1e293b",
    "text_medium": "#475569",
    "text_light": "#94a3b8",
}

class InstallerWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Instalador - Tienda Concepto")
        self.root.geometry("700x550")
        self.root.configure(bg=COLORS["bg_main"])
        self.root.resizable(False, False)
        
        self.center_window()
        
        self.current_step = 0
        self.steps = ["Bienvenida", "Configuracion", "Base de Datos", "Usuario Admin", "Finalizar"]
        
        self.config_data = {
            "nombre_tienda": "Tienda Concepto",
            "moneda_local": "HNL",
            "moneda_extranjera": "USD",
            "tasa_cambio": 24.50,
            "admin_nombre": "",
            "admin_email": "",
            "admin_password": "",
            "admin_password_confirm": ""
        }
        
        self.create_widgets()
        self.show_step(0)
        
        self.root.mainloop()
    
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.root.winfo_screenheight() // 2) - (550 // 2)
        self.root.geometry(f"700x550+{x}+{y}")
    
    def create_widgets(self):
        self.header = tk.Frame(self.root, bg=COLORS["primary"], height=80)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        
        tk.Label(self.header, text="INSTALADOR", font=("Segoe UI", 22, "bold"),
                bg=COLORS["primary"], fg="white").pack(pady=15)
        tk.Label(self.header, text="Sistema de Gestion Tienda Concepto",
                font=("Segoe UI", 10), bg=COLORS["primary"], fg="#94a3b8").pack()
        
        self.content_frame = tk.Frame(self.root, bg=COLORS["bg_main"])
        self.content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.footer = tk.Frame(self.root, bg="white", height=70)
        self.footer.pack(fill="x")
        self.footer.pack_propagate(False)
        
        self.btn_anterior = tk.Button(self.footer, text="Anterior", font=("Segoe UI", 11),
                                      bg="#e2e8f0", fg="#475569", relief="flat", cursor="hand2",
                                      padx=20, pady=10, command=self.anteriorPaso)
        self.btn_anterior.pack(side="left", padx=10, pady=15)
        
        self.btn_siguiente = tk.Button(self.footer, text="Siguiente", font=("Segoe UI", 11, "bold"),
                                      bg=COLORS["primary"], fg="white", relief="flat", cursor="hand2",
                                      padx=25, pady=10, command=self.siguientePaso)
        self.btn_siguiente.pack(side="right", padx=10, pady=15)
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_step(self, step):
        self.current_step = step
        self.clear_content()
        
        for widget in self.header.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == "INSTALADOR":
                continue
            widget.destroy()
        
        tk.Label(self.header, text=self.steps[step], font=("Segoe UI", 14, "bold"),
                bg=COLORS["primary"], fg="white").pack(pady=15)
        
        if step == 0:
            self.step_bienvenida()
        elif step == 1:
            self.step_configuracion()
        elif step == 2:
            self.step_base_datos()
        elif step == 3:
            self.step_usuario_admin()
        elif step == 4:
            self.step_finalizar()
        
        self.btn_anterior.config(state="normal" if step > 0 else "disabled")
        self.btn_siguiente.config(text="Siguiente" if step < len(self.steps) - 1 else "Finalizar")
    
    def step_bienvenida(self):
        card = tk.Frame(self.content_frame, bg="white")
        card.pack(fill="both", expand=True)
        
        shadow = tk.Frame(card, bg="#d1d5db")
        shadow.pack(padx=3, pady=3, fill="both", expand=True)
        
        inner = tk.Frame(shadow, bg="white")
        inner.pack(padx=2, pady=2, fill="both", expand=True)
        
        tk.Label(inner, text="Bienvenido al Instalador", font=("Segoe UI", 20, "bold"),
                bg="white", fg=COLORS["text_dark"]).pack(pady=(30, 10))
        
        tk.Label(inner, text="Sistema de Gestion Tienda Concepto",
                font=("Segoe UI", 14), bg="white", fg=COLORS["text_medium"]).pack()
        
        info_frame = tk.Frame(inner, bg="#f8fafc", padx=20, pady=15)
        info_frame.pack(pady=30, padx=40)
        
        tk.Label(info_frame, text="Este asistente le ayudara a configurar el sistema.",
                font=("Segoe UI", 11), bg="#f8fafc", fg=COLORS["text_medium"]).pack(pady=3)
        tk.Label(info_frame, text="El proceso incluye:", font=("Segoe UI", 11, "bold"),
                bg="#f8fafc", fg=COLORS["text_dark"]).pack(pady=(10, 5))
        
        pasos = [
            "1. Configuracion general del sistema",
            "2. Creacion de la base de datos",
            "3. Creacion del usuario administrador",
            "4. Verificacion final"
        ]
        for paso in pasos:
            tk.Label(info_frame, text=paso, font=("Segoe UI", 10),
                    bg="#f8fafc", fg=COLORS["text_medium"]).pack(anchor="w", pady=2)
        
        tk.Label(inner, text="Haga clic en 'Siguiente' para comenzar.",
                font=("Segoe UI", 11), bg="white", fg=COLORS["success"]).pack(pady=20)
    
    def step_configuracion(self):
        card = tk.Frame(self.content_frame, bg="white")
        card.pack(fill="both", expand=True)
        
        shadow = tk.Frame(card, bg="#d1d5db")
        shadow.pack(padx=3, pady=3, fill="both", expand=True)
        
        inner = tk.Frame(shadow, bg="white")
        inner.pack(padx=2, pady=2, fill="both", expand=True)
        
        tk.Label(inner, text="Configuracion General", font=("Segoe UI", 18, "bold"),
                bg="white", fg=COLORS["text_dark"]).pack(pady=(20, 5))
        tk.Label(inner, text="Configure los parametros basicos del sistema",
                font=("Segoe UI", 10), bg="white", fg=COLORS["text_medium"]).pack()
        
        form = tk.Frame(inner, bg="white")
        form.pack(pady=20, padx=40, fill="x")
        
        self.nombre_tienda_var = tk.StringVar(value=self.config_data["nombre_tienda"])
        self.tasa_cambio_var = tk.StringVar(value=str(self.config_data["tasa_cambio"]))
        
        row = tk.Frame(form, bg="white")
        row.pack(fill="x", pady=10)
        tk.Label(row, text="Nombre de la Tienda:", font=("Segoe UI", 11), bg="white", width=20, anchor="w").pack(side="left")
        ttk.Entry(row, textvariable=self.nombre_tienda_var, font=("Segoe UI", 11), width=30).pack(side="left", padx=10)
        
        row2 = tk.Frame(form, bg="white")
        row2.pack(fill="x", pady=10)
        tk.Label(row2, text="Moneda Local:", font=("Segoe UI", 11), bg="white", width=20, anchor="w").pack(side="left")
        ttk.Combobox(row2, values=["HNL - Lempira", "USD - Dolar", "EUR - Euro"], 
                    state="readonly", width=28, font=("Segoe UI", 11)).pack(side="left", padx=10)
        
        row3 = tk.Frame(form, bg="white")
        row3.pack(fill="x", pady=10)
        tk.Label(row3, text="Tasa de Cambio:", font=("Segoe UI", 11), bg="white", width=20, anchor="w").pack(side="left")
        ttk.Entry(row3, textvariable=self.tasa_cambio_var, font=("Segoe UI", 11), width=15).pack(side="left", padx=10)
        tk.Label(row3, text="USD", font=("Segoe UI", 11), bg="white", fg=COLORS["text_medium"]).pack(side="left")
    
    def step_base_datos(self):
        card = tk.Frame(self.content_frame, bg="white")
        card.pack(fill="both", expand=True)
        
        shadow = tk.Frame(card, bg="#d1d5db")
        shadow.pack(padx=3, pady=3, fill="both", expand=True)
        
        inner = tk.Frame(shadow, bg="white")
        inner.pack(padx=2, pady=2, fill="both", expand=True)
        
        tk.Label(inner, text="Base de Datos", font=("Segoe UI", 18, "bold"),
                bg="white", fg=COLORS["text_dark"]).pack(pady=(20, 5))
        tk.Label(inner, text="Se creara la base de datos del sistema",
                font=("Segoe UI", 10), bg="white", fg=COLORS["text_medium"]).pack()
        
        info_frame = tk.Frame(inner, bg="#f8fafc", padx=25, pady=20)
        info_frame.pack(pady=30, padx=40)
        
        self.db_status_label = tk.Label(info_frame, text="Estado: Verificando...",
                font=("Segoe UI", 12), bg="#f8fafc", fg=COLORS["text_medium"])
        self.db_status_label.pack(pady=5)
        
        db_path_label = tk.Label(info_frame, text=f"Ruta: {DB_PATH}",
                font=("Segoe UI", 9), bg="#f8fafc", fg=COLORS["text_light"])
        db_path_label.pack(pady=5)
        
        self.check_db_status()
    
    def check_db_status(self):
        if os.path.exists(DB_PATH):
            self.db_status_label.config(text="Estado: La base de datos ya existe",
                                      fg=COLORS["warning"])
        else:
            self.db_status_label.config(text="Estado: Se creara una nueva base de datos",
                                      fg=COLORS["success"])
    
    def step_usuario_admin(self):
        card = tk.Frame(self.content_frame, bg="white")
        card.pack(fill="both", expand=True)
        
        shadow = tk.Frame(card, bg="#d1d5db")
        shadow.pack(padx=3, pady=3, fill="both", expand=True)
        
        inner = tk.Frame(shadow, bg="white")
        inner.pack(padx=2, pady=2, fill="both", expand=True)
        
        tk.Label(inner, text="Usuario Administrador", font=("Segoe UI", 18, "bold"),
                bg="white", fg=COLORS["text_dark"]).pack(pady=(20, 5))
        tk.Label(inner, text="Cree las credenciales del administrador del sistema",
                font=("Segoe UI", 10), bg="white", fg=COLORS["text_medium"]).pack()
        
        form = tk.Frame(inner, bg="white")
        form.pack(pady=15, padx=40, fill="x")
        
        self.admin_nombre_var = tk.StringVar()
        self.admin_email_var = tk.StringVar()
        self.admin_password_var = tk.StringVar()
        self.admin_password_confirm_var = tk.StringVar()
        
        row = tk.Frame(form, bg="white")
        row.pack(fill="x", pady=8)
        tk.Label(row, text="Nombre Completo:", font=("Segoe UI", 11), bg="white", width=20, anchor="w").pack(side="left")
        ttk.Entry(row, textvariable=self.admin_nombre_var, font=("Segoe UI", 11), width=30).pack(side="left", padx=10)
        
        row2 = tk.Frame(form, bg="white")
        row2.pack(fill="x", pady=8)
        tk.Label(row2, text="Correo Electronico:", font=("Segoe UI", 11), bg="white", width=20, anchor="w").pack(side="left")
        ttk.Entry(row2, textvariable=self.admin_email_var, font=("Segoe UI", 11), width=30).pack(side="left", padx=10)
        
        row3 = tk.Frame(form, bg="white")
        row3.pack(fill="x", pady=8)
        tk.Label(row3, text="Contrasena:", font=("Segoe UI", 11), bg="white", width=20, anchor="w").pack(side="left")
        ttk.Entry(row3, textvariable=self.admin_password_var, font=("Segoe UI", 11), width=30, show="*").pack(side="left", padx=10)
        
        row4 = tk.Frame(form, bg="white")
        row4.pack(fill="x", pady=8)
        tk.Label(row4, text="Confirmar Clave:", font=("Segoe UI", 11), bg="white", width=20, anchor="w").pack(side="left")
        ttk.Entry(row4, textvariable=self.admin_password_confirm_var, font=("Segoe UI", 11), width=30, show="*").pack(side="left", padx=10)
        
        tk.Label(inner, text="La contrasena debe tener al menos 6 caracteres",
                font=("Segoe UI", 9), bg="white", fg=COLORS["text_light"]).pack(pady=(5, 0))
    
    def step_finalizar(self):
        card = tk.Frame(self.content_frame, bg="white")
        card.pack(fill="both", expand=True)
        
        shadow = tk.Frame(card, bg="#d1d5db")
        shadow.pack(padx=3, pady=3, fill="both", expand=True)
        
        inner = tk.Frame(shadow, bg="white")
        inner.pack(padx=2, pady=2, fill="both", expand=True)
        
        tk.Label(inner, text="Instalacion Completada", font=("Segoe UI", 20, "bold"),
                bg="white", fg=COLORS["success"]).pack(pady=(30, 10))
        
        success_frame = tk.Frame(inner, bg="#ecfdf5", padx=30, pady=20)
        success_frame.pack(pady=20, padx=40)
        
        tk.Label(success_frame, text="El sistema se ha instalado correctamente!",
                font=("Segoe UI", 12), bg="#ecfdf5", fg=COLORS["success"]).pack()
        
        tk.Label(inner, text="Resumen de la instalacion:",
                font=("Segoe UI", 11, "bold"), bg="white", fg=COLORS["text_dark"]).pack(pady=(20, 10))
        
        resumen = [
            f"Nombre de Tienda: {self.config_data['nombre_tienda']}",
            f"Moneda Local: {self.config_data['moneda_local']}",
            f"Tasa de Cambio: {self.config_data['tasa_cambio']}",
            f"Usuario Admin: {self.config_data['admin_email']}",
        ]
        
        for item in resumen:
            tk.Label(inner, text=f"  - {item}", font=("Segoe UI", 10),
                    bg="white", fg=COLORS["text_medium"]).pack(anchor="w", padx=80)
        
        tk.Label(inner, text="Haga clic en 'Finalizar' para iniciar el sistema.",
                font=("Segoe UI", 11), bg="white", fg=COLORS["primary"]).pack(pady=30)
    
    def anteriorPaso(self):
        if self.current_step > 0:
            self.show_step(self.current_step - 1)
    
    def siguientePaso(self):
        if self.current_step == 1:
            self.config_data["nombre_tienda"] = self.nombre_tienda_var.get()
            self.config_data["tasa_cambio"] = float(self.tasa_cambio_var.get())
        elif self.current_step == 2:
            pass
        elif self.current_step == 3:
            nombre = self.admin_nombre_var.get().strip()
            email = self.admin_email_var.get().strip()
            password = self.admin_password_var.get()
            password_confirm = self.admin_password_confirm_var.get()
            
            if not nombre:
                messagebox.showwarning("Campo requerido", "Ingrese el nombre del administrador")
                return
            if not email or "@" not in email:
                messagebox.showwarning("Campo requerido", "Ingrese un correo electronico valido")
                return
            if len(password) < 6:
                messagebox.showwarning("Contrasena invalida", "La contrasena debe tener al menos 6 caracteres")
                return
            if password != password_confirm:
                messagebox.showwarning("Contrasena no coincide", "Las contrasenas no coinciden")
                return
            
            self.config_data["admin_nombre"] = nombre
            self.config_data["admin_email"] = email
            self.config_data["admin_password"] = password
        elif self.current_step == 4:
            if self.config_data["admin_password"]:
                self.instalar()
            else:
                messagebox.showwarning("Datos incompletos", "Por favor complete los datos del administrador")
                self.show_step(3)
            return
        
        self.show_step(self.current_step + 1)
    
    def instalar(self):
        try:
            self.btn_siguiente.config(state="disabled", text="Instalando...")
            self.root.update()
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    rol TEXT NOT NULL CHECK(rol IN ('admin', 'supervisor', 'cajero', 'proveedor')),
                    id_proveedor_fk INTEGER,
                    estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo')),
                    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_proveedor_fk) REFERENCES proveedores(id_proveedor)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS monedas (
                    id_moneda INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    simbolo TEXT NOT NULL,
                    tipo TEXT DEFAULT 'local' CHECK(tipo IN ('local', 'extranjera')),
                    estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo'))
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS config_sistema (
                    id_config INTEGER PRIMARY KEY,
                    moneda_local TEXT DEFAULT 'HNL',
                    moneda_extranjera TEXT DEFAULT 'USD',
                    tasa_cambio REAL DEFAULT 24.50,
                    fecha_tasa TEXT,
                    nombre_tienda TEXT DEFAULT 'Tienda Concepto',
                    FOREIGN KEY (moneda_local) REFERENCES monedas(codigo),
                    FOREIGN KEY (moneda_extranjera) REFERENCES monedas(codigo)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proveedores (
                    id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    ruc_nit TEXT UNIQUE NOT NULL,
                    telefono TEXT,
                    email TEXT,
                    estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo')),
                    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contratos (
                    id_proveedor INTEGER NOT NULL,
                    fecha_inicio TEXT NOT NULL,
                    fecha_fin TEXT NOT NULL,
                    porcentaje_comision REAL NOT NULL,
                    condiciones TEXT,
                    estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'vencido', 'terminado')),
                    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS espacios_exhibicion (
                    id_espacio INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE NOT NULL,
                    descripcion TEXT,
                    ubicacion TEXT,
                    capacidad_max INTEGER DEFAULT 100,
                    estado TEXT DEFAULT 'disponible' CHECK(estado IN ('disponible', 'ocupado', 'mantenimiento'))
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_proveedor INTEGER NOT NULL,
                    nombre TEXT NOT NULL,
                    codigo_barras TEXT UNIQUE,
                    precio_venta REAL NOT NULL,
                    precio_costo REAL,
                    tipo_impuesto TEXT DEFAULT 'gravado' CHECK(tipo_impuesto IN ('gravado', 'exento', 'zero')),
                    estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo', 'agotado')),
                    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventarios (
                    id_inventario INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_producto INTEGER NOT NULL,
                    id_espacio INTEGER NOT NULL,
                    cant_actual INTEGER DEFAULT 0,
                    cant_minima INTEGER DEFAULT 5,
                    cant_maxima INTEGER DEFAULT 100,
                    f_ultimo_surtido TEXT,
                    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
                    FOREIGN KEY (id_espacio) REFERENCES espacios_exhibicion(id_espacio),
                    UNIQUE(id_producto, id_espacio)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT,
                    email TEXT,
                    telefono TEXT,
                    doc_identidad TEXT UNIQUE,
                    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cliente INTEGER,
                    id_usuario INTEGER NOT NULL,
                    fecha_venta TEXT DEFAULT CURRENT_TIMESTAMP,
                    subtotal REAL NOT NULL,
                    impuesto REAL NOT NULL,
                    total REAL NOT NULL,
                    metodo_pago TEXT,
                    estado TEXT DEFAULT 'completada' CHECK(estado IN ('completada', 'anulada', 'devuelta')),
                    referencia TEXT,
                    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detalle_venta (
                    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_venta INTEGER NOT NULL,
                    id_producto INTEGER NOT NULL,
                    id_espacio INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio_unit REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    tipo_impuesto TEXT DEFAULT 'gravado',
                    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
                    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
                    FOREIGN KEY (id_espacio) REFERENCES espacios_exhibicion(id_espacio)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS devoluciones (
                    id_devolucion INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_venta INTEGER NOT NULL,
                    id_usuario INTEGER NOT NULL,
                    fecha_devolucion TEXT DEFAULT CURRENT_TIMESTAMP,
                    cantidad INTEGER NOT NULL,
                    motivo TEXT,
                    estado TEXT DEFAULT 'completada',
                    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS planif_surtido (
                    id_planificacion INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_producto INTEGER NOT NULL,
                    id_espacio INTEGER NOT NULL,
                    fecha_planificada TEXT NOT NULL,
                    cant_solicitada INTEGER NOT NULL,
                    estado TEXT DEFAULT 'pendiente' CHECK(estado IN ('pendiente', 'aprobado', 'rechazado', 'ejecutado')),
                    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
                    FOREIGN KEY (id_espacio) REFERENCES espacios_exhibicion(id_espacio)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historial_inventario (
                    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_inventario INTEGER NOT NULL,
                    tipo_movimiento TEXT NOT NULL CHECK(tipo_movimiento IN ('entrada', 'salida', 'ajuste')),
                    cantidad INTEGER NOT NULL,
                    observaciones TEXT,
                    usuario INTEGER,
                    fecha_movimiento TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_inventario) REFERENCES inventarios(id_inventario),
                    FOREIGN KEY (usuario) REFERENCES usuarios(id_usuario)
                )
            """)
            
            cursor.execute("INSERT INTO monedas (codigo, nombre, simbolo, tipo) VALUES ('HNL', 'Lempira Hondureno', 'L', 'local')")
            cursor.execute("INSERT INTO monedas (codigo, nombre, simbolo, tipo) VALUES ('USD', 'Dolar Estadounidense', '$', 'extranjera')")
            
            cursor.execute("INSERT INTO config_sistema (moneda_local, moneda_extranjera, tasa_cambio, nombre_tienda) VALUES (?, ?, ?, ?)",
                          (self.config_data["moneda_local"], self.config_data["moneda_extranjera"], self.config_data["tasa_cambio"], self.config_data["nombre_tienda"]))
            
            import hashlib
            password_hash = hashlib.sha256(self.config_data["admin_password"].encode()).hexdigest()
            cursor.execute("INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES (?, ?, ?, 'admin')",
                          (self.config_data["admin_nombre"], self.config_data["admin_email"], password_hash))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Exito", "Sistema instalado correctamente!")
            self.root.destroy()
            self.iniciar_aplicacion()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la instalacion:\n{str(e)}")
            self.btn_siguiente.config(state="normal", text="Finalizar")
    
    def iniciar_aplicacion(self):
        from auth import LoginWindow
        
        def on_login_success(usuario):
            from main_window import MainWindow
            app = MainWindow(usuario)
            app.run()
        
        login = LoginWindow(on_login_success)
        login.run()

def is_installed():
    return os.path.exists(DB_PATH)

def run_installer():
    installer = InstallerWindow()

def main():
    if is_installed():
        from auth import LoginWindow
        
        def on_login_success(usuario):
            from main_window import MainWindow
            app = MainWindow(usuario)
            app.run()
        
        login = LoginWindow(on_login_success)
        login.run()
    else:
        run_installer()

if __name__ == "__main__":
    main()
