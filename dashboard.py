"""Dashboard ejecutivo corporativo - Disenado para propietarios y gerentes"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from database import get_connection
from styles import ElegantStyles

class CorporateDashboard:
    COLORS = {
        "primary": "#1e3a5f",
        "primary_light": "#2d5a87",
        "secondary": "#0ea5e9",
        "success": "#059669",
        "warning": "#d97706",
        "danger": "#dc2626",
        "purple": "#7c3aed",
        "bg_dark": "#0f172a",
        "bg_main": "#f1f5f9",
        "bg_card": "#ffffff",
        "bg_card_header": "#f8fafc",
        "text_dark": "#1e293b",
        "text_medium": "#475569",
        "text_light": "#94a3b8",
        "border": "#e2e8f0",
        "border_dark": "#cbd5e1",
        "positive": "#10b981",
        "negative": "#ef4444",
    }
    
    GRADIENT_PRIMARY = ["#1e3a5f", "#2d5a87", "#0ea5e9"]
    GRADIENT_SUCCESS = ["#059669", "#10b981", "#34d399"]
    GRADIENT_PURPLE = ["#6d28d9", "#7c3aed", "#8b5cf6"]

class DashboardWindow:
    def __init__(self, parent):
        self.parent = parent
        self.usuario_actual = parent.usuario_actual
        self.S = ElegantStyles
        self.content_frame = parent.content_frame
        self.kpi_cards = {}
        self.refresh_job = None
        self.chart_frames = {}
        
        self.create_widgets()
        self.cargar_datos()
    
    def get_currency_info(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT simbolo FROM monedas WHERE codigo = 'HNL'")
        moneda = cursor.fetchone()
        conn.close()
        simbolo = moneda["simbolo"] if moneda else "L"
        return simbolo
    
    def create_card_shadow(self, parent, **kwargs):
        outer = tk.Frame(parent, bg="#d1d5db", **kwargs)
        inner = tk.Frame(outer, bg="white", **kwargs)
        inner.pack(padx=2, pady=2, fill="both", expand=True)
        return outer, inner
    
    def create_widgets(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.content_frame.configure(bg=CorporateDashboard.COLORS["bg_main"])
        
        self.create_header()
        
        self.scroll_canvas = tk.Canvas(self.content_frame, bg=CorporateDashboard.COLORS["bg_main"],
                                       highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical",
                                       command=self.scroll_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scroll_frame = tk.Frame(self.scroll_canvas, bg=CorporateDashboard.COLORS["bg_main"])
        self.scroll_frame.bind("<Configure>",
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        
        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        
        self.scroll_canvas.bind_all("<MouseWheel>", lambda e: self.scroll_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        self.create_executive_summary()
        self.create_kpi_row()
        self.create_charts_row()
        self.create_bottom_row()
    
    def create_header(self):
        header = tk.Frame(self.content_frame, bg=CorporateDashboard.COLORS["bg_dark"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        logo_frame = tk.Frame(header, bg=CorporateDashboard.COLORS["bg_dark"])
        logo_frame.pack(side="left", padx=25, pady=12)
        
        tk.Label(logo_frame, text="TC", font=("Segoe UI", 26, "bold"),
                bg=CorporateDashboard.COLORS["bg_dark"], fg="#14b8a6").pack(side="left")
        
        brand_frame = tk.Frame(logo_frame, bg=CorporateDashboard.COLORS["bg_dark"])
        brand_frame.pack(side="left", padx=(12, 0))
        tk.Label(brand_frame, text="TIENDA CONCEPTO", font=("Segoe UI", 8, "bold"),
                bg=CorporateDashboard.COLORS["bg_dark"], fg="#64748b").pack(anchor="w")
        tk.Label(brand_frame, text="Executive Dashboard", font=("Segoe UI", 11),
                bg=CorporateDashboard.COLORS["bg_dark"], fg="#94a3b8").pack(anchor="w")
        
        title_frame = tk.Frame(header, bg=CorporateDashboard.COLORS["bg_dark"])
        title_frame.pack(side="left", padx=50)
        
        tk.Label(title_frame, text="PANEL DE CONTROL EJECUTIVO",
                font=("Segoe UI", 16, "bold"), bg=CorporateDashboard.COLORS["bg_dark"], fg="white").pack(anchor="w")
        
        now = datetime.now()
        fecha_str = now.strftime("%d de %B del %Y").capitalize()
        hora_str = now.strftime("%H:%M")
        tk.Label(title_frame, text=f"{fecha_str} | {hora_str}",
                font=("Segoe UI", 10), bg=CorporateDashboard.COLORS["bg_dark"], fg="#64748b").pack(anchor="w")
        
        actions_frame = tk.Frame(header, bg=CorporateDashboard.COLORS["bg_dark"])
        actions_frame.pack(side="right", padx=25, pady=15)
        
        refresh_btn = tk.Button(actions_frame, text="⟳ Actualizar", font=("Segoe UI", 10, "bold"),
                               bg=CorporateDashboard.COLORS["primary_light"], fg="white",
                               relief="flat", cursor="hand2", padx=15, pady=5,
                               command=self.cargar_datos)
        refresh_btn.pack(side="left", padx=5)
        
        rol_colors = {"admin": "#14b8a6", "supervisor": "#0ea5e9", "cajero": "#8b5cf6", "proveedor": "#f59e0b"}
        rol_bg = rol_colors.get(self.usuario_actual["rol"].lower(), "#8b5cf6")
        
        user_frame = tk.Frame(actions_frame, bg=CorporateDashboard.COLORS["bg_dark"])
        user_frame.pack(side="left", padx=20)
        
        tk.Label(user_frame, text=self.usuario_actual["nombre"],
                font=("Segoe UI", 11, "bold"), bg=CorporateDashboard.COLORS["bg_dark"], fg="white").pack(anchor="e")
        tk.Label(user_frame, text=f"ROL: {self.usuario_actual['rol'].upper()}", font=("Segoe UI", 8, "bold"),
                bg=rol_bg, fg="white", padx=8, pady=2).pack(anchor="e", pady=(3, 0))
    
    def create_executive_summary(self):
        summary_frame = tk.Frame(self.scroll_frame, bg=CorporateDashboard.COLORS["bg_main"])
        summary_frame.pack(fill="x", padx=25, pady=(20, 10))
        
        card_outer, card = self.create_card_shadow(summary_frame)
        card.pack(fill="x")
        
        header_bar = tk.Frame(card, bg=CorporateDashboard.COLORS["primary"], height=40)
        header_bar.pack(fill="x")
        header_bar.pack_propagate(False)
        
        tk.Label(header_bar, text="RESUMEN EJECUTIVO", font=("Segoe UI", 12, "bold"),
                bg=CorporateDashboard.COLORS["primary"], fg="white").pack(side="left", padx=20, pady=8)
        
        content = tk.Frame(card, bg="white")
        content.pack(fill="x", padx=20, pady=15)
        
        summary_items = [
            ("Ventas del Mes", "ventas_mes", "#0ea5e9"),
            ("Crecimiento", "crecimiento", "#10b981"),
            ("Tickets Promedio", "ticket_prom", "#7c3aed"),
            ("Clientes Activos", "clientes_activos", "#f59e0b"),
        ]
        
        for titulo, key, color in summary_items:
            item_frame = tk.Frame(content, bg="white")
            item_frame.pack(side="left", fill="y", padx=30)
            
            tk.Label(item_frame, text=titulo.upper(), font=("Segoe UI", 9, "bold"),
                    bg="white", fg=CorporateDashboard.COLORS["text_light"]).pack(anchor="w")
            
            valor_label = tk.Label(item_frame, text="--", font=("Segoe UI", 22, "bold"),
                                  bg="white", fg=color)
            valor_label.pack(anchor="w", pady=(5, 0))
            
            self.kpi_cards[key] = {"label": valor_label, "color": color}
    
    def create_kpi_row(self):
        kpi_frame = tk.Frame(self.scroll_frame, bg=CorporateDashboard.COLORS["bg_main"])
        kpi_frame.pack(fill="x", padx=25, pady=(10, 10))
        
        kpi_data = [
            ("VENTAS HOY", "ventas_hoy", "HNL", "#10b981", "📈"),
            ("VENTAS MES", "ventas_mes_kpi", "HNL", "#0ea5e9", "💰"),
            ("ÓRDENES", "ordenes", "und", "#7c3aed", "📋"),
            ("CLIENTES", "clientes", "und", "#f59e0b", "👥"),
            ("PRODUCTOS", "productos", "und", "#ec4899", "📦"),
            ("ALERTAS", "alertas", "und", "#ef4444", "⚠️"),
        ]
        
        for titulo, key, unidad, color, icon in kpi_data:
            card_outer, card = self.create_card_shadow(kpi_frame)
            card.pack(side="left", fill="both", expand=True, padx=5)
            
            top_bar = tk.Frame(card, bg=color, height=4)
            top_bar.pack(fill="x")
            top_bar.pack_propagate(False)
            
            content = tk.Frame(card, bg="white")
            content.pack(fill="both", expand=True, padx=15, pady=12)
            
            header_row = tk.Frame(content, bg="white")
            header_row.pack(fill="x")
            
            tk.Label(header_row, text=icon, font=("Segoe UI", 14), bg="white").pack(side="left")
            tk.Label(header_row, text=titulo, font=("Segoe UI", 9, "bold"),
                    bg="white", fg=CorporateDashboard.COLORS["text_light"]).pack(side="right")
            
            valor_label = tk.Label(content, text="--", font=("Segoe UI", 26, "bold"),
                                  bg="white", fg=color)
            valor_label.pack(anchor="w", pady=(10, 5))
            
            self.kpi_cards[key] = {"label": valor_label, "color": color, "unidad": unidad}
    
    def create_charts_row(self):
        charts_frame = tk.Frame(self.scroll_frame, bg=CorporateDashboard.COLORS["bg_main"])
        charts_frame.pack(fill="both", expand=True, padx=25, pady=(10, 10))
        
        left_card_outer, left_card = self.create_card_shadow(charts_frame)
        left_card_outer.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        self.create_chart_header(left_card, "TENDENCIA DE VENTAS", "7 días")
        self.chart_frames["ventas"] = tk.Frame(left_card, bg="white", height=220)
        self.chart_frames["ventas"].pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.chart_frames["ventas"].pack_propagate(False)
        
        right_card_outer, right_card = self.create_card_shadow(charts_frame)
        right_card_outer.pack(side="left", fill="both", expand=True, padx=(8, 0))
        
        self.create_chart_header(right_card, "DISTRIBUCIÓN POR MÉTODO DE PAGO", "Mes actual")
        self.chart_frames["metodos"] = tk.Frame(right_card, bg="white", height=220)
        self.chart_frames["metodos"].pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.chart_frames["metodos"].pack_propagate(False)
    
    def create_chart_header(self, parent, titulo, subtitulo):
        header = tk.Frame(parent, bg="white")
        header.pack(fill="x", pady=(12, 5))
        
        title_frame = tk.Frame(header, bg="white")
        title_frame.pack(side="left")
        
        tk.Label(title_frame, text=titulo, font=("Segoe UI", 12, "bold"),
                bg="white", fg=CorporateDashboard.COLORS["text_dark"]).pack(anchor="w")
        
        tk.Label(title_frame, text=subtitulo, font=("Segoe UI", 9),
                bg="white", fg=CorporateDashboard.COLORS["text_light"]).pack(anchor="w")
        
        period_frame = tk.Frame(header, bg=CorporateDashboard.COLORS["bg_main"], padx=10, pady=4)
        period_frame.pack(side="right")
        
        tk.Label(period_frame, text=subtitulo, font=("Segoe UI", 9, "bold"),
                bg=CorporateDashboard.COLORS["bg_main"], fg=CorporateDashboard.COLORS["text_medium"]).pack()
    
    def create_bottom_row(self):
        bottom_frame = tk.Frame(self.scroll_frame, bg=CorporateDashboard.COLORS["bg_main"])
        bottom_frame.pack(fill="both", expand=True, padx=25, pady=(10, 20))
        
        left_card_outer, left_card = self.create_card_shadow(bottom_frame)
        left_card_outer.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        self.create_transactions_header(left_card)
        self.chart_frames["transacciones"] = tk.Frame(left_card, bg="white", height=280)
        self.chart_frames["transacciones"].pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.chart_frames["transacciones"].pack_propagate(False)
        
        mid_card_outer, mid_card = self.create_card_shadow(bottom_frame)
        mid_card_outer.pack(side="left", fill="both", expand=True, padx=8)
        
        self.create_top_products_header(mid_card)
        self.chart_frames["productos_top"] = tk.Frame(mid_card, bg="white", height=280)
        self.chart_frames["productos_top"].pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.chart_frames["productos_top"].pack_propagate(False)
        
        right_card_outer, right_card = self.create_card_shadow(bottom_frame)
        right_card_outer.pack(side="left", fill="both", expand=True, padx=(8, 0))
        
        self.create_alerts_header(right_card)
        self.chart_frames["alertas"] = tk.Frame(right_card, bg="white", height=280)
        self.chart_frames["alertas"].pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.chart_frames["alertas"].pack_propagate(False)
    
    def create_transactions_header(self, parent):
        header = tk.Frame(parent, bg="white")
        header.pack(fill="x", pady=(12, 5))
        
        tk.Label(header, text="ÚLTIMAS TRANSACCIONES", font=("Segoe UI", 12, "bold"),
                bg="white", fg=CorporateDashboard.COLORS["text_dark"]).pack(side="left", padx=10)
        
        tk.Label(header, text="Hoy", font=("Segoe UI", 9, "bold"),
                bg=CorporateDashboard.COLORS["secondary"], fg="white",
                padx=10, pady=3).pack(side="right", padx=10)
    
    def create_top_products_header(self, parent):
        header = tk.Frame(parent, bg="white")
        header.pack(fill="x", pady=(12, 5))
        
        tk.Label(header, text="TOP PRODUCTOS", font=("Segoe UI", 12, "bold"),
                bg="white", fg=CorporateDashboard.COLORS["text_dark"]).pack(side="left", padx=10)
        
        tk.Label(header, text="Mes", font=("Segoe UI", 9, "bold"),
                bg=CorporateDashboard.COLORS["purple"], fg="white",
                padx=10, pady=3).pack(side="right", padx=10)
    
    def create_alerts_header(self, parent):
        header = tk.Frame(parent, bg="white")
        header.pack(fill="x", pady=(12, 5))
        
        tk.Label(header, text="ALERTAS DE INVENTARIO", font=("Segoe UI", 12, "bold"),
                bg="white", fg=CorporateDashboard.COLORS["text_dark"]).pack(side="left", padx=10)
        
        tk.Label(header, text="Crítico", font=("Segoe UI", 9, "bold"),
                bg=CorporateDashboard.COLORS["danger"], fg="white",
                padx=10, pady=3).pack(side="right", padx=10)
    
    def dibujar_grafico_ventas(self, datos):
        if "ventas" not in self.chart_frames:
            return
        
        try:
            if not self.chart_frames["ventas"].winfo_exists():
                return
        except:
            return
        
        for widget in self.chart_frames["ventas"].winfo_children():
            widget.destroy()
        
        canvas = tk.Canvas(self.chart_frames["ventas"], bg="white", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        self.chart_frames["ventas"].update_idletasks()
        ancho = 450
        alto = 200
        
        try:
            w = self.chart_frames["ventas"].winfo_width()
            h = self.chart_frames["ventas"].winfo_height()
            if w > 1 and h > 1:
                ancho = w
                alto = h
        except:
            pass
        
        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        
        if not datos:
            canvas.create_text(ancho/2, alto/2, text="Sin datos de ventas",
                    font=("Segoe UI", 12), fill="#94a3b8", anchor="center")
            return
        
        canvas.delete("all")
        
        max_valor = max((d["total"] for d in datos), default=1)
        
        margen_izq = 55
        margen_der = 20
        margen_sup = 25
        margen_inf = 35
        
        area_ancho = ancho - margen_izq - margen_der
        area_alto = alto - margen_sup - margen_inf
        
        num_barras = len(datos)
        ancho_barra = min(50, (area_ancho / num_barras) * 0.6)
        espacio = (area_ancho - (num_barras * ancho_barra)) / (num_barras + 1)
        
        y_base = alto - margen_inf
        
        for i, dato in enumerate(datos):
            x = margen_izq + espacio + i * (ancho_barra + espacio)
            altura = (dato["total"] / max_valor) * area_alto if max_valor > 0 else 0
            
            is_today = i == len(datos) - 1
            color = CorporateDashboard.COLORS["positive"] if is_today else CorporateDashboard.COLORS["secondary"]
            
            grad_id = canvas.create_rectangle(x, y_base - altura, x + ancho_barra, y_base,
                                              fill=color, outline="")
            
            canvas.create_rectangle(x, y_base - altura, x + ancho_barra, y_base + 3,
                                   fill=color, outline="")
            
            canvas.create_text(x + ancho_barra/2, y_base - altura - 8,
                    text=f"{dato['total']:,.0f}",
                    font=("Segoe UI", 9, "bold"), fill=color)
            
            idx = i if i < len(dias_semana) else i % 7
            canvas.create_text(x + ancho_barra/2, y_base + 12,
                    text=dias_semana[idx], font=("Segoe UI", 9, "bold"),
                    fill=CorporateDashboard.COLORS["text_dark"])
        
        for j in range(5):
            y_line = y_base - (area_alto * j / 4)
            canvas.create_line(margen_izq - 5, y_line, ancho - margen_der, y_line,
                             fill="#f1f5f9", width=1)
            
            valor_linea = max_valor * j / 4
            canvas.create_text(margen_izq - 8, y_line, text=f"{valor_linea:,.0f}",
                             font=("Segoe UI", 8), fill="#94a3b8", anchor="e")
        
        canvas.create_line(margen_izq - 5, y_base, ancho - margen_der, y_base,
                          fill=CorporateDashboard.COLORS["border_dark"], width=1)
    
    def dibujar_grafico_metodos(self, datos):
        if "metodos" not in self.chart_frames:
            return
        
        try:
            if not self.chart_frames["metodos"].winfo_exists():
                return
        except:
            return
        
        for widget in self.chart_frames["metodos"].winfo_children():
            widget.destroy()
        
        if not datos:
            frame = tk.Frame(self.chart_frames["metodos"], bg="white")
            frame.pack(fill="both", expand=True)
            tk.Label(frame, text="Sin datos de ventas este mes",
                    font=("Segoe UI", 12), bg="white", fg="#94a3b8").place(relx=0.5, rely=0.5, anchor="center")
            return
        
        colors_map = {
            "Efectivo": "#10b981",
            "Tarjeta Debito": "#0ea5e9",
            "Tarjeta Credito": "#7c3aed",
            "Transferencia": "#f59e0b",
            "Yape/Plin": "#ec4899",
            "Mixto": "#64748b"
        }
        
        total = sum(d["total"] for d in datos)
        
        chart_frame = tk.Frame(self.chart_frames["metodos"], bg="white")
        chart_frame.pack(side="left", fill="both", expand=True)
        
        pie_frame = tk.Frame(chart_frame, bg="white")
        pie_frame.pack(side="left", fill="both", expand=True)
        
        canvas = tk.Canvas(pie_frame, bg="white", highlightthickness=0, width=160, height=160)
        canvas.pack(pady=10)
        
        x_centro = 80
        y_centro = 80
        radio = 60
        
        angulo_actual = 90
        
        for dato in datos:
            metodo = dato["metodo_pago"]
            angulo_extent = (dato["total"] / total) * 360 if total > 0 else 0
            color = colors_map.get(metodo, "#64748b")
            
            if angulo_extent > 0:
                canvas.create_arc(x_centro - radio, y_centro - radio,
                               x_centro + radio, y_centro + radio,
                               start=angulo_actual - angulo_extent,
                               extent=angulo_extent,
                               fill=color, outline="white", width=2)
            
            angulo_actual -= angulo_extent
        
        canvas.create_oval(x_centro - 25, y_centro - 25, x_centro + 25, y_centro + 25,
                          fill="white", outline="#e2e8f0", width=1)
        canvas.create_text(x_centro, y_centro, text=f"{total:,.0f}",
                         font=("Segoe UI", 10, "bold"), fill="#1e293b")
        
        legend_frame = tk.Frame(chart_frame, bg="white")
        legend_frame.pack(side="left", fill="y", padx=15, pady=10)
        
        for dato in datos:
            metodo = dato["metodo_pago"]
            color = colors_map.get(metodo, "#64748b")
            pct = (dato["total"] / total * 100) if total > 0 else 0
            
            row = tk.Frame(legend_frame, bg="white")
            row.pack(fill="x", pady=4)
            
            tk.Frame(row, bg=color, width=12, height=12).pack(side="left", padx=(0, 8))
            
            tk.Label(row, text=metodo[:15], font=("Segoe UI", 9),
                    bg="white", fg="#1e293b").pack(side="left")
            
            tk.Label(row, text=f"{pct:.0f}%", font=("Segoe UI", 9, "bold"),
                    bg="white", fg=color).pack(side="right")
    
    def mostrar_transacciones(self, transacciones):
        if "transacciones" not in self.chart_frames:
            return
        
        try:
            if not self.chart_frames["transacciones"].winfo_exists():
                return
        except:
            return
        
        for widget in self.chart_frames["transacciones"].winfo_children():
            widget.destroy()
        
        frame = self.chart_frames["transacciones"]
        
        header = tk.Frame(frame, bg="#f8fafc")
        header.pack(fill="x", padx=10, pady=(5, 5))
        
        cols = [("#", 30), ("Hora", 50), ("Cliente", 140), ("Total", 80), ("Estado", 50)]
        for col, width in cols:
            tk.Label(header, text=col, font=("Segoe UI", 8, "bold"),
                    bg="#f8fafc", fg="#64748b").pack(side="left", padx=5)
        
        if not transacciones:
            tk.Label(frame, text="No hay transacciones hoy",
                    font=("Segoe UI", 10), bg="white", fg="#94a3b8").pack(pady=20)
            return
        
        for trans in transacciones[:8]:
            row = tk.Frame(frame, bg="white")
            row.pack(fill="x", padx=10, pady=2)
            
            estado = trans["estado"].lower()
            estado_colors = {
                "completada": ("#ecfdf5", "#059669"),
                "anulada": ("#fef2f2", "#dc2626"),
                "devuelta": ("#fef3c7", "#d97706")
            }
            bg_color, fg_color = estado_colors.get(estado, ("#f8fafc", "#64748b"))
            
            row.configure(bg=bg_color)
            
            tk.Label(row, text=f"{trans['id_venta']}", font=("Segoe UI", 9),
                    bg=bg_color, fg="#64748b").pack(side="left", padx=5)
            
            hora = trans["fecha_venta"][11:16] if len(trans["fecha_venta"]) > 16 else ""
            tk.Label(row, text=hora, font=("Segoe UI", 9),
                    bg=bg_color, fg="#1e293b").pack(side="left", padx=5)
            
            cliente = trans["cliente"][:18] + "..." if len(trans["cliente"]) > 18 else trans["cliente"]
            tk.Label(row, text=cliente, font=("Segoe UI", 9),
                    bg=bg_color, fg="#1e293b").pack(side="left", padx=5)
            
            tk.Label(row, text=f"L {trans['total']:,.2f}", font=("Segoe UI", 9, "bold"),
                    bg=bg_color, fg="#1e293b").pack(side="left", padx=5)
            
            estado_text = {"completada": "✓", "anulada": "✗", "devuelta": "↩"}.get(estado, "•")
            tk.Label(row, text=estado_text, font=("Segoe UI", 10, "bold"),
                    bg=bg_color, fg=fg_color).pack(side="left", padx=5)
    
    def mostrar_top_productos(self, productos):
        if "productos_top" not in self.chart_frames:
            return
        
        try:
            if not self.chart_frames["productos_top"].winfo_exists():
                return
        except:
            return
        
        for widget in self.chart_frames["productos_top"].winfo_children():
            widget.destroy()
        
        frame = self.chart_frames["productos_top"]
        
        if not productos:
            tk.Label(frame, text="Sin datos de ventas",
                    font=("Segoe UI", 10), bg="white", fg="#94a3b8").pack(pady=20)
            return
        
        max_cantidad = max((p["cantidad"] for p in productos), default=1)
        
        colors = ["#0ea5e9", "#7c3aed", "#10b981", "#f59e0b", "#ec4899"]
        
        for i, prod in enumerate(productos[:5]):
            row = tk.Frame(frame, bg="white")
            row.pack(fill="x", padx=10, pady=4)
            
            rank = tk.Label(row, text=f"#{i+1}", font=("Segoe UI", 10, "bold"),
                           bg="white", fg=colors[i % len(colors)], width=4)
            rank.pack(side="left", padx=(0, 10))
            
            info_frame = tk.Frame(row, bg="white")
            info_frame.pack(side="left", fill="x", expand=True)
            
            nombre = prod["producto"][:25] + "..." if len(prod["producto"]) > 25 else prod["producto"]
            tk.Label(info_frame, text=nombre, font=("Segoe UI", 10),
                    bg="white", fg="#1e293b").pack(anchor="w")
            
            bar_bg = tk.Frame(info_frame, bg="#f1f5f9", height=6)
            bar_bg.pack(fill="x", pady=(3, 0))
            
            bar_fill_width = (prod["cantidad"] / max_cantidad) * 100 if max_cantidad > 0 else 0
            bar_fill = tk.Frame(bar_bg, bg=colors[i % len(colors)], height=6)
            bar_fill.place(x=0, y=0, relwidth=bar_fill_width/100, relheight=1)
            
            tk.Label(row, text=f"{prod['cantidad']}", font=("Segoe UI", 9, "bold"),
                    bg="white", fg=colors[i % len(colors)]).pack(side="right")
    
    def mostrar_alertas(self, alertas):
        if "alertas" not in self.chart_frames:
            return
        
        try:
            if not self.chart_frames["alertas"].winfo_exists():
                return
        except:
            return
        
        for widget in self.chart_frames["alertas"].winfo_children():
            widget.destroy()
        
        frame = self.chart_frames["alertas"]
        
        if not alertas:
            no_alerts = tk.Frame(frame, bg="#ecfdf5")
            no_alerts.pack(fill="x", padx=10, pady=20)
            tk.Label(no_alerts, text="✓ Sin alertas - Inventario saludable",
                    font=("Segoe UI", 11), bg="#ecfdf5", fg="#059669").pack()
            return
        
        for alerta in alertas[:6]:
            stock = alerta["cant_actual"]
            minima = alerta["cant_minima"]
            
            if stock == 0:
                nivel, bg, color = "crítico", "#fef2f2", "#dc2626"
            elif stock <= minima * 0.5:
                nivel, bg, color = "crítico", "#fef2f2", "#dc2626"
            elif stock <= minima:
                nivel, bg, color = "bajo", "#fef3c7", "#d97706"
            else:
                nivel, bg, color = "medio", "#f0fdf4", "#22c55e"
            
            alert_row = tk.Frame(frame, bg=bg, padx=10, pady=8)
            alert_row.pack(fill="x", padx=10, pady=3)
            
            indicator = tk.Frame(alert_row, bg=color, width=4)
            indicator.pack(side="left", fill="y", padx=(0, 10))
            
            info = tk.Frame(alert_row, bg=bg)
            info.pack(side="left", fill="both", expand=True)
            
            nombre = alerta["producto"][:28] + "..." if len(alerta["producto"]) > 28 else alerta["producto"]
            tk.Label(info, text=nombre, font=("Segoe UI", 10, "bold"),
                    bg=bg, fg=color).pack(anchor="w")
            
            espacio = alerta.get("espacio", "N/A")
            tk.Label(info, text=f"Stock: {stock} | Mín: {minima} | {espacio}",
                    font=("Segoe UI", 8), bg=bg, fg="#64748b").pack(anchor="w")
            
            badge = tk.Label(alert_row, text=nivel.upper(), font=("Segoe UI", 8, "bold"),
                           bg=color, fg="white", padx=8, pady=2)
            badge.pack(side="right")
    
    def cargar_datos(self):
        try:
            if not self.kpi_cards or "ventas_hoy" not in self.kpi_cards:
                return
            
            try:
                if not self.kpi_cards["ventas_hoy"]["label"].winfo_exists():
                    return
            except:
                return
            
            conn = get_connection()
            cursor = conn.cursor()
            
            simbolo = "L"
            cursor.execute("SELECT simbolo FROM monedas WHERE codigo = 'HNL'")
            result = cursor.fetchone()
            if result:
                simbolo = result["simbolo"]
            
            cursor.execute("""
                SELECT COALESCE(SUM(total), 0) as total 
                FROM ventas 
                WHERE DATE(fecha_venta) = DATE('now') AND estado = 'completada'
            """)
            ventas_hoy = cursor.fetchone()["total"]
            
            cursor.execute("""
                SELECT COALESCE(SUM(total), 0) as total 
                FROM ventas 
                WHERE strftime('%Y-%m', fecha_venta) = strftime('%Y-%m', 'now') AND estado = 'completada'
            """)
            ventas_mes = cursor.fetchone()["total"]
            
            cursor.execute("""
                SELECT COALESCE(SUM(total), 0) as total 
                FROM ventas 
                WHERE strftime('%Y-%m', fecha_venta) = strftime('%Y-%m', 'now', '-1 month') AND estado = 'completada'
            """)
            ventas_mes_anterior = cursor.fetchone()["total"]
            
            crecimiento = 0
            if ventas_mes_anterior > 0:
                crecimiento = ((ventas_mes - ventas_mes_anterior) / ventas_mes_anterior) * 100
            
            cursor.execute("""
                SELECT COUNT(*) as total, AVG(total) as promedio
                FROM ventas 
                WHERE strftime('%Y-%m', fecha_venta) = strftime('%Y-%m', 'now') AND estado = 'completada'
            """)
            stats = cursor.fetchone()
            ordenes = stats["total"]
            ticket_prom = stats["promedio"] or 0
            
            cursor.execute("SELECT COUNT(*) as total FROM clientes")
            clientes = cursor.fetchone()["total"]
            
            cursor.execute("""
                SELECT COUNT(DISTINCT v.id_cliente) as total
                FROM ventas v
                WHERE strftime('%Y-%m', v.fecha_venta) = strftime('%Y-%m', 'now')
            """)
            clientes_activos = cursor.fetchone()["total"]
            
            cursor.execute("SELECT COUNT(*) as total FROM productos WHERE estado='activo'")
            productos = cursor.fetchone()["total"]
            
            cursor.execute("SELECT COUNT(*) as total FROM inventarios WHERE cant_actual <= cant_minima")
            alertas = cursor.fetchone()["total"]
            
            self.kpi_cards["ventas_hoy"]["label"].config(text=f"{simbolo} {ventas_hoy:,.2f}")
            self.kpi_cards["ventas_mes_kpi"]["label"].config(text=f"{simbolo} {ventas_mes:,.2f}")
            self.kpi_cards["ordenes"]["label"].config(text=str(ordenes))
            self.kpi_cards["clientes"]["label"].config(text=str(clientes))
            self.kpi_cards["productos"]["label"].config(text=str(productos))
            self.kpi_cards["alertas"]["label"].config(text=str(alertas))
            
            self.kpi_cards["ventas_mes"]["label"].config(text=f"{simbolo} {ventas_mes:,.2f}")
            
            crecimiento_color = CorporateDashboard.COLORS["positive"] if crecimiento >= 0 else CorporateDashboard.COLORS["negative"]
            crecimiento_text = f"{'+' if crecimiento >= 0 else ''}{crecimiento:.1f}%"
            self.kpi_cards["crecimiento"]["label"].config(text=crecimiento_text)
            self.kpi_cards["crecimiento"]["label"].config(fg=crecimiento_color)
            
            self.kpi_cards["ticket_prom"]["label"].config(text=f"{simbolo} {ticket_prom:,.2f}")
            self.kpi_cards["clientes_activos"]["label"].config(text=str(clientes_activos))
            
            cursor.execute("""
                SELECT strftime('%Y-%m-%d', fecha_venta) as dia, SUM(total) as total
                FROM ventas 
                WHERE fecha_venta >= DATE('now', '-6 days') AND estado = 'completada'
                GROUP BY strftime('%Y-%m-%d', fecha_venta)
                ORDER BY fecha_venta
            """)
            datos_ventas = [dict(row) for row in cursor.fetchall()]
            self.dibujar_grafico_ventas(datos_ventas)
            
            cursor.execute("""
                SELECT metodo_pago, SUM(total) as total
                FROM ventas 
                WHERE strftime('%Y-%m', fecha_venta) = strftime('%Y-%m', 'now') AND estado = 'completada'
                GROUP BY metodo_pago
                ORDER BY total DESC
            """)
            datos_metodos = [dict(row) for row in cursor.fetchall()]
            self.dibujar_grafico_metodos(datos_metodos)
            
            cursor.execute("""
                SELECT v.id_venta, v.fecha_venta, COALESCE(c.nombre, 'Consumidor Final') as cliente,
                       v.total, v.metodo_pago, v.estado
                FROM ventas v
                LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
                WHERE DATE(v.fecha_venta) = DATE('now')
                ORDER BY v.fecha_venta DESC LIMIT 10
            """)
            transacciones = [dict(row) for row in cursor.fetchall()]
            self.mostrar_transacciones(transacciones)
            
            cursor.execute("""
                SELECT p.nombre as producto, SUM(dv.cantidad) as cantidad
                FROM detalle_venta dv
                JOIN ventas v ON dv.id_venta = v.id_venta
                JOIN productos p ON dv.id_producto = p.id_producto
                WHERE strftime('%Y-%m', v.fecha_venta) = strftime('%Y-%m', 'now')
                  AND v.estado = 'completada'
                GROUP BY p.id_producto
                ORDER BY cantidad DESC
                LIMIT 5
            """)
            top_productos = [dict(row) for row in cursor.fetchall()]
            self.mostrar_top_productos(top_productos)
            
            cursor.execute("""
                SELECT p.nombre as producto, i.cant_actual, i.cant_minima, e.codigo as espacio
                FROM inventarios i
                JOIN productos p ON i.id_producto = p.id_producto
                JOIN espacios_exhibicion e ON i.id_espacio = e.id_espacio
                WHERE i.cant_actual <= i.cant_minima
                ORDER BY (CAST(i.cant_actual AS REAL) / NULLIF(i.cant_minima, 0)) ASC
            """)
            alertas_inv = [dict(row) for row in cursor.fetchall()]
            self.mostrar_alertas(alertas_inv)
            
            conn.close()
            
            if self.refresh_job:
                try:
                    self.parent.root.after_cancel(self.refresh_job)
                except:
                    pass
            self.refresh_job = self.parent.root.after(10000, self.cargar_datos)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
