"""Módulo de Liquidaciones"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from datetime import datetime
from styles import ElegantStyles

class LiquidacionesWindow:
    def __init__(self, parent):
        self.S = ElegantStyles
        self.window = tk.Toplevel(parent)
        self.window.title("Liquidaciones y Pagos")
        self.window.geometry("1050x500")
        self.window.configure(bg=self.S.COLORS["bg_main"])
        
        self.create_widgets()
        self.cargar_liquidaciones()
        
    def create_widgets(self):
        toolbar = tk.Frame(self.window, bg="white", height=60)
        toolbar.pack(fill="x", side="top")
        toolbar.pack_propagate(False)
        
        tk.Label(toolbar, text="Liquidaciones", 
                font=("Segoe UI", 14, "bold"), bg="white", 
                fg=self.S.COLORS["text_dark"]).pack(side="left", padx=20, pady=15)
        
        btn_frame = tk.Frame(toolbar, bg="white")
        btn_frame.pack(side="right", padx=20)
        
        tk.Button(btn_frame, text="Generar", font=("Segoe UI", 10, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", 
                 cursor="hand2", padx=20, pady=8, command=self.generar_liquidacion).pack(side="left", padx=5)
        
        card = tk.Frame(self.window, bg="white", relief="flat")
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        columns = ("ID", "Proveedor", "Periodo", "Total Ventas", "Comision", "Monto Pagar", "Estado")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=16)
        
        for col in columns:
            self.tree.heading(col, text=col)
            widths = {"ID": 50, "Proveedor": 180, "Periodo": 180, "Total Ventas": 110, 
                     "Comision": 90, "Monto Pagar": 110, "Estado": 90}
            self.tree.column(col, width=widths.get(col, 100))
        
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        info_frame = tk.Frame(self.window, bg=self.S.COLORS["primary"], height=35)
        info_frame.pack(fill="x", side="bottom")
        self.label_info = tk.Label(info_frame, text="", bg=self.S.COLORS["primary"], 
                                  fg="white", font=("Segoe UI", 10))
        self.label_info.pack(pady=8)
        
    def cargar_liquidaciones(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT l.id_liquidacion, p.nombre as proveedor, 
                   l.periodo_inicio || ' - ' || l.periodo_fin as periodo,
                   l.total_ventas, l.monto_comision, l.monto_pagar, l.estado
            FROM liquidaciones l
            JOIN proveedores p ON l.id_proveedor = p.id_proveedor
            ORDER BY l.fecha_liquidacion DESC
        """)
        
        total_pagar = 0
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(
                row["id_liquidacion"], row["proveedor"], row["periodo"],
                f"S/. {row['total_ventas']:.2f}", f"S/. {row['monto_comision']:.2f}",
                f"S/. {row['monto_pagar']:.2f}", row["estado"]
            ))
            if row["estado"] != "pagada":
                total_pagar += row["monto_pagar"]
                
        conn.close()
        self.label_info.config(text=f"Total pendiente de pago: S/. {total_pagar:.2f}")
        
    def generar_liquidacion(self):
        form = tk.Toplevel(self.window)
        form.title("Generar Liquidacion")
        form.geometry("400x300")
        form.configure(bg=self.S.COLORS["bg_main"])
        form.transient(self.window)
        form.grab_set()
        
        header = tk.Frame(form, bg=self.S.COLORS["primary"])
        header.pack(fill="x")
        tk.Label(header, text="Generar Liquidacion",
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
        entry_inicio.insert(0, datetime.now().replace(day=1).strftime("%Y-%m-%d"))
        
        tk.Label(card, text="Fecha Fin:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=0, sticky="w", pady=10)
        entry_fin = ttk.Entry(card, width=35, font=("Segoe UI", 11))
        entry_fin.grid(row=2, column=1, pady=10, padx=10)
        entry_fin.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        def guardar():
            if not proveedor_var.get():
                messagebox.showwarning("Error", "Seleccione un proveedor")
                return
                
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id_proveedor FROM proveedores WHERE nombre=?", (proveedor_var.get(),))
            id_proveedor = cursor.fetchone()["id_proveedor"]
            
            cursor.execute("""
                SELECT c.id_contrato, c.porcentaje_comision FROM contratos c 
                WHERE c.id_proveedor=? AND c.estado='activo'
            """, (id_proveedor,))
            contrato = cursor.fetchone()
            
            if not contrato:
                messagebox.showerror("Error", "No existe contrato activo")
                conn.close()
                return
                
            cursor.execute("""
                SELECT COALESCE(SUM(v.total), 0) as total_ventas FROM ventas v
                JOIN detalle_venta dv ON v.id_venta = dv.id_venta
                JOIN productos p ON dv.id_producto = p.id_producto
                WHERE p.id_proveedor = ? AND v.fecha_venta BETWEEN ? AND ?
                AND v.estado = 'completada'
            """, (id_proveedor, entry_inicio.get(), entry_fin.get() + " 23:59:59"))
            
            total_ventas = cursor.fetchone()["total_ventas"]
            
            if total_ventas == 0:
                messagebox.showinfo("Sin ventas", "No hay ventas en este periodo")
                conn.close()
                return
                
            monto_comision = total_ventas * (contrato["porcentaje_comision"] / 100)
            monto_pagar = total_ventas - monto_comision
            
            try:
                cursor.execute("""
                    INSERT INTO liquidaciones (id_proveedor, id_contrato, periodo_inicio, periodo_fin,
                                              total_ventas, monto_comision, monto_pagar, estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'pendiente')
                """, (id_proveedor, contrato["id_contrato"], entry_inicio.get(), entry_fin.get(),
                      total_ventas, monto_comision, monto_pagar))
                conn.commit()
                form.destroy()
                self.cargar_liquidaciones()
                messagebox.showinfo("Exito", "Liquidacion generada")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
                
        tk.Button(card, text="Generar", font=("Segoe UI", 11, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", cursor="hand2", padx=30, pady=10, command=guardar).grid(row=3, column=0, columnspan=2, pady=20)
