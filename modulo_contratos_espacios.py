"""Módulo de Contratos y Espacios"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from datetime import datetime, timedelta
from styles import ElegantStyles

class ContratosEspaciosWindow:
    def __init__(self, parent):
        self.S = ElegantStyles
        self.window = tk.Toplevel(parent)
        self.window.title("Contratos y Espacios")
        self.window.geometry("1050x600")
        
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.tab_contratos = tk.Frame(self.notebook, bg=self.S.COLORS["bg_main"])
        self.tab_espacios = tk.Frame(self.notebook, bg=self.S.COLORS["bg_main"])
        
        self.notebook.add(self.tab_contratos, text="  Contratos  ")
        self.notebook.add(self.tab_espacios, text="  Espacios  ")
        
        self.create_tab_contratos()
        self.create_tab_espacios()
        
    def create_tab_contratos(self):
        toolbar = tk.Frame(self.tab_contratos, bg="white", height=50)
        toolbar.pack(fill="x")
        
        btn_frame = tk.Frame(toolbar, bg="white")
        btn_frame.pack(side="right", padx=15)
        
        tk.Button(btn_frame, text="+ Nuevo", font=("Segoe UI", 9, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", 
                 cursor="hand2", padx=15, pady=5, command=self.nuevo_contrato).pack(side="left", padx=3)
        
        card = tk.Frame(self.tab_contratos, bg="white")
        card.pack(fill="both", expand=True, padx=15, pady=10)
        
        columns = ("ID", "Proveedor", "Fecha Inicio", "Fecha Fin", "Comision", "Estado")
        self.tree_contratos = ttk.Treeview(card, columns=columns, show="headings", height=18)
        
        for col in columns:
            self.tree_contratos.heading(col, text=col)
            self.tree_contratos.column(col, width=140 if col != "ID" else 50)
        
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.tree_contratos.yview)
        self.tree_contratos.configure(yscrollcommand=scrollbar.set)
        self.tree_contratos.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        self.cargar_contratos()
        
    def create_tab_espacios(self):
        toolbar = tk.Frame(self.tab_espacios, bg="white", height=50)
        toolbar.pack(fill="x")
        
        tk.Button(toolbar, text="+ Nuevo Espacio", font=("Segoe UI", 9, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", 
                 cursor="hand2", padx=15, pady=5, command=self.nuevo_espacio).pack(side="right", padx=15)
        
        card = tk.Frame(self.tab_espacios, bg="white")
        card.pack(fill="both", expand=True, padx=15, pady=10)
        
        columns = ("ID", "Codigo", "Descripcion", "Ubicacion", "Capacidad", "Estado")
        self.tree_espacios = ttk.Treeview(card, columns=columns, show="headings", height=18)
        
        for col in columns:
            self.tree_espacios.heading(col, text=col)
            self.tree_espacios.column(col, width=150 if col not in ("ID", "Capacidad") else 80)
        self.tree_espacios.column("ID", width=50)
        
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.tree_espacios.yview)
        self.tree_espacios.configure(yscrollcommand=scrollbar.set)
        self.tree_espacios.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        self.cargar_espacios()
        
    def cargar_contratos(self):
        for item in self.tree_contratos.get_children():
            self.tree_contratos.delete(item)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id_contrato, p.nombre as proveedor, c.fecha_inicio, c.fecha_fin,
                   c.porcentaje_comision, c.estado
            FROM contratos c JOIN proveedores p ON c.id_proveedor = p.id_proveedor
            ORDER BY c.fecha_inicio DESC
        """)
        for row in cursor.fetchall():
            self.tree_contratos.insert("", "end", values=(
                row["id_contrato"], row["proveedor"], row["fecha_inicio"],
                row["fecha_fin"], f"{row['porcentaje_comision']}%", row["estado"]
            ))
        conn.close()
        
    def cargar_espacios(self):
        for item in self.tree_espacios.get_children():
            self.tree_espacios.delete(item)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM espacios_exhibicion ORDER BY codigo")
        for row in cursor.fetchall():
            self.tree_espacios.insert("", "end", values=(
                row["id_espacio"], row["codigo"], row["descripcion"] or "-",
                row["ubicacion"] or "-", row["capacidad_max"], row["estado"]
            ))
        conn.close()
        
    def nuevo_contrato(self):
        form = tk.Toplevel(self.window)
        form.title("Nuevo Contrato")
        form.geometry("400x320")
        form.configure(bg=self.S.COLORS["bg_main"])
        form.transient(self.window)
        form.grab_set()
        
        header = tk.Frame(form, bg=self.S.COLORS["primary"])
        header.pack(fill="x")
        tk.Label(header, text="Nuevo Contrato",
                font=("Segoe UI", 14, "bold"), bg=self.S.COLORS["primary"], fg="white").pack(pady=12, padx=20)
        
        card = tk.Frame(form, bg="white")
        card.pack(fill="both", expand=True, padx=25, pady=20)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM proveedores WHERE estado='activo'")
        proveedores = [p["nombre"] for p in cursor.fetchall()]
        conn.close()
        
        tk.Label(card, text="Proveedor:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        proveedor_var = tk.StringVar()
        ttk.Combobox(card, textvariable=proveedor_var, values=proveedores, width=33, state="readonly").grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(card, text="Fecha Inicio:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        entry_inicio = ttk.Entry(card, width=35, font=("Segoe UI", 11))
        entry_inicio.grid(row=1, column=1, pady=10, padx=10)
        entry_inicio.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        tk.Label(card, text="Fecha Fin:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=0, sticky="w", pady=10)
        entry_fin = ttk.Entry(card, width=35, font=("Segoe UI", 11))
        entry_fin.grid(row=2, column=1, pady=10, padx=10)
        entry_fin.insert(0, (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"))
        
        tk.Label(card, text="Comision (%):", font=("Segoe UI", 10, "bold"), bg="white").grid(row=3, column=0, sticky="w", pady=10)
        entry_comision = ttk.Entry(card, width=35, font=("Segoe UI", 11))
        entry_comision.grid(row=3, column=1, pady=10, padx=10)
        entry_comision.insert(0, "15.0")
        
        def guardar():
            if not proveedor_var.get():
                messagebox.showwarning("Error", "Seleccione un proveedor")
                return
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id_proveedor FROM proveedores WHERE nombre=?", (proveedor_var.get(),))
            id_proveedor = cursor.fetchone()["id_proveedor"]
            try:
                cursor.execute("""
                    INSERT INTO contratos (id_proveedor, fecha_inicio, fecha_fin, porcentaje_comision, condiciones)
                    VALUES (?, ?, ?, ?, 'Contrato estandar')
                """, (id_proveedor, entry_inicio.get(), entry_fin.get(), float(entry_comision.get())))
                conn.commit()
                form.destroy()
                self.cargar_contratos()
                messagebox.showinfo("Exito", "Contrato creado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
                
        tk.Button(card, text="Guardar", font=("Segoe UI", 11, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", cursor="hand2", padx=30, pady=10, command=guardar).grid(row=4, column=0, columnspan=2, pady=20)
        
    def nuevo_espacio(self):
        form = tk.Toplevel(self.window)
        form.title("Nuevo Espacio")
        form.geometry("400x280")
        form.configure(bg=self.S.COLORS["bg_main"])
        form.transient(self.window)
        form.grab_set()
        
        header = tk.Frame(form, bg=self.S.COLORS["primary"])
        header.pack(fill="x")
        tk.Label(header, text="Nuevo Espacio",
                font=("Segoe UI", 14, "bold"), bg=self.S.COLORS["primary"], fg="white").pack(pady=12, padx=20)
        
        card = tk.Frame(form, bg="white")
        card.pack(fill="both", expand=True, padx=25, pady=20)
        
        campos = [("Codigo:", "codigo"), ("Descripcion:", "descripcion"), ("Ubicacion:", "ubicacion")]
        entries = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(card, text=label, font=("Segoe UI", 10, "bold"), bg="white").grid(row=i, column=0, sticky="w", pady=10)
            entry = ttk.Entry(card, width=30, font=("Segoe UI", 11))
            entry.grid(row=i, column=1, pady=10, padx=10)
            entries[key] = entry
            
        tk.Label(card, text="Capacidad:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=3, column=0, sticky="w", pady=10)
        entry_cap = ttk.Entry(card, width=30, font=("Segoe UI", 11))
        entry_cap.grid(row=3, column=1, pady=10, padx=10)
        entry_cap.insert(0, "100")
        
        def guardar():
            if not entries["codigo"].get().strip():
                messagebox.showwarning("Error", "El codigo es obligatorio")
                return
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO espacios_exhibicion (codigo, descripcion, ubicacion, capacidad_max) VALUES (?, ?, ?, ?)",
                             (entries["codigo"].get().strip(), entries["descripcion"].get().strip(), entries["ubicacion"].get().strip(), int(entry_cap.get())))
                conn.commit()
                form.destroy()
                self.cargar_espacios()
                messagebox.showinfo("Exito", "Espacio creado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
                
        tk.Button(card, text="Guardar", font=("Segoe UI", 11, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", cursor="hand2", padx=30, pady=15, command=guardar).grid(row=4, column=0, columnspan=2, pady=15)
