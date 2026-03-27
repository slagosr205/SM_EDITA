"""Módulo de Productos"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from styles import ElegantStyles
import random

class ProductosWindow:
    def __init__(self, parent):
        self.S = ElegantStyles
        self.window = tk.Toplevel(parent)
        self.window.title("Catalogo de Productos")
        self.window.geometry("1050x500")
        self.window.configure(bg=self.S.COLORS["bg_main"])
        
        self.create_widgets()
        self.cargar_productos()
        
    def create_widgets(self):
        toolbar = tk.Frame(self.window, bg="white", height=60)
        toolbar.pack(fill="x", side="top")
        toolbar.pack_propagate(False)
        
        tk.Label(toolbar, text="Productos", 
                font=("Segoe UI", 14, "bold"), bg="white", 
                fg=self.S.COLORS["text_dark"]).pack(side="left", padx=20, pady=15)
        
        btn_frame = tk.Frame(toolbar, bg="white")
        btn_frame.pack(side="right", padx=20)
        
        tk.Button(btn_frame, text="+ Nuevo", font=("Segoe UI", 10, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", 
                 cursor="hand2", padx=20, pady=8, command=self.nuevo_producto).pack(side="left", padx=5)
        
        search_frame = tk.Frame(self.window, bg=self.S.COLORS["bg_main"])
        search_frame.pack(fill="x", padx=20, pady=10)
        
        search_box = tk.Frame(search_frame, bg="white", padx=10)
        search_box.pack(side="left")
        
        tk.Label(search_box, text="Buscar:", bg="white", font=("Segoe UI", 10)).pack(side="left", padx=(10, 5))
        
        self.entry_buscar = ttk.Entry(search_box, width=40, font=("Segoe UI", 11))
        self.entry_buscar.pack(side="left", ipady=8)
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.buscar_productos())
        
        card = tk.Frame(self.window, bg="white", relief="flat")
        card.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        columns = ("ID", "Codigo", "Nombre", "Proveedor", "P. Venta", "Estado")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=16)
        
        for col in columns:
            self.tree.heading(col, text=col)
            widths = {"ID": 50, "Codigo": 120, "Nombre": 250, "Proveedor": 180, "P. Venta": 100, "Estado": 80}
            self.tree.column(col, width=widths.get(col, 100))
        
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
    def cargar_productos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id_producto, p.codigo_barras, p.nombre, pr.nombre as proveedor,
                   p.precio_venta, p.estado
            FROM productos p JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
            ORDER BY p.nombre
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(
                row["id_producto"], row["codigo_barras"], row["nombre"],
                row["proveedor"], f"S/. {row['precio_venta']:.2f}", row["estado"]
            ))
        conn.close()
        
    def buscar_productos(self):
        texto = self.entry_buscar.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = get_connection()
        cursor = conn.cursor()
        
        if texto:
            cursor.execute("""
                SELECT p.id_producto, p.codigo_barras, p.nombre, pr.nombre as proveedor,
                       p.precio_venta, p.estado
                FROM productos p JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
                WHERE p.nombre LIKE ? OR p.codigo_barras LIKE ?
                ORDER BY p.nombre
            """, (f"%{texto}%", f"%{texto}%"))
        else:
            cursor.execute("""
                SELECT p.id_producto, p.codigo_barras, p.nombre, pr.nombre as proveedor,
                       p.precio_venta, p.estado
                FROM productos p JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
                ORDER BY p.nombre
            """)
            
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(
                row["id_producto"], row["codigo_barras"], row["nombre"],
                row["proveedor"], f"S/. {row['precio_venta']:.2f}", row["estado"]
            ))
        conn.close()
        
    def generar_codigo(self):
        return f"750{random.randint(10000000, 99999999)}"
        
    def nuevo_producto(self):
        form = tk.Toplevel(self.window)
        form.title("Nuevo Producto")
        form.geometry("450x380")
        form.configure(bg=self.S.COLORS["bg_main"])
        form.transient(self.window)
        form.grab_set()
        
        header = tk.Frame(form, bg=self.S.COLORS["purple"])
        header.pack(fill="x")
        tk.Label(header, text="Nuevo Producto",
                font=("Segoe UI", 14, "bold"), bg=self.S.COLORS["purple"], fg="white").pack(pady=12, padx=20)
        
        card = tk.Frame(form, bg="white")
        card.pack(fill="both", expand=True, padx=25, pady=20)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_proveedor, nombre FROM proveedores WHERE estado='activo'")
        proveedores = list(cursor.fetchall())
        conn.close()
        
        tk.Label(card, text="Proveedor:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        proveedor_var = tk.StringVar()
        ttk.Combobox(card, textvariable=proveedor_var, values=[p["nombre"] for p in proveedores], width=33, state="readonly").grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(card, text="Nombre:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        entry_nombre = ttk.Entry(card, width=35, font=("Segoe UI", 11))
        entry_nombre.grid(row=1, column=1, pady=10, padx=10)
        
        tk.Label(card, text="Codigo:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=0, sticky="w", pady=10)
        frame_codigo = tk.Frame(card, bg="white")
        frame_codigo.grid(row=2, column=1, pady=10, padx=10, sticky="w")
        
        entry_codigo = ttk.Entry(frame_codigo, width=25, font=("Segoe UI", 11))
        entry_codigo.pack(side="left")
        entry_codigo.insert(0, self.generar_codigo())
        
        tk.Label(card, text="Precio Venta:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=3, column=0, sticky="w", pady=10)
        entry_venta = ttk.Entry(card, width=35, font=("Segoe UI", 11))
        entry_venta.grid(row=3, column=1, pady=10, padx=10)
        
        def guardar():
            nombre_proveedor = proveedor_var.get()
            if not nombre_proveedor or not entry_nombre.get().strip():
                messagebox.showwarning("Error", "Complete los campos obligatorios")
                return
            id_proveedor = next((p["id_proveedor"] for p in proveedores if p["nombre"] == nombre_proveedor), None)
            
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO productos (id_proveedor, nombre, codigo_barras, precio_venta, precio_costo, estado)
                    VALUES (?, ?, ?, ?, ?, 'activo')
                """, (id_proveedor, entry_nombre.get().strip(), entry_codigo.get().strip(),
                      float(entry_venta.get()), float(entry_venta.get()) * 0.5 if entry_venta.get() else None))
                conn.commit()
                form.destroy()
                self.cargar_productos()
                messagebox.showinfo("Exito", "Producto guardado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
                
        tk.Button(card, text="Guardar", font=("Segoe UI", 11, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", cursor="hand2", padx=30, pady=10, command=guardar).grid(row=4, column=0, columnspan=2, pady=20)
