"""Módulo de Punto de Venta (POS)"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from styles import ElegantStyles
from datetime import datetime

class POSWindow:
    def __init__(self, parent, usuario_actual):
        self.S = ElegantStyles
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.carrito = []
        
        self.window = tk.Toplevel(parent)
        self.window.title("Punto de Venta")
        self.window.geometry("1200x700")
        self.window.configure(bg=self.S.COLORS["bg_main"])
        
        self.create_widgets()
        self.cargar_productos_venta()
        self.cargar_clientes()
        
    def create_widgets(self):
        main_paned = ttk.PanedWindow(self.window, orient="horizontal")
        main_paned.pack(fill="both", expand=True, padx=20, pady=20)
        
        left_panel = tk.Frame(main_paned, bg="white")
        main_paned.add(left_panel, weight=2)
        
        right_panel = tk.Frame(main_paned, bg="white")
        main_paned.add(right_panel, weight=1)
        
        self.create_products_panel(left_panel)
        self.create_cart_panel(right_panel)
        
    def create_products_panel(self, parent):
        header = tk.Frame(parent, bg=self.S.COLORS["primary"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="PRODUCTOS DISPONIBLES", 
                font=("Segoe UI", 14, "bold"),
                bg=self.S.COLORS["primary"], fg="white").pack(side="left", padx=20, pady=15)
        
        search_frame = tk.Frame(parent, bg=self.S.COLORS["bg_main"])
        search_frame.pack(fill="x", padx=15, pady=10)
        
        search_box = tk.Frame(search_frame, bg="white", padx=10)
        search_box.pack(side="left")
        
        tk.Label(search_box, text="Buscar:", bg="white", 
                font=("Segoe UI", 10)).pack(side="left", padx=(10, 5))
        
        self.entry_buscar = ttk.Entry(search_box, width=35, font=("Segoe UI", 11))
        self.entry_buscar.pack(side="left", ipady=8)
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.buscar_productos())
        
        tk.Label(search_box, text="Codigo:", bg="white", 
                font=("Segoe UI", 10)).pack(side="left", padx=(20, 5))
        
        self.entry_codigo = ttk.Entry(search_box, width=20, font=("Segoe UI", 11))
        self.entry_codigo.pack(side="left", ipady=6)
        self.entry_codigo.bind("<Return>", lambda e: self.agregar_por_codigo())
        
        table_frame = tk.Frame(parent, bg="white")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        columns = ("Codigo", "Producto", "Precio", "Stock", "Espacio")
        self.tree_productos = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.tree_productos.heading(col, text=col)
            widths = {"Codigo": 130, "Producto": 280, "Precio": 100, "Stock": 80, "Espacio": 100}
            self.tree_productos.column(col, width=widths.get(col, 100))
            
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree_productos.bind("<Double-1>", lambda e: self.agregar_al_carrito())
        
        btn_frame = tk.Frame(parent, bg=self.S.COLORS["bg_main"])
        btn_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        tk.Button(btn_frame, text="Agregar al Carrito", font=("Segoe UI", 10, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", 
                 cursor="hand2", padx=20, pady=8, command=self.agregar_al_carrito).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Limpiar", font=("Segoe UI", 10),
                 bg=self.S.COLORS["text_light"], fg="white", relief="flat", 
                 cursor="hand2", padx=15, pady=8,
                 command=lambda: [self.entry_buscar.delete(0, tk.END), self.cargar_productos_venta()]).pack(side="left")
        
    def create_cart_panel(self, parent):
        header = tk.Frame(parent, bg=self.S.COLORS["accent"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="CARRITO DE COMPRA", 
                font=("Segoe UI", 14, "bold"),
                bg=self.S.COLORS["accent"], fg="white").pack(pady=15, padx=20)
        
        table_frame = tk.Frame(parent, bg="white")
        table_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        columns = ("Producto", "Cant.", "P.Unit", "Subtotal")
        self.tree_carrito = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree_carrito.heading(col, text=col)
            widths = {"Producto": 220, "Cant.": 60, "P.Unit": 90, "Subtotal": 90}
            self.tree_carrito.column(col, width=widths.get(col, 100))
            
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_carrito.yview)
        self.tree_carrito.configure(yscrollcommand=scrollbar.set)
        
        self.tree_carrito.pack(side="top", fill="x", expand=False)
        scrollbar.pack(side="right", fill="y")
        
        btn_carrito = tk.Frame(parent, bg=self.S.COLORS["bg_main"])
        btn_carrito.pack(fill="x", padx=15, pady=(0, 10))
        
        tk.Button(btn_carrito, text="+", font=("Segoe UI", 12, "bold"),
                 bg=self.S.COLORS["accent"], fg="white", relief="flat", 
                 cursor="hand2", width=3, command=self.aumentar_cantidad).pack(side="left", padx=2)
        
        tk.Button(btn_carrito, text="-", font=("Segoe UI", 12, "bold"),
                 bg=self.S.COLORS["warning"], fg="white", relief="flat", 
                 cursor="hand2", width=3, command=self.disminuir_cantidad).pack(side="left", padx=2)
        
        tk.Button(btn_carrito, text="X", font=("Segoe UI", 10),
                 bg=self.S.COLORS["danger"], fg="white", relief="flat", 
                 cursor="hand2", width=4, command=self.eliminar_del_carrito).pack(side="left", padx=2)
        
        tk.Button(btn_carrito, text="Vaciar", font=("Segoe UI", 9),
                 bg=self.S.COLORS["text_light"], fg="white", relief="flat", 
                 cursor="hand2", command=self.vaciar_carrito).pack(side="left", padx=10)
        
        totales_frame = tk.Frame(parent, bg=self.S.COLORS["primary"])
        totales_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(totales_frame, text="Subtotal:", font=("Segoe UI", 12),
                bg=self.S.COLORS["primary"], fg="#bdc3c7").grid(row=0, column=0, sticky="w", pady=8, padx=15)
        self.label_subtotal = tk.Label(totales_frame, text="S/. 0.00", font=("Segoe UI", 12), 
                                       bg=self.S.COLORS["primary"], fg="white")
        self.label_subtotal.grid(row=0, column=1, sticky="e", pady=8, padx=15)
        
        tk.Label(totales_frame, text="IGV (18%):", font=("Segoe UI", 12),
                bg=self.S.COLORS["primary"], fg="#bdc3c7").grid(row=1, column=0, sticky="w", pady=8, padx=15)
        self.label_igv = tk.Label(totales_frame, text="S/. 0.00", font=("Segoe UI", 12),
                                  bg=self.S.COLORS["primary"], fg="white")
        self.label_igv.grid(row=1, column=1, sticky="e", pady=8, padx=15)
        
        separator = tk.Frame(totales_frame, bg=self.S.COLORS["secondary"], height=2)
        separator.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10, padx=15)
        
        tk.Label(totales_frame, text="TOTAL:", font=("Segoe UI", 18, "bold"), 
                bg=self.S.COLORS["primary"], fg="white").grid(row=3, column=0, sticky="w", pady=15, padx=15)
        self.label_total = tk.Label(totales_frame, text="S/. 0.00", font=("Segoe UI", 20, "bold"),
                                    bg=self.S.COLORS["primary"], fg=self.S.COLORS["success"])
        self.label_total.grid(row=3, column=1, sticky="e", pady=15, padx=15)
        
        options_frame = tk.Frame(parent, bg="white")
        options_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(options_frame, text="Cliente:", font=("Segoe UI", 10, "bold"),
                bg="white", fg=self.S.COLORS["text_dark"]).pack(anchor="w", pady=(5, 5))
        
        cliente_frame = tk.Frame(options_frame, bg="white")
        cliente_frame.pack(fill="x", pady=(0, 5))
        
        self.combo_cliente = ttk.Combobox(cliente_frame, width=40, state="readonly", font=("Segoe UI", 10))
        self.combo_cliente.pack(side="left", fill="x", expand=True)
        self.cargar_clientes()
        
        tk.Button(cliente_frame, text="+", font=("Segoe UI", 11, "bold"), bg="#3b82f6", fg="white",
                 relief="flat", cursor="hand2", width=3, command=self.nuevo_cliente_desde_pos).pack(side="left", padx=(5, 0))
        
        self.cliente_info_label = tk.Label(options_frame, text="", font=("Segoe UI", 9),
                bg="white", fg=self.S.COLORS["text_light"])
        self.cliente_info_label.pack(anchor="w", pady=(0, 5))
        
        self.combo_cliente.bind("<<ComboboxSelected>>", lambda e: self.on_cliente_seleccionado())
        
        tk.Label(options_frame, text="Pago:", font=("Segoe UI", 10, "bold"),
                bg="white", fg=self.S.COLORS["text_dark"]).pack(anchor="w", pady=(5, 5))
        
        self.combo_pago = ttk.Combobox(options_frame, width=35, state="readonly", font=("Segoe UI", 10))
        self.combo_pago["values"] = ["Efectivo", "Tarjeta Debito", "Tarjeta Credito", "Transferencia", "Yape/Plin", "Mixto"]
        self.combo_pago.current(0)
        self.combo_pago.pack(fill="x")
        
        btn_vender = tk.Button(parent, text="COBRAR AHORA", font=("Segoe UI", 14, "bold"),
                              bg=self.S.COLORS["success"], fg="white", relief="flat", 
                              cursor="hand2", height=50, command=self.procesar_venta)
        btn_vender.pack(fill="x", padx=15, pady=15)
        
    def cargar_productos_venta(self):
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.codigo_barras, p.nombre, p.precio_venta, i.cant_actual, e.codigo as espacio
            FROM productos p
            JOIN inventarios i ON p.id_producto = i.id_producto
            JOIN espacios_exhibicion e ON i.id_espacio = e.id_espacio
            WHERE p.estado = 'activo' AND i.cant_actual > 0
            ORDER BY p.nombre
        """)
        
        for row in cursor.fetchall():
            self.tree_productos.insert("", "end", values=(
                row["codigo_barras"], row["nombre"], f"S/. {row['precio_venta']:.2f}",
                row["cant_actual"], row["espacio"]
            ))
        conn.close()
        
    def cargar_clientes(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nombre, apellido, doc_identidad FROM clientes ORDER BY nombre")
        clientes = cursor.fetchall()
        conn.close()
        
        valores = ["[SIN CLIENTE] Consumidor Final"]
        for c in clientes:
            nombre = f"{c['nombre']} {c['apellido'] or ''}".strip()
            doc = c['doc_identidad'] or 'S/D'
            valores.append(f"{nombre} | DOC: {doc}")
        self.combo_cliente["values"] = valores
        self.combo_cliente.current(0)
    
    def on_cliente_seleccionado(self):
        cliente = self.combo_cliente.get()
        if not cliente or cliente.startswith("[SIN CLIENTE]"):
            self.cliente_info_label.config(text="Venta como Consumidor Final")
            return
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, COUNT(v.id_venta) as num_compras, COALESCE(SUM(v.total), 0) as total_compras
            FROM clientes c
            LEFT JOIN ventas v ON c.id_cliente = v.id_cliente
            WHERE c.nombre || ' ' || COALESCE(c.apellido, '') || ' | DOC: ' || COALESCE(c.doc_identidad, 'S/D') = ?
            GROUP BY c.id_cliente
        """, (cliente,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            info = f"Cliente: {cliente.split(' | ')[0]} | Doc: {result['doc_identidad'] or 'S/D'} | Compras: {result['num_compras']} | Total: L {result['total_compras']:,.2f}"
            self.cliente_info_label.config(text=info)
    
    def nuevo_cliente_desde_pos(self):
        form = tk.Toplevel(self.window)
        form.title("Nuevo Cliente")
        form.geometry("400x320")
        form.configure(bg="white")
        form.transient(self.window)
        form.grab_set()
        
        header = tk.Frame(form, bg="#3b82f6")
        header.pack(fill="x")
        tk.Label(header, text="Agregar Nuevo Cliente", font=("Segoe UI", 14, "bold"),
                bg="#3b82f6", fg="white").pack(pady=12, padx=20)
        
        card = tk.Frame(form, bg="white")
        card.pack(fill="both", expand=True, padx=25, pady=20)
        
        campos = [("Nombre:", "nombre"), ("Apellido:", "apellido"), ("Documento:", "doc_identidad"), ("Telefono:", "telefono"), ("Email:", "email")]
        entries = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(card, text=label, font=("Segoe UI", 10, "bold"), bg="white").grid(row=i, column=0, sticky="w", pady=8, padx=(0, 10))
            entry = ttk.Entry(card, width=30, font=("Segoe UI", 11))
            entry.grid(row=i, column=1, pady=8)
            entries[key] = entry
        
        def guardar():
            if not entries["nombre"].get().strip():
                messagebox.showwarning("Error", "El nombre es obligatorio")
                return
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO clientes (nombre, apellido, doc_identidad, telefono, email) VALUES (?, ?, ?, ?, ?)",
                             (entries["nombre"].get(), entries["apellido"].get(), entries["doc_identidad"].get(), entries["telefono"].get(), entries["email"].get()))
                conn.commit()
                form.destroy()
                self.cargar_clientes()
                messagebox.showinfo("Exito", "Cliente agregado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
        
        tk.Button(card, text="Guardar Cliente", font=("Segoe UI", 11, "bold"), bg="#3b82f6", fg="white",
                 relief="flat", cursor="hand2", padx=20, pady=10, command=guardar).grid(row=len(campos), column=0, columnspan=2, pady=20)
        
    def buscar_productos(self):
        texto = self.entry_buscar.get().strip()
        
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
            
        conn = get_connection()
        cursor = conn.cursor()
        
        if texto:
            cursor.execute("""
                SELECT p.codigo_barras, p.nombre, p.precio_venta, i.cant_actual, e.codigo as espacio
                FROM productos p
                JOIN inventarios i ON p.id_producto = i.id_producto
                JOIN espacios_exhibicion e ON i.id_espacio = e.id_espacio
                WHERE p.estado = 'activo' AND i.cant_actual > 0
                AND (p.nombre LIKE ? OR p.codigo_barras LIKE ?)
                ORDER BY p.nombre
            """, (f"%{texto}%", f"%{texto}%"))
        else:
            cursor.execute("""
                SELECT p.codigo_barras, p.nombre, p.precio_venta, i.cant_actual, e.codigo as espacio
                FROM productos p
                JOIN inventarios i ON p.id_producto = i.id_producto
                JOIN espacios_exhibicion e ON i.id_espacio = e.id_espacio
                WHERE p.estado = 'activo' AND i.cant_actual > 0
                ORDER BY p.nombre
            """)
            
        for row in cursor.fetchall():
            self.tree_productos.insert("", "end", values=(
                row["codigo_barras"], row["nombre"], f"S/. {row['precio_venta']:.2f}",
                row["cant_actual"], row["espacio"]
            ))
        conn.close()
        
    def agregar_por_codigo(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            return
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.codigo_barras, p.nombre, p.precio_venta, i.cant_actual, e.codigo as espacio,
                   i.id_inventario, i.id_producto, i.id_espacio
            FROM productos p
            JOIN inventarios i ON p.id_producto = i.id_producto
            JOIN espacios_exhibicion e ON i.id_espacio = e.id_espacio
            WHERE p.codigo_barras = ? AND p.estado = 'activo' AND i.cant_actual > 0
        """, (codigo,))
        producto = cursor.fetchone()
        conn.close()
        
        if producto:
            self.agregar_item(producto["nombre"], producto["precio_venta"], producto["cant_actual"],
                            producto["espacio"], producto["id_inventario"], producto["id_producto"],
                            producto["id_espacio"])
            self.entry_codigo.delete(0, tk.END)
        else:
            messagebox.showwarning("No encontrado", "Producto no encontrado o sin stock")
            
    def agregar_al_carrito(self):
        selection = self.tree_productos.selection()
        if not selection:
            return
            
        item = self.tree_productos.item(selection[0])
        values = item["values"]
        
        nombre = values[1]
        precio = float(values[2].replace("S/. ", ""))
        stock = values[3]
        espacio = values[4]
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.id_inventario, i.id_producto, i.id_espacio 
            FROM productos p
            JOIN inventarios i ON p.id_producto = i.id_producto
            JOIN espacios_exhibicion e ON i.id_espacio = e.id_espacio
            WHERE p.codigo_barras = ?
        """, (values[0],))
        prod_data = cursor.fetchone()
        conn.close()
        
        self.agregar_item(nombre, precio, stock, espacio, prod_data["id_inventario"],
                        prod_data["id_producto"], prod_data["id_espacio"])
        
    def agregar_item(self, nombre, precio, stock, espacio, id_inventario, id_producto, id_espacio):
        for item in self.tree_carrito.get_children():
            item_data = self.tree_carrito.item(item)
            if item_data["values"][0] == nombre:
                cant_actual = int(item_data["values"][1])
                if cant_actual < stock:
                    nueva_cant = cant_actual + 1
                    self.tree_carrito.item(item, values=(
                        nombre, nueva_cant, f"S/. {precio:.2f}", f"S/. {precio * nueva_cant:.2f}"
                    ))
                self.actualizar_totales()
                return
                
        self.tree_carrito.insert("", "end", values=(
            nombre, 1, f"S/. {precio:.2f}", f"S/. {precio:.2f}"
        ))
        self.carrito.append({
            "nombre": nombre, "precio": precio, "stock": stock, "espacio": espacio,
            "id_inventario": id_inventario, "id_producto": id_producto, "id_espacio": id_espacio
        })
        self.actualizar_totales()
        
    def aumentar_cantidad(self):
        selection = self.tree_carrito.selection()
        if not selection:
            return
        item = self.tree_carrito.item(selection[0])
        values = item["values"]
        
        for i, cart_item in enumerate(self.carrito):
            if cart_item["nombre"] == values[0]:
                if self.carrito[i]["stock"] > int(values[1]):
                    nueva_cant = int(values[1]) + 1
                    self.tree_carrito.item(selection[0], values=(
                        values[0], nueva_cant, values[2], f"S/. {self.carrito[i]['precio'] * nueva_cant:.2f}"
                    ))
        self.actualizar_totales()
        
    def disminuir_cantidad(self):
        selection = self.tree_carrito.selection()
        if not selection:
            return
        item = self.tree_carrito.item(selection[0])
        values = item["values"]
        
        if int(values[1]) > 1:
            nueva_cant = int(values[1]) - 1
            for i, cart_item in enumerate(self.carrito):
                if cart_item["nombre"] == values[0]:
                    self.tree_carrito.item(selection[0], values=(
                        values[0], nueva_cant, values[2], f"S/. {self.carrito[i]['precio'] * nueva_cant:.2f}"
                    ))
        self.actualizar_totales()
        
    def eliminar_del_carrito(self):
        selection = self.tree_carrito.selection()
        if not selection:
            return
        item = self.tree_carrito.item(selection[0])
        values = item["values"]
        
        for i, cart_item in enumerate(self.carrito):
            if cart_item["nombre"] == values[0]:
                self.carrito.pop(i)
                break
                
        self.tree_carrito.delete(selection[0])
        self.actualizar_totales()
        
    def vaciar_carrito(self):
        self.carrito = []
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
        self.actualizar_totales()
        
    def actualizar_totales(self):
        total = 0
        for item in self.tree_carrito.get_children():
            values = self.tree_carrito.item(item)["values"]
            total += float(values[3].replace("S/. ", ""))
            
        igv = total * 0.18
        self.label_subtotal.config(text=f"S/. {total:.2f}")
        self.label_igv.config(text=f"S/. {igv:.2f}")
        self.label_total.config(text=f"S/. {total:.2f}")
        
    def procesar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Carrito vacio", "Agregue productos al carrito")
            return
            
        total = sum(float(self.tree_carrito.item(item)["values"][3].replace("S/. ", ""))
                   for item in self.tree_carrito.get_children())
        
        metodo_pago = self.combo_pago.get()
        cliente_seleccionado = self.combo_cliente.get()
        
        id_cliente = None
        if cliente_seleccionado and not cliente_seleccionado.startswith("[SIN CLIENTE]"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_cliente FROM clientes 
                WHERE nombre || ' ' || COALESCE(apellido, '') || ' | DOC: ' || COALESCE(doc_identidad, 'S/D') = ?
            """, (cliente_seleccionado,))
            cliente = cursor.fetchone()
            id_cliente = cliente["id_cliente"] if cliente else None
            conn.close()
            
        confirmar = messagebox.askyesno("Confirmar Venta", 
            f"Total: S/. {total:.2f}\nMetodo: {metodo_pago}\nCliente: {cliente_nombre}\n\nConfirmar venta?")
        
        if not confirmar:
            return
            
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO ventas (id_cliente, id_usuario, total, metodo_pago, estado)
                VALUES (?, ?, ?, ?, 'completada')
            """, (id_cliente, self.usuario_actual["id_usuario"], total, metodo_pago))
            
            id_venta = cursor.lastrowid
            
            for item in self.tree_carrito.get_children():
                values = self.tree_carrito.item(item)["values"]
                
                for cart_item in self.carrito:
                    if cart_item["nombre"] == values[0]:
                        cantidad = int(values[1])
                        precio_unit = cart_item["precio"]
                        subtotal = float(values[3].replace("S/. ", ""))
                        
                        cursor.execute("""
                            INSERT INTO detalle_venta (id_venta, id_producto, id_espacio, cantidad, precio_unit, subtotal)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (id_venta, cart_item["id_producto"], cart_item["id_espacio"],
                              cantidad, precio_unit, subtotal))
                        
                        cursor.execute("""
                            UPDATE inventarios SET cant_actual = cant_actual - ?
                            WHERE id_inventario = ?
                        """, (cantidad, cart_item["id_inventario"]))
                        break
                        
            conn.commit()
            
            for item in self.tree_carrito.get_children():
                self.tree_carrito.delete(item)
            self.carrito = []
            self.actualizar_totales()
            self.cargar_productos_venta()
            
            messagebox.showinfo("Venta exitosa", f"Venta #{id_venta} registrada correctamente")
            
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()
