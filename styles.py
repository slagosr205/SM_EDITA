"""Estilos y temas corporativos para el sistema"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class ElegantStyles:
    COLORS = {
        "primary": "#1e3a5f",
        "primary_dark": "#152a45",
        "secondary": "#64748b",
        "accent": "#0ea5e9",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "purple": "#8b5cf6",
        "teal": "#14b8a6",
        "pink": "#ec4899",
        "orange": "#f97316",
        "bg_main": "#f1f5f9",
        "bg_card": "#ffffff",
        "bg_dark": "#0f172a",
        "text_dark": "#1e293b",
        "text_light": "#64748b",
        "text_muted": "#94a3b8",
        "border": "#e2e8f0",
        "border_dark": "#334155",
    }
    
    CHARTS = {
        "ventas": "#10b981",
        "ventas_fade": "#d1fae5",
        "efectivo": "#f59e0b",
        "tarjeta": "#3b82f6",
        "transferencia": "#8b5cf6",
        "yape": "#ec4899",
        "mixto": "#64748b",
        "stock_bajo": "#ef4444",
        "stock_bajo_fade": "#fee2e2",
    }
    
    @classmethod
    def configure_styles(cls, root):
        style = ttk.Style(root)
        root.configure(bg=cls.COLORS["bg_main"])
        
        style.theme_use("clam")
        
        style.configure(".", 
                       background=cls.COLORS["bg_main"],
                       foreground=cls.COLORS["text_dark"],
                       font=("Segoe UI", 10))
        
        style.configure("TFrame", background=cls.COLORS["bg_main"])
        style.configure("Card.TFrame", background=cls.COLORS["bg_card"], relief="flat")
        
        style.configure("TLabel",
                       background=cls.COLORS["bg_main"],
                       foreground=cls.COLORS["text_dark"],
                       font=("Segoe UI", 10))
        
        style.configure("TButton",
                       font=("Segoe UI", 10),
                       padding=(15, 8))
        
        style.configure("Treeview",
                       background=cls.COLORS["bg_card"],
                       foreground=cls.COLORS["text_dark"],
                       fieldbackground=cls.COLORS["bg_card"],
                       font=("Segoe UI", 10),
                       rowheight=32)
        
        style.configure("Treeview.Heading",
                       background=cls.COLORS["primary"],
                       foreground="white",
                       font=("Segoe UI", 10, "bold"),
                       padding=(10, 8))
        
        style.map("Treeview",
                  background=[("selected", cls.COLORS["accent"])],
                  foreground=[("selected", "white")])
        
        style.configure("TEntry", padding=8, font=("Segoe UI", 10))
        style.configure("TCombobox", padding=8, font=("Segoe UI", 10))
        
        return style


class CorporateDashboard:
    HEADER_BG = "#0f172a"
    HEADER_FG = "#f8fafc"
    ACCENT_TEAL = "#0d9488"
    ACCENT_BLUE = "#3b82f6"
    ACCENT_GREEN = "#22c55e"
    ACCENT_RED = "#ef4444"
    ACCENT_PURPLE = "#8b5cf6"
    ACCENT_ORANGE = "#f97316"
    
    @staticmethod
    def crear_header_corporativo(parent, titulo, usuario, rol):
        header = tk.Frame(parent, bg=CorporateDashboard.HEADER_BG, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        logo_frame = tk.Frame(header, bg=CorporateDashboard.HEADER_BG)
        logo_frame.pack(side="left", padx=25, pady=12)
        
        tk.Label(logo_frame, text="TC", font=("Segoe UI", 28, "bold"),
                bg=CorporateDashboard.HEADER_BG, fg=CorporateDashboard.ACCENT_TEAL).pack()
        
        tk.Label(logo_frame, text="TIENDA CONCEPTO", font=("Segoe UI", 9, "bold"),
                bg=CorporateDashboard.HEADER_BG, fg="#94a3b8").pack()
        
        title_frame = tk.Frame(header, bg=CorporateDashboard.HEADER_BG)
        title_frame.pack(side="left", padx=30)
        
        tk.Label(title_frame, text=titulo.upper(),
                font=("Segoe UI", 18, "bold"), bg=CorporateDashboard.HEADER_BG, fg="white").pack(anchor="w")
        
        tk.Label(title_frame, text=datetime.now().strftime("%A, %d de %B del %Y"),
                font=("Segoe UI", 10), bg=CorporateDashboard.HEADER_BG, fg="#64748b").pack(anchor="w")
        
        user_frame = tk.Frame(header, bg=CorporateDashboard.HEADER_BG)
        user_frame.pack(side="right", padx=25, pady=12)
        
        tk.Label(user_frame, text=usuario,
                font=("Segoe UI", 12, "bold"), bg=CorporateDashboard.HEADER_BG, fg="white").pack(anchor="e")
        
        rol_colors = {"admin": CorporateDashboard.ACCENT_TEAL, "supervisor": CorporateDashboard.ACCENT_BLUE, 
                     "cajero": CorporateDashboard.ACCENT_PURPLE}
        rol_bg = rol_colors.get(rol.lower(), CorporateDashboard.ACCENT_PURPLE)
        tk.Label(user_frame, text=rol.upper(), font=("Segoe UI", 9, "bold"),
                bg=rol_bg, fg="white", padx=12, pady=2).pack(anchor="e", pady=(5, 0))
        
        return header
    
    @staticmethod
    def crear_kpi_card(parent, titulo, valor, icono, color, comparar=""):
        card = tk.Frame(parent, bg="white", relief="solid", bd=1)
        card.configure(highlightbackground=color, highlightthickness=3)
        
        top_bar = tk.Frame(card, bg=color, height=4)
        top_bar.pack(fill="x")
        
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, padx=18, pady=15)
        
        tk.Label(content, text=titulo, font=("Segoe UI", 11),
                bg="white", fg="#64748b").pack(anchor="w")
        
        value_frame = tk.Frame(content, bg="white")
        value_frame.pack(fill="x", pady=(8, 0))
        
        valor_label = tk.Label(value_frame, text=valor,
                font=("Segoe UI", 26, "bold"), bg="white", fg=color)
        valor_label.pack(side="left")
        
        if comparar:
            tk.Label(content, text=comparar,
                    font=("Segoe UI", 9), bg="white", fg="#22c55e").pack(anchor="w", pady=(8, 0))
        
        return card, valor_label
    
    @staticmethod
    def crear_chart_bar(canvas, x, y_base, altura, ancho, color, texto_arriba, texto_abajo):
        canvas.create_rectangle(x, y_base - altura, x + ancho, y_base,
                fill=color, outline="", tags="bar")
        
        canvas.create_text(x + ancho/2, y_base - altura - 15,
                text=texto_arriba, font=("Segoe UI", 9, "bold"), fill=color, tags="label")
        
        canvas.create_text(x + ancho/2, y_base + 10,
                text=texto_abajo, font=("Segoe UI", 9), fill="#64748b", tags="label")
    
    @staticmethod
    def crear_chart_pie(canvas, datos, x_centro, y_centro, radio):
        colores = ["#22c55e", "#3b82f6", "#f59e0b", "#8b5cf6", "#ec4899", "#64748b"]
        
        total = sum(d["valor"] for d in datos) if datos else 1
        if total == 0:
            canvas.create_oval(x_centro - 40, y_centro - 40, x_centro + 40, y_centro + 40,
                    fill="#e2e8f0", outline="")
            canvas.create_text(x_centro, y_centro, text="Sin datos",
                    font=("Segoe UI", 9), fill="#64748b")
            return
        
        angulo_inicio = 90
        for i, dato in enumerate(datos):
            angulo_fin = angulo_inicio - (dato["valor"] / total) * 360
            
            color = colores[i % len(colores)]
            
            canvas.create_arc(x_centro - radio, y_centro - radio, 
                           x_centro + radio, y_centro + radio,
                           start=angulo_fin, extent=(dato["valor"] / total) * 360,
                           fill=color, outline="white", width=2)
            
            angulo_medio = (angulo_inicio + angulo_fin) / 2
            if abs(angulo_fin - angulo_inicio) > 10:
                etiqueta_x = x_centro + (radio + 30) * (angulo_medio / 360 if angulo_medio < 360 else (angulo_medio - 360) / 360)
                etiqueta_y = y_centro - (radio + 30) * abs(90 - (angulo_medio % 180)) / 90
                canvas.create_text(etiqueta_x, etiqueta_y,
                        text=f"{dato['etiqueta']}: {dato['valor']:,.0f}",
                        font=("Segoe UI", 8), fill="#1e293b")
            
            angulo_inicio = angulo_fin
    
    @staticmethod
    def crear_card_panel(parent, titulo, expandable=False):
        card = tk.Frame(parent, bg="white", relief="solid", bd=1)
        
        header = tk.Frame(card, bg="white")
        header.pack(fill="x", padx=18, pady=(15, 10))
        
        tk.Label(header, text=titulo, font=("Segoe UI", 13, "bold"),
                bg="white", fg="#1e293b").pack(side="left")
        
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, padx=18, pady=(0, 15))
        
        return card, content
    
    @staticmethod
    def crear_alerta_item(parent, producto, stock, minima, espacio, nivel):
        colores = {
            "critico": ("#fef2f2", "#ef4444", "#dc2626"),
            "bajo": ("#fef3c7", "#f59e0b", "#b45309"),
            "medio": ("#f0fdf4", "#22c55e", "#15803d")
        }
        
        bg, border, texto = colores.get(nivel, colores["medio"])
        
        frame = tk.Frame(parent, bg=bg, padx=12, pady=10, relief="solid", bd=1)
        frame.pack(fill="x", pady=4)
        
        dot = tk.Frame(frame, bg=border, width=8, height=8)
        dot.pack(side="left", padx=(0, 12), pady=5)
        dot.pack_propagate(False)
        
        info = tk.Frame(frame, bg=bg)
        info.pack(side="left", fill="x", expand=True)
        
        nombre = producto[:35] + "..." if len(producto) > 35 else producto
        tk.Label(info, text=nombre, font=("Segoe UI", 11, "bold"),
                bg=bg, fg=texto).pack(anchor="w")
        
        tk.Label(info, text=f"Stock: {stock} | Min: {minima} | {espacio}",
                font=("Segoe UI", 9), bg=bg, fg="#64748b").pack(anchor="w")
        
        return frame
    
    @staticmethod
    def crear_tabla(parent, columns, height=10):
        tree = ttk.Treeview(parent, height=height)
        
        style = ttk.Style()
        style.configure("Corporate.Treeview", font=("Segoe UI", 10), rowheight=32)
        style.configure("Corporate.Treeview.Heading", font=("Segoe UI", 10, "bold"))
        
        tree["style"] = "Corporate.Treeview"
        tree["columns"] = columns
        tree["show"] = "headings"
        
        for col in columns:
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return tree
    
    @staticmethod
    def crear_boton_accion(parent, texto, comando, color=None, icono=""):
        bg = color if color else CorporateDashboard.ACCENT_BLUE
        
        btn = tk.Button(parent, text=f" {texto}", font=("Segoe UI", 10, "bold"),
                       bg=bg, fg="white", relief="flat", cursor="hand2",
                       padx=16, pady=8, command=comando)
        return btn
    
    @staticmethod
    def crear_fila_resumen(parent, concepto, valor, color):
        row = tk.Frame(parent, bg="white")
        row.pack(fill="x", pady=6)
        
        dot = tk.Frame(row, bg=color, width=8, height=8)
        dot.pack(side="left", padx=(0, 10))
        dot.pack_propagate(False)
        
        tk.Label(row, text=concepto, font=("Segoe UI", 11),
                bg="white", fg="#64748b").pack(side="left")
        
        tk.Label(row, text=valor, font=("Segoe UI", 11, "bold"),
                bg="white", fg=color).pack(side="right")
        
        return row
