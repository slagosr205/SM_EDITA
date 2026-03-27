"""Módulo de Proveedores"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from styles import ElegantStyles

class ProveedoresWindow:
    def __init__(self, parent):
        self.S = ElegantStyles
        self.window = tk.Toplevel(parent)
        self.window.title("Gestion de Proveedores")
        self.window.geometry("1000x550")
        self.window.configure(bg=self.S.COLORS["bg_main"])
        
        self.create_widgets()
        self.cargar_proveedores()
        
    def create_widgets(self):
        toolbar = tk.Frame(self.window, bg="white", height=60)
        toolbar.pack(fill="x", side="top")
        toolbar.pack_propagate(False)
        
        tk.Label(toolbar, text="Proveedores", 
                font=("Segoe UI", 14, "bold"), bg="white", 
                fg=self.S.COLORS["text_dark"]).pack(side="left", padx=20, pady=15)
        
        btn_frame = tk.Frame(toolbar, bg="white")
        btn_frame.pack(side="right", padx=20)
        
        tk.Button(btn_frame, text="+ Nuevo", font=("Segoe UI", 10, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", 
                 cursor="hand2", padx=20, pady=8, command=self.nuevo_proveedor).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Editar", font=("Segoe UI", 10),
                 bg=self.S.COLORS["accent"], fg="white", relief="flat", 
                 cursor="hand2", padx=15, pady=8, command=self.editar_proveedor).pack(side="left", padx=5)
        
        search_frame = tk.Frame(self.window, bg=self.S.COLORS["bg_main"])
        search_frame.pack(fill="x", padx=20, pady=15)
        
        search_box = tk.Frame(search_frame, bg="white", padx=10)
        search_box.pack(side="left")
        
        tk.Label(search_box, text="Buscar:", bg="white", font=("Segoe UI", 10)).pack(side="left", padx=(10, 5))
        
        self.entry_buscar = ttk.Entry(search_box, width=40, font=("Segoe UI", 11))
        self.entry_buscar.pack(side="left", ipady=8)
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.buscar_proveedores())
        
        card = tk.Frame(self.window, bg="white", relief="flat")
        card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        columns = ("ID", "Nombre", "RUC/NIT", "Telefono", "Email", "Estado")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120 if col == "Nombre" else 100)
        self.tree.column("ID", width=50)
        
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        self.tree.bind("<Double-1>", lambda e: self.editar_proveedor())
        
    def cargar_proveedores(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_proveedor, nombre, ruc_nit, telefono, email, estado
            FROM proveedores ORDER BY nombre
        """)
        
        for row in cursor.fetchall():
            estado_color = "Activo" if row["estado"] == "activo" else "Inactivo"
            self.tree.insert("", "end", values=(
                row["id_proveedor"], row["nombre"], row["ruc_nit"],
                row["telefono"] or "-", row["email"] or "-", estado_color
            ))
        conn.close()
        
    def buscar_proveedores(self):
        texto = self.entry_buscar.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = get_connection()
        cursor = conn.cursor()
        
        if texto:
            cursor.execute("""
                SELECT id_proveedor, nombre, ruc_nit, telefono, email, estado
                FROM proveedores 
                WHERE nombre LIKE ? OR ruc_nit LIKE ? OR email LIKE ?
                ORDER BY nombre
            """, (f"%{texto}%", f"%{texto}%", f"%{texto}%"))
        else:
            cursor.execute("""
                SELECT id_proveedor, nombre, ruc_nit, telefono, email, estado
                FROM proveedores ORDER BY nombre
            """)
            
        for row in cursor.fetchall():
            estado_color = "Activo" if row["estado"] == "activo" else "Inactivo"
            self.tree.insert("", "end", values=(
                row["id_proveedor"], row["nombre"], row["ruc_nit"],
                row["telefono"] or "-", row["email"] or "-", estado_color
            ))
        conn.close()
        
    def nuevo_proveedor(self):
        self.formulario_proveedor(None)
        
    def editar_proveedor(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Seleccionar", "Seleccione un proveedor")
            return
            
        item = self.tree.item(selection[0])
        values = item["values"]
        self.formulario_proveedor(values[0])
        
    def formulario_proveedor(self, id_proveedor):
        es_edicion = id_proveedor is not None
        
        form = tk.Toplevel(self.window)
        form.title("Editar Proveedor" if es_edicion else "Nuevo Proveedor")
        form.geometry("500x400")
        form.resizable(False, False)
        form.transient(self.window)
        form.grab_set()
        form.configure(bg=self.S.COLORS["bg_main"])
        
        header = tk.Frame(form, bg=self.S.COLORS["primary"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=("Editar Proveedor" if es_edicion else "Nuevo Proveedor"),
                font=("Segoe UI", 14, "bold"), bg=self.S.COLORS["primary"], 
                fg="white").pack(pady=15, padx=20)
        
        card = tk.Frame(form, bg="white")
        card.pack(fill="both", expand=True, padx=25, pady=20)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        datos = {}
        if es_edicion:
            cursor.execute("SELECT * FROM proveedores WHERE id_proveedor = ?", (id_proveedor,))
            datos = dict(cursor.fetchone())
        conn.close()
        
        campos = [
            ("Nombre completo:", "nombre", datos.get("nombre", "")),
            ("RUC / NIT:", "ruc_nit", datos.get("ruc_nit", "")),
            ("Telefono:", "telefono", datos.get("telefono", "")),
            ("Correo electronico:", "email", datos.get("email", "")),
        ]
        
        entries = {}
        for i, (label, key, default) in enumerate(campos):
            tk.Label(card, text=label, font=("Segoe UI", 10, "bold"),
                    bg="white", fg=self.S.COLORS["text_dark"]).grid(row=i, column=0, sticky="w", pady=12, padx=(0, 10))
            
            entry = ttk.Entry(card, width=35, font=("Segoe UI", 11))
            entry.grid(row=i, column=1, pady=12)
            entry.insert(0, default)
            entries[key] = entry
            
        tk.Label(card, text="Estado:", font=("Segoe UI", 10, "bold"),
                bg="white", fg=self.S.COLORS["text_dark"]).grid(row=4, column=0, sticky="w", pady=12)
        
        estado_var = tk.StringVar(value=datos.get("estado", "activo"))
        estado_frame = tk.Frame(card, bg="white")
        estado_frame.grid(row=4, column=1, sticky="w", pady=12)
        
        tk.Radiobutton(estado_frame, text="Activo", variable=estado_var, value="activo",
                      bg="white", font=("Segoe UI", 10)).pack(side="left", padx=10)
        tk.Radiobutton(estado_frame, text="Inactivo", variable=estado_var, value="inactivo",
                      bg="white", font=("Segoe UI", 10)).pack(side="left")
        
        def guardar():
            nombre = entries["nombre"].get().strip()
            ruc_nit = entries["ruc_nit"].get().strip()
            telefono = entries["telefono"].get().strip()
            email = entries["email"].get().strip()
            estado = estado_var.get()
            
            if not nombre or not ruc_nit:
                messagebox.showwarning("Campos requeridos", "Nombre y RUC/NIT son obligatorios")
                return
                
            conn = get_connection()
            cursor = conn.cursor()
            
            try:
                if es_edicion:
                    cursor.execute("""
                        UPDATE proveedores SET nombre=?, ruc_nit=?, telefono=?, email=?, estado=?
                        WHERE id_proveedor=?
                    """, (nombre, ruc_nit, telefono, email, estado, id_proveedor))
                else:
                    cursor.execute("""
                        INSERT INTO proveedores (nombre, ruc_nit, telefono, email, estado)
                        VALUES (?, ?, ?, ?, ?)
                    """, (nombre, ruc_nit, telefono, email, estado))
                    
                conn.commit()
                form.destroy()
                self.cargar_proveedores()
                messagebox.showinfo("Exito", "Proveedor guardado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")
            finally:
                conn.close()
                
        tk.Button(card, text="Guardar", font=("Segoe UI", 11, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", 
                 cursor="hand2", padx=30, pady=10, command=guardar).grid(row=5, column=0, columnspan=2, pady=25)
