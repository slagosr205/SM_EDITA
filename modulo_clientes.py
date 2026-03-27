"""Módulo de Clientes"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from styles import ElegantStyles

class ClientesWindow:
    def __init__(self, parent):
        self.S = ElegantStyles
        self.window = tk.Toplevel(parent)
        self.window.title("Gestion de Clientes")
        self.window.geometry("950x500")
        self.window.configure(bg=self.S.COLORS["bg_main"])
        
        self.create_widgets()
        self.cargar_clientes()
        
    def create_widgets(self):
        toolbar = tk.Frame(self.window, bg="white", height=60)
        toolbar.pack(fill="x", side="top")
        toolbar.pack_propagate(False)
        
        tk.Label(toolbar, text="Clientes", 
                font=("Segoe UI", 14, "bold"), bg="white", 
                fg=self.S.COLORS["text_dark"]).pack(side="left", padx=20, pady=15)
        
        btn_frame = tk.Frame(toolbar, bg="white")
        btn_frame.pack(side="right", padx=20)
        
        tk.Button(btn_frame, text="+ Nuevo", font=("Segoe UI", 10, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", 
                 cursor="hand2", padx=20, pady=8, command=self.nuevo_cliente).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Editar", font=("Segoe UI", 10),
                 bg=self.S.COLORS["accent"], fg="white", relief="flat", 
                 cursor="hand2", padx=15, pady=8, command=self.editar_cliente).pack(side="left", padx=5)
        
        search_frame = tk.Frame(self.window, bg=self.S.COLORS["bg_main"])
        search_frame.pack(fill="x", padx=20, pady=15)
        
        search_box = tk.Frame(search_frame, bg="white", padx=10)
        search_box.pack(side="left")
        
        tk.Label(search_box, text="Buscar:", bg="white", font=("Segoe UI", 10)).pack(side="left", padx=(10, 5))
        
        self.entry_buscar = ttk.Entry(search_box, width=40, font=("Segoe UI", 11))
        self.entry_buscar.pack(side="left", ipady=8)
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.buscar_clientes())
        
        card = tk.Frame(self.window, bg="white", relief="flat")
        card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        columns = ("ID", "Nombre", "Apellido", "Documento", "Telefono", "Email")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=16)
        
        for col in columns:
            self.tree.heading(col, text=col)
            widths = {"ID": 50, "Nombre": 150, "Apellido": 150, "Documento": 110, "Telefono": 110, "Email": 180}
            self.tree.column(col, width=widths.get(col, 100))
        
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        self.tree.bind("<Double-1>", lambda e: self.editar_cliente())
        
    def cargar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_cliente, nombre, apellido, doc_identidad, telefono, email
            FROM clientes ORDER BY nombre
        """)
        
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(
                row["id_cliente"], row["nombre"], row["apellido"] or "-",
                row["doc_identidad"] or "-", row["telefono"] or "-", row["email"] or "-"
            ))
        conn.close()
        
    def buscar_clientes(self):
        texto = self.entry_buscar.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = get_connection()
        cursor = conn.cursor()
        
        if texto:
            cursor.execute("""
                SELECT id_cliente, nombre, apellido, doc_identidad, telefono, email
                FROM clientes 
                WHERE nombre LIKE ? OR apellido LIKE ? OR doc_identidad LIKE ?
                ORDER BY nombre
            """, (f"%{texto}%", f"%{texto}%", f"%{texto}%"))
        else:
            cursor.execute("""
                SELECT id_cliente, nombre, apellido, doc_identidad, telefono, email
                FROM clientes ORDER BY nombre
            """)
            
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(
                row["id_cliente"], row["nombre"], row["apellido"] or "-",
                row["doc_identidad"] or "-", row["telefono"] or "-", row["email"] or "-"
            ))
        conn.close()
        
    def nuevo_cliente(self):
        self.formulario_cliente(None)
        
    def editar_cliente(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Seleccionar", "Seleccione un cliente")
            return
            
        item = self.tree.item(selection[0])
        values = item["values"]
        self.formulario_cliente(values[0])
        
    def formulario_cliente(self, id_cliente):
        es_edicion = id_cliente is not None
        
        form = tk.Toplevel(self.window)
        form.title("Editar Cliente" if es_edicion else "Nuevo Cliente")
        form.geometry("450x380")
        form.resizable(False, False)
        form.transient(self.window)
        form.grab_set()
        form.configure(bg=self.S.COLORS["bg_main"])
        
        header = tk.Frame(form, bg=self.S.COLORS["teal"], height=50)
        header.pack(fill="x")
        
        tk.Label(header, text=("Editar Cliente" if es_edicion else "Nuevo Cliente"),
                font=("Segoe UI", 14, "bold"), bg=self.S.COLORS["teal"], 
                fg="white").pack(pady=12, padx=20)
        
        card = tk.Frame(form, bg="white")
        card.pack(fill="both", expand=True, padx=25, pady=20)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        datos = {}
        if es_edicion:
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = ?", (id_cliente,))
            datos = dict(cursor.fetchone())
        conn.close()
        
        campos = [
            ("Nombre:", "nombre", datos.get("nombre", "")),
            ("Apellido:", "apellido", datos.get("apellido", "")),
            ("Documento:", "doc_identidad", datos.get("doc_identidad", "")),
            ("Telefono:", "telefono", datos.get("telefono", "")),
            ("Email:", "email", datos.get("email", "")),
        ]
        
        entries = {}
        for i, (label, key, default) in enumerate(campos):
            tk.Label(card, text=label, font=("Segoe UI", 10, "bold"),
                    bg="white", fg=self.S.COLORS["text_dark"]).grid(row=i, column=0, sticky="w", pady=10)
            entry = ttk.Entry(card, width=35, font=("Segoe UI", 11))
            entry.grid(row=i, column=1, pady=10, padx=10)
            entry.insert(0, default)
            entries[key] = entry
            
        def guardar():
            nombre = entries["nombre"].get().strip()
            if not nombre:
                messagebox.showwarning("Error", "El nombre es obligatorio")
                return
                
            conn = get_connection()
            cursor = conn.cursor()
            try:
                if es_edicion:
                    cursor.execute("""
                        UPDATE clientes SET nombre=?, apellido=?, doc_identidad=?, telefono=?, email=?
                        WHERE id_cliente=?
                    """, (nombre, entries["apellido"].get().strip(), entries["doc_identidad"].get().strip(),
                          entries["telefono"].get().strip(), entries["email"].get().strip(), id_cliente))
                else:
                    cursor.execute("""
                        INSERT INTO clientes (nombre, apellido, doc_identidad, telefono, email)
                        VALUES (?, ?, ?, ?, ?)
                    """, (nombre, entries["apellido"].get().strip(), entries["doc_identidad"].get().strip(),
                          entries["telefono"].get().strip(), entries["email"].get().strip()))
                    
                conn.commit()
                form.destroy()
                self.cargar_clientes()
                messagebox.showinfo("Exito", "Cliente guardado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
                
        tk.Button(card, text="Guardar", font=("Segoe UI", 11, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", 
                 cursor="hand2", padx=30, pady=10, command=guardar).grid(row=6, column=0, columnspan=2, pady=20)
