"""Módulo de Surtido"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from datetime import datetime
from styles import ElegantStyles

class SurtidoWindow:
    def __init__(self, parent):
        self.S = ElegantStyles
        self.window = tk.Toplevel(parent)
        self.window.title("Planificacion de Surtido")
        self.window.geometry("1000x500")
        self.window.configure(bg=self.S.COLORS["bg_main"])
        
        self.create_widgets()
        self.cargar_planificaciones()
        
    def create_widgets(self):
        toolbar = tk.Frame(self.window, bg="white", height=60)
        toolbar.pack(fill="x", side="top")
        toolbar.pack_propagate(False)
        
        tk.Label(toolbar, text="Surtido", 
                font=("Segoe UI", 14, "bold"), bg="white", 
                fg=self.S.COLORS["text_dark"]).pack(side="left", padx=20, pady=15)
        
        btn_frame = tk.Frame(toolbar, bg="white")
        btn_frame.pack(side="right", padx=20)
        
        tk.Button(btn_frame, text="Generar Planes", font=("Segoe UI", 10, "bold"),
                 bg=self.S.COLORS["success"], fg="white", relief="flat", 
                 cursor="hand2", padx=15, pady=8, command=self.generar_plan).pack(side="left", padx=5)
        
        card = tk.Frame(self.window, bg="white", relief="flat")
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        columns = ("ID", "Producto", "Espacio", "Cant. Solicitada", "Fecha", "Estado")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=16)
        
        for col in columns:
            self.tree.heading(col, text=col)
            widths = {"ID": 50, "Producto": 280, "Espacio": 100, "Cant. Solicitada": 120, "Fecha": 120, "Estado": 100}
            self.tree.column(col, width=widths.get(col, 100))
        
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
    def cargar_planificaciones(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ps.id_planificacion, p.nombre as producto, e.codigo as espacio,
                   ps.cant_solicitada, ps.fecha_planificada, ps.estado
            FROM planif_surtido ps
            JOIN productos p ON ps.id_producto = p.id_producto
            JOIN espacios_exhibicion e ON ps.id_espacio = e.id_espacio
            ORDER BY ps.fecha_creacion DESC
        """)
        
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(
                row["id_planificacion"], row["producto"], row["espacio"],
                row["cant_solicitada"], row["fecha_planificada"], row["estado"]
            ))
        conn.close()
        
    def generar_plan(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.id_producto, e.id_espacio, i.cant_actual, i.cant_maxima
            FROM inventarios i
            JOIN productos p ON i.id_producto = p.id_producto
            JOIN espacios_exhibicion e ON i.id_espacio = e.id_espacio
            WHERE i.cant_actual <= i.cant_minima
        """)
        
        bajo_stock = cursor.fetchall()
        creados = 0
        
        for item in bajo_stock:
            cantidad = item["cant_maxima"] - item["cant_actual"]
            
            cursor.execute("""
                SELECT COUNT(*) FROM planif_surtido 
                WHERE id_producto=? AND id_espacio=? AND estado IN ('pendiente', 'aprobado')
            """, (item["id_producto"], item["id_espacio"]))
            
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO planif_surtido (id_producto, id_espacio, fecha_planificada, cant_solicitada, estado)
                    VALUES (?, ?, ?, ?, 'pendiente')
                """, (item["id_producto"], item["id_espacio"], datetime.now().strftime("%Y-%m-%d"), cantidad))
                creados += 1
                
        conn.commit()
        conn.close()
        
        self.cargar_planificaciones()
        messagebox.showinfo("Planes generados", f"Se generaron {creados} planes de surtido")
