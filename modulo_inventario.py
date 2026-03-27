"""Módulo de Inventario"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from styles import ElegantStyles
from datetime import datetime

class InventarioWindow:
    def __init__(self, parent):
        self.S = ElegantStyles
        self.window = tk.Toplevel(parent)
        self.window.title("Control de Inventario")
        self.window.geometry("1100x550")
        self.window.configure(bg=self.S.COLORS["bg_main"])
        
        self.create_widgets()
        self.cargar_inventario()
        
    def create_widgets(self):
        toolbar = tk.Frame(self.window, bg="white", height=60)
        toolbar.pack(fill="x", side="top")
        toolbar.pack_propagate(False)
        
        tk.Label(toolbar, text="Control de Inventario", 
                font=("Segoe UI", 14, "bold"), bg="white", 
                fg=self.S.COLORS["text_dark"]).pack(side="left", padx=20, pady=15)
        
        btn_frame = tk.Frame(toolbar, bg="white")
        btn_frame.pack(side="right", padx=20)
        
        tk.Button(btn_frame, text="+ Asignar", font=("Segoe UI", 10, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", 
                 cursor="hand2", padx=20, pady=8, command=self.asignar_inventario).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Ajuste", font=("Segoe UI", 10),
                 bg=self.S.COLORS["warning"], fg="white", relief="flat", 
                 cursor="hand2", padx=15, pady=8, command=self.ajustar_stock).pack(side="left", padx=5)
        
        filter_frame = tk.Frame(self.window, bg=self.S.COLORS["bg_main"])
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        search_box = tk.Frame(filter_frame, bg="white", padx=10)
        search_box.pack(side="left")
        
        tk.Label(search_box, text="Buscar:", bg="white", font=("Segoe UI", 10)).pack(side="left", padx=(10, 5))
        
        self.entry_buscar = ttk.Entry(search_box, width=30, font=("Segoe UI", 11))
        self.entry_buscar.pack(side="left", ipady=8)
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.buscar_inventario())
        
        self.var_alertas = tk.BooleanVar()
        tk.Checkbutton(filter_frame, text="Solo alertas", variable=self.var_alertas,
                      bg=self.S.COLORS["bg_main"], font=("Segoe UI", 10),
                      command=self.buscar_inventario).pack(side="left", padx=20)
        
        card = tk.Frame(self.window, bg="white", relief="flat")
        card.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        columns = ("ID", "Producto", "Espacio", "Actual", "Min", "Max", "Estado")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            widths = {"ID": 50, "Producto": 250, "Espacio": 100, "Actual": 70, "Min": 60, "Max": 60, "Estado": 100}
            self.tree.column(col, width=widths.get(col, 100))
        
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        self.tree.tag_configure("alerta", background="#ffcccc")
        self.tree.tag_configure("ok", background="#e8f5e9")
        
        info_frame = tk.Frame(self.window, bg=self.S.COLORS["primary"], height=35)
        info_frame.pack(fill="x", side="bottom")
        self.label_info = tk.Label(info_frame, text="", bg=self.S.COLORS["primary"], 
                                  fg="white", font=("Segoe UI", 10))
        self.label_info.pack(pady=8)
        
    def cargar_inventario(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.id_inventario, p.nombre as producto, e.codigo as espacio,
                   i.cant_actual, i.cant_minima, i.cant_maxima,
                   CASE WHEN i.cant_actual <= i.cant_minima THEN 'BAJO' ELSE 'OK' END as estado_nivel
            FROM inventarios i
            JOIN productos p ON i.id_producto = p.id_producto
            JOIN espacios_exhibicion e ON i.id_espacio = e.id_espacio
            ORDER BY i.cant_actual ASC
        """)
        
        total_bajo = 0
        for row in cursor.fetchall():
            tag = "alerta" if row["estado_nivel"] == "BAJO" else "ok"
            estado_texto = "BAJO" if row["estado_nivel"] == "BAJO" else "OK"
            self.tree.insert("", "end", tags=(tag,), values=(
                row["id_inventario"], row["producto"], row["espacio"],
                row["cant_actual"], row["cant_minima"], row["cant_maxima"], estado_texto
            ))
            if row["estado_nivel"] == "BAJO":
                total_bajo += 1
        conn.close()
        self.label_info.config(text=f"Total: {len(self.tree.get_children())} | Alertas: {total_bajo}")
        
    def buscar_inventario(self):
        texto = self.entry_buscar.get().strip()
        solo_alertas = self.var_alertas.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT i.id_inventario, p.nombre as producto, e.codigo as espacio,
                   i.cant_actual, i.cant_minima, i.cant_maxima,
                   CASE WHEN i.cant_actual <= i.cant_minima THEN 'BAJO' ELSE 'OK' END as estado_nivel
            FROM inventarios i
            JOIN productos p ON i.id_producto = p.id_producto
            JOIN espacios_exhibicion e ON i.id_espacio = e.id_espacio
            WHERE 1=1
        """
        params = []
        if texto:
            query += " AND p.nombre LIKE ?"
            params.append(f"%{texto}%")
        if solo_alertas:
            query += " AND i.cant_actual <= i.cant_minima"
        query += " ORDER BY i.cant_actual ASC"
        
        cursor.execute(query, params)
        
        total_bajo = 0
        for row in cursor.fetchall():
            tag = "alerta" if row["estado_nivel"] == "BAJO" else "ok"
            estado_texto = "BAJO" if row["estado_nivel"] == "BAJO" else "OK"
            self.tree.insert("", "end", tags=(tag,), values=(
                row["id_inventario"], row["producto"], row["espacio"],
                row["cant_actual"], row["cant_minima"], row["cant_maxima"], estado_texto
            ))
            if row["estado_nivel"] == "BAJO":
                total_bajo += 1
        conn.close()
        self.label_info.config(text=f"Total: {len(self.tree.get_children())} | Alertas: {total_bajo}")
        
    def asignar_inventario(self):
        form = tk.Toplevel(self.window)
        form.title("Asignar Producto")
        form.geometry("400x300")
        form.configure(bg=self.S.COLORS["bg_main"])
        form.transient(self.window)
        form.grab_set()
        
        header = tk.Frame(form, bg=self.S.COLORS["success"])
        header.pack(fill="x")
        tk.Label(header, text="Asignar Producto a Espacio",
                font=("Segoe UI", 14, "bold"), bg=self.S.COLORS["success"], fg="white").pack(pady=12, padx=20)
        
        card = tk.Frame(form, bg="white")
        card.pack(fill="both", expand=True, padx=25, pady=20)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_producto, nombre FROM productos WHERE estado='activo'")
        productos = [f"{p['id_producto']} - {p['nombre']}" for p in cursor.fetchall()]
        cursor.execute("SELECT id_espacio, codigo FROM espacios_exhibicion WHERE estado='ocupado'")
        espacios = [f"{e['id_espacio']} - {e['codigo']}" for e in cursor.fetchall()]
        conn.close()
        
        tk.Label(card, text="Producto:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        producto_var = tk.StringVar()
        ttk.Combobox(card, textvariable=producto_var, values=productos, width=35, state="readonly").grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(card, text="Espacio:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        espacio_var = tk.StringVar()
        ttk.Combobox(card, textvariable=espacio_var, values=espacios, width=35, state="readonly").grid(row=1, column=1, pady=10, padx=10)
        
        tk.Label(card, text="Cantidad:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=0, sticky="w", pady=10)
        entry_cantidad = ttk.Entry(card, width=37, font=("Segoe UI", 11))
        entry_cantidad.grid(row=2, column=1, pady=10, padx=10)
        entry_cantidad.insert(0, "0")
        
        def guardar():
            if not producto_var.get() or not espacio_var.get():
                messagebox.showwarning("Error", "Complete todos los campos")
                return
            id_producto = int(producto_var.get().split(" - ")[0])
            id_espacio = int(espacio_var.get().split(" - ")[0])
            
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO inventarios (id_producto, id_espacio, cant_actual, cant_minima, cant_maxima)
                    VALUES (?, ?, ?, 5, 100)
                """, (id_producto, id_espacio, int(entry_cantidad.get())))
                conn.commit()
                form.destroy()
                self.cargar_inventario()
                messagebox.showinfo("Exito", "Producto asignado al espacio")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
                
        tk.Button(card, text="Guardar", font=("Segoe UI", 11, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", cursor="hand2", padx=30, pady=10, command=guardar).grid(row=3, column=0, columnspan=2, pady=20)
        
    def ajustar_stock(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Seleccionar", "Seleccione un registro")
            return
        item = self.tree.item(selection[0])
        values = item["values"]
        
        form = tk.Toplevel(self.window)
        form.title("Ajuste de Stock")
        form.geometry("400x280")
        form.configure(bg=self.S.COLORS["bg_main"])
        form.transient(self.window)
        form.grab_set()
        
        header = tk.Frame(form, bg=self.S.COLORS["warning"])
        header.pack(fill="x")
        tk.Label(header, text="Ajuste de Stock",
                font=("Segoe UI", 14, "bold"), bg=self.S.COLORS["warning"], fg="white").pack(pady=12, padx=20)
        
        card = tk.Frame(form, bg="white")
        card.pack(fill="both", expand=True, padx=25, pady=20)
        
        tk.Label(card, text=f"Producto: {values[1]}", font=("Segoe UI", 12, "bold"), bg="white").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        tk.Label(card, text=f"Stock Actual: {values[3]}", font=("Segoe UI", 10), bg="white").grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        tk.Label(card, text="Nuevo Stock:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=0, sticky="w", pady=10)
        entry_nuevo = ttk.Entry(card, width=25, font=("Segoe UI", 11))
        entry_nuevo.grid(row=2, column=1, pady=10, padx=10)
        entry_nuevo.insert(0, values[3])
        
        tk.Label(card, text="Motivo:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=3, column=0, sticky="nw", pady=10)
        text_motivo = tk.Text(card, width=25, height=3, font=("Segoe UI", 11))
        text_motivo.grid(row=3, column=1, pady=10, padx=10)
        
        def guardar_ajuste():
            nuevo_stock = int(entry_nuevo.get())
            motivo = text_motivo.get("1.0", "end-1c")
            stock_anterior = int(values[3])
            
            if not motivo.strip():
                messagebox.showwarning("Error", "Ingrese el motivo del ajuste")
                return
            
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE inventarios SET cant_actual=? WHERE id_inventario=?", (nuevo_stock, values[0]))
                conn.commit()
                form.destroy()
                self.cargar_inventario()
                messagebox.showinfo("Exito", "Stock ajustado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
                
        tk.Button(card, text="Guardar Ajuste", font=("Segoe UI", 11, "bold"),
                 bg=self.S.COLORS["warning"], fg="white", relief="flat", cursor="hand2", padx=30, pady=10, command=guardar_ajuste).grid(row=4, column=0, columnspan=2, pady=15)
