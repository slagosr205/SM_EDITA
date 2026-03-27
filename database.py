"""Configuración de la base de datos SQLite"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tienda_concepto.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL CHECK(rol IN ('admin', 'supervisor', 'cajero', 'proveedor')),
            id_proveedor_fk INTEGER,
            estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo')),
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_proveedor_fk) REFERENCES proveedores(id_proveedor)
        );
        
        CREATE TABLE IF NOT EXISTS monedas (
            id_moneda INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            simbolo TEXT NOT NULL,
            tipo TEXT DEFAULT 'local' CHECK(tipo IN ('local', 'extranjera')),
            estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo'))
        );
        
        CREATE TABLE IF NOT EXISTS config_sistema (
            id_config INTEGER PRIMARY KEY,
            moneda_local TEXT DEFAULT 'HNL',
            moneda_extranjera TEXT DEFAULT 'USD',
            tasa_cambio REAL DEFAULT 24.50,
            fecha_tasa TEXT,
            nombre_tienda TEXT DEFAULT 'Tienda Concepto',
            FOREIGN KEY (moneda_local) REFERENCES monedas(codigo),
            FOREIGN KEY (moneda_extranjera) REFERENCES monedas(codigo)
        );
        
        CREATE TABLE IF NOT EXISTS proveedores (
            id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ruc_nit TEXT UNIQUE NOT NULL,
            telefono TEXT,
            email TEXT,
            estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo')),
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS contratos (
            id_contrato INTEGER PRIMARY KEY AUTOINCREMENT,
            id_proveedor INTEGER NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT NOT NULL,
            porcentaje_comision REAL NOT NULL,
            condiciones TEXT,
            estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'vencido', 'terminado')),
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
        );
        
        CREATE TABLE IF NOT EXISTS impresiones_contrato (
            id_impresion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_contrato INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('ORIGINAL', 'COPIA')),
            fecha_impresion TEXT DEFAULT CURRENT_TIMESTAMP,
            usuario_imprime INTEGER,
            FOREIGN KEY (id_contrato) REFERENCES contratos(id_contrato),
            FOREIGN KEY (usuario_imprime) REFERENCES usuarios(id_usuario)
        );
        
        CREATE TABLE IF NOT EXISTS espacios_exhibicion (
            id_espacio INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            descripcion TEXT,
            ubicacion TEXT,
            capacidad_max INTEGER DEFAULT 100,
            estado TEXT DEFAULT 'disponible' CHECK(estado IN ('disponible', 'ocupado', 'mantenimiento'))
        );
        
        CREATE TABLE IF NOT EXISTS asignacion_espacio (
            id_asignacion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_contrato INTEGER NOT NULL,
            id_espacio INTEGER NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT,
            estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'libre')),
            FOREIGN KEY (id_contrato) REFERENCES contratos(id_contrato),
            FOREIGN KEY (id_espacio) REFERENCES espacios_exhibicion(id_espacio)
        );
        
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_proveedor INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            codigo_barras TEXT UNIQUE,
            precio_venta REAL NOT NULL,
            precio_costo REAL,
            tipo_impuesto TEXT DEFAULT 'gravado' CHECK(tipo_impuesto IN ('gravado', 'exento', 'zero')),
            estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'inactivo', 'agotado')),
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
        );
        
        CREATE TABLE IF NOT EXISTS inventarios (
            id_inventario INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER NOT NULL,
            id_espacio INTEGER NOT NULL,
            cant_actual INTEGER DEFAULT 0,
            cant_minima INTEGER DEFAULT 5,
            cant_maxima INTEGER DEFAULT 100,
            f_ultimo_surtido TEXT,
            FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
            FOREIGN KEY (id_espacio) REFERENCES espacios_exhibicion(id_espacio),
            UNIQUE(id_producto, id_espacio)
        );
        
        CREATE TABLE IF NOT EXISTS planif_surtido (
            id_planificacion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER NOT NULL,
            id_espacio INTEGER NOT NULL,
            fecha_planificada TEXT NOT NULL,
            cant_solicitada INTEGER NOT NULL,
            estado TEXT DEFAULT 'pendiente' CHECK(estado IN ('pendiente', 'aprobado', 'rechazado', 'ejecutado')),
            fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
            FOREIGN KEY (id_espacio) REFERENCES espacios_exhibicion(id_espacio)
        );
        
        CREATE TABLE IF NOT EXISTS historial_inventario (
            id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_inventario INTEGER NOT NULL,
            tipo_movimiento TEXT NOT NULL CHECK(tipo_movimiento IN ('entrada', 'salida', 'ajuste')),
            cantidad INTEGER NOT NULL,
            observaciones TEXT,
            usuario INTEGER,
            fecha_movimiento TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_inventario) REFERENCES inventarios(id_inventario),
            FOREIGN KEY (usuario) REFERENCES usuarios(id_usuario)
        );
        
        CREATE TABLE IF NOT EXISTS surtidos (
            id_surtido INTEGER PRIMARY KEY AUTOINCREMENT,
            id_planificacion INTEGER NOT NULL,
            fecha_surtido TEXT NOT NULL,
            cant_recibida INTEGER NOT NULL,
            recibido_por TEXT,
            observaciones TEXT,
            FOREIGN KEY (id_planificacion) REFERENCES planif_surtido(id_planificacion)
        );
        
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT,
            email TEXT,
            telefono TEXT,
            doc_identidad TEXT UNIQUE,
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS ventas (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            id_usuario INTEGER NOT NULL,
            fecha_venta TEXT DEFAULT CURRENT_TIMESTAMP,
            subtotal REAL NOT NULL DEFAULT 0,
            impuesto REAL NOT NULL DEFAULT 0,
            total REAL NOT NULL,
            metodo_pago TEXT CHECK(metodo_pago IN ('Efectivo', 'Tarjeta Debito', 'Tarjeta Credito', 'Transferencia', 'Yape/Plin', 'Mixto')),
            estado TEXT DEFAULT 'completada' CHECK(estado IN ('completada', 'anulada', 'devuelta')),
            referencia TEXT,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        );
        
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            id_espacio INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unit REAL NOT NULL,
            subtotal REAL NOT NULL,
            tipo_impuesto TEXT DEFAULT 'gravado',
            FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
            FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
            FOREIGN KEY (id_espacio) REFERENCES espacios_exhibicion(id_espacio)
        );
        
        CREATE TABLE IF NOT EXISTS liquidaciones (
            id_liquidacion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_proveedor INTEGER NOT NULL,
            id_contrato INTEGER NOT NULL,
            periodo_inicio TEXT NOT NULL,
            periodo_fin TEXT NOT NULL,
            total_ventas REAL NOT NULL,
            monto_comision REAL NOT NULL,
            monto_pagar REAL NOT NULL,
            estado TEXT DEFAULT 'pendiente' CHECK(estado IN ('pendiente', 'aprobada', 'pagada')),
            fecha_liquidacion TEXT DEFAULT CURRENT_TIMESTAMP,
            fecha_pago TEXT,
            FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
            FOREIGN KEY (id_contrato) REFERENCES contratos(id_contrato)
        );
        
        CREATE TABLE IF NOT EXISTS devoluciones (
            id_devolucion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER NOT NULL,
            id_usuario INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            motivo TEXT,
            estado TEXT DEFAULT 'pendiente' CHECK(estado IN ('pendiente', 'completada', 'rechazada')),
            fecha_devolucion TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        );
        
        CREATE TABLE IF NOT EXISTS auditoria (
            id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT,
            tabla TEXT NOT NULL,
            accion TEXT NOT NULL,
            id_registro INTEGER,
            datos_anteriores TEXT,
            datos_nuevos TEXT,
            usuario TEXT,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS movimientos_inventario (
            id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_inventario INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('entrada', 'salida', 'ajuste')),
            cantidad INTEGER NOT NULL,
            cantidad_anterior INTEGER,
            cantidad_nueva INTEGER,
            motivo TEXT,
            usuario TEXT,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_inventario) REFERENCES inventarios(id_inventario)
        );
    """)
    
    conn.commit()
    conn.close()

def verificar_contrasena(password: str) -> str:
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def crear_usuario_admin():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = ?", ("admin@tienda.com",))
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO usuarios (nombre, email, password_hash, rol, estado)
            VALUES (?, ?, ?, ?, ?)
        """, ("Administrador", "admin@tienda.com", verificar_contrasena("admin123"), "admin", "activo"))
        conn.commit()
    conn.close()

def inicializar_monedas():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM monedas")
    if cursor.fetchone()[0] == 0:
        monedas = [
            ("HNL", "Lempira Hondureño", "L", "local"),
            ("USD", "Dólar Estadounidense", "$", "extranjera"),
        ]
        cursor.executemany("""
            INSERT INTO monedas (codigo, nombre, simbolo, tipo)
            VALUES (?, ?, ?, ?)
        """, monedas)
        conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM config_sistema")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO config_sistema (id_config, moneda_local, moneda_extranjera, tasa_cambio, fecha_tasa, nombre_tienda)
            VALUES (1, 'HNL', 'USD', 24.50, ?, 'Tienda Concepto')
        """, (datetime.now().strftime("%Y-%m-%d"),))
        conn.commit()
    
    conn.close()

def get_config_sistema():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM config_sistema WHERE id_config = 1")
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None

def update_config_sistema(moneda_local=None, moneda_extranjera=None, tasa_cambio=None, nombre_tienda=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    if moneda_local or moneda_extranjera or tasa_cambio:
        if not moneda_local:
            cursor.execute("SELECT moneda_local FROM config_sistema WHERE id_config=1")
            moneda_local = cursor.fetchone()[0]
        if not moneda_extranjera:
            cursor.execute("SELECT moneda_extranjera FROM config_sistema WHERE id_config=1")
            moneda_extranjera = cursor.fetchone()[0]
        if not tasa_cambio:
            cursor.execute("SELECT tasa_cambio FROM config_sistema WHERE id_config=1")
            tasa_cambio = cursor.fetchone()[0]
            
        cursor.execute("""
            UPDATE config_sistema SET moneda_local=?, moneda_extranjera=?, tasa_cambio=?, fecha_tasa=?
            WHERE id_config=1
        """, (moneda_local, moneda_extranjera, tasa_cambio, datetime.now().strftime("%Y-%m-%d")))
    elif nombre_tienda:
        cursor.execute("UPDATE config_sistema SET nombre_tienda=? WHERE id_config=1", (nombre_tienda,))
    
    conn.commit()
    conn.close()

def get_monedas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM monedas WHERE estado='activo'")
    result = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return result

def seed_data_ejemplo():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM espacios_exhibicion")
    if cursor.fetchone()[0] == 0:
        espacios = [
            ("ESP-001", "Estante central 1", "Zona A - Entrada", 50),
            ("ESP-002", "Estante central 2", "Zona A - Entrada", 50),
            ("ESP-003", "Góndola lateral", "Zona B - Pasillo", 30),
            ("ESP-004", "Vitrina cristal", "Zona C - Fondo", 20),
            ("ESP-005", "Estante pared", "Zona D - Lateral", 40),
        ]
        cursor.executemany("""
            INSERT INTO espacios_exhibicion (codigo, descripcion, ubicacion, capacidad_max)
            VALUES (?, ?, ?, ?)
        """, espacios)
        
        proveedores = [
            ("Boutique Moda S.A.", "20123456789", "999888777", "moda@boutique.com"),
            ("Tecnología Plus E.I.R.L.", "20987654321", "888777666", "ventas@techplus.com"),
            ("Accesorios & Más", "20111222333", "777666555", "info@accesorios.com"),
        ]
        cursor.executemany("""
            INSERT INTO proveedores (nombre, ruc_nit, telefono, email)
            VALUES (?, ?, ?, ?)
        """, proveedores)
        
        cursor.execute("SELECT id_contrato FROM contratos LIMIT 1")
        if cursor.fetchone() is None:
            from datetime import datetime, timedelta
            fecha_inicio = datetime.now().strftime("%Y-%m-%d")
            fecha_fin = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
            
            for prov_id in [1, 2, 3]:
                cursor.execute("""
                    INSERT INTO contratos (id_proveedor, fecha_inicio, fecha_fin, porcentaje_comision, condiciones)
                    VALUES (?, ?, ?, ?, ?)
                """, (prov_id, fecha_inicio, fecha_fin, 15.0, "Contrato estándar de arrendamiento"))
        
        cursor.execute("SELECT id_espacio FROM espacios_exhibicion LIMIT 2")
        espacios_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id_contrato FROM contratos LIMIT 2")
        contratos_ids = [row[0] for row in cursor.fetchall()]
        
        for i, (esp_id, con_id) in enumerate(zip(espacios_ids, contratos_ids)):
            cursor.execute("""
                INSERT INTO asignacion_espacio (id_contrato, id_espacio, fecha_inicio)
                VALUES (?, ?, ?)
            """, (con_id, esp_id, fecha_inicio))
        
        cursor.execute("SELECT id_espacio FROM espacios_exhibicion WHERE id_espacio <= 2")
        esp_ids = [row[0] for row in cursor.fetchall()]
        
        productos = [
            (1, "Camisa Formal Blanca", "750100001", 89.90, 45.00, "gravado"),
            (1, "Pantalón Dress Negro", "750100002", 129.90, 65.00, "gravado"),
            (1, "Corbata Slim Azul", "750100003", 49.90, 25.00, "gravado"),
            (2, "Auriculares Bluetooth Pro", "750200001", 199.90, 120.00, "gravado"),
            (2, "Cargador Rápido USB-C", "750200002", 39.90, 20.00, "gravado"),
            (2, "Funda Smartphone Transparente", "750200003", 29.90, 15.00, "gravado"),
            (3, "Bolso de Cuero Marrón", "750300001", 149.90, 75.00, "gravado"),
            (3, "Cartera Mujer Clásica", "750300002", 79.90, 40.00, "gravado"),
        ]
        
        producto_ids = []
        for prod in productos:
            cursor.execute("""
                INSERT INTO productos (id_proveedor, nombre, codigo_barras, precio_venta, precio_costo, tipo_impuesto)
                VALUES (?, ?, ?, ?, ?, ?)
            """, prod)
            producto_ids.append(cursor.lastrowid)
        
        for i, (prod_id, esp_id) in enumerate(zip(producto_ids[:4], esp_ids * 2)):
            cursor.execute("""
                INSERT INTO inventarios (id_producto, id_espacio, cant_actual, cant_minima, cant_maxima)
                VALUES (?, ?, ?, ?, ?)
            """, (prod_id, esp_id, 10, 3, 50))
        
        clientes = [
            ("Carlos", "Garcia", "carlos.garcia@email.com", "999111222", "44556677"),
            ("Maria", "Lopez", "maria.lopez@email.com", "999333444", "77889900"),
            ("Juan", "Perez", "juan.perez@email.com", "999555666", "11223344"),
        ]
        cursor.executemany("""
            INSERT INTO clientes (nombre, apellido, email, telefono, doc_identidad)
            VALUES (?, ?, ?, ?, ?)
        """, clientes)
        
        from datetime import datetime, timedelta
        ventas_data = [
            (1, 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 299.80, 44.97, 344.77, "Efectivo", "completada"),
            (2, 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 149.80, 22.47, 172.27, "Tarjeta Debito", "completada"),
            (None, 1, (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), 89.90, 13.49, 103.39, "Efectivo", "completada"),
            (3, 1, (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"), 199.90, 29.99, 229.89, "Transferencia", "completada"),
            (1, 1, (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"), 179.80, 26.97, 206.77, "Tarjeta Credito", "completada"),
        ]
        
        for venta in ventas_data:
            cursor.execute("""
                INSERT INTO ventas (id_cliente, id_usuario, fecha_venta, subtotal, impuesto, total, metodo_pago, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, venta)
        
        conn.commit()
    
    conn.close()

def get_impresiones_count(id_contrato):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM impresiones_contrato WHERE id_contrato = ?
    """, (id_contrato,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def registrar_impresion(id_contrato, tipo, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO impresiones_contrato (id_contrato, tipo, usuario_imprime)
        VALUES (?, ?, ?)
    """, (id_contrato, tipo, usuario_id))
    conn.commit()
    conn.close()

def get_contrato_completo(id_contrato):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, p.nombre as proveedor_nombre, p.ruc_nit, p.telefono, p.email
        FROM contratos c
        JOIN proveedores p ON c.id_proveedor = p.id_proveedor
        WHERE c.id_contrato = ?
    """, (id_contrato,))
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None

def generar_contrato_pdf(id_contrato, tipo_documento):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
    import os
    
    contrato = get_contrato_completo(id_contrato)
    if not contrato:
        return None
    
    filename = f"contrato_{id_contrato}_{tipo_documento.replace(' ', '_')}.pdf"
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=16,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1a365d')
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14
    )
    
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica-Bold'
    )
    
    story = []
    
    story.append(Paragraph("CONTRATO DE CONCESION COMERCIAL", title_style))
    story.append(Paragraph(f"CONTRATO N° {id_contrato:04d}/2026", subtitle_style))
    story.append(Paragraph(f"<b>TIPO DE DOCUMENTO:</b> {tipo_documento}", 
                           ParagraphStyle('Tipo', parent=body_style, alignment=TA_CENTER, 
                                         fontName='Helvetica-Bold', textColor=colors.HexColor('#c53030'))))
    story.append(Spacer(1, 20))
    
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a365d')))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("I. PARTES CONTRATANTES", section_style))
    
    partes_data = [
        ["<b>CONCESIONARIO (PROVEEDOR):</b>", ""],
        ["Nombre/Razon Social:", contrato['proveedor_nombre']],
        ["RUC/NIT:", contrato['ruc_nit']],
        ["Telefono:", contrato['telefono'] or 'N/A'],
        ["Email:", contrato['email'] or 'N/A'],
        ["", ""],
        ["<b>CONCEDENTE:</b>", "TIENDA CONCEPTO S.A."],
        ["RUC/NIT:", "12345678901"],
        ["Direccion:", "Av. Principal 123, Ciudad"],
    ]
    
    partes_table = Table([[Paragraph(cell, body_style) for cell in row] for row in partes_data],
                         colWidths=[2.5*inch, 4*inch])
    partes_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(partes_table)
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("II. OBJETO DEL CONTRATO", section_style))
    story.append(Paragraph(
        "El presente contrato tiene por objeto establecer los terminos y condiciones bajo los cuales "
        "el CONCESIONARIO ofrecera sus productos en los espacios de exhibicion asignados dentro de "
        "las instalaciones de TIENDA CONCEPTO S.A., conforme a los terminos aqui establecidos.",
        body_style
    ))
    
    story.append(Paragraph("III. DURACION DEL CONTRATO", section_style))
    story.append(Paragraph(
        f"El presente contrato tendra una duracion de <b>UN (1) ANO</b>, comenzando el "
        f"<b>{contrato['fecha_inicio']}</b> y culminando el <b>{contrato['fecha_fin']}</b>, "
        "a menos que sea renovado por mutuo acuerdo entre las partes.",
        body_style
    ))
    
    story.append(Paragraph("IV. ESPACIOS ASIGNADOS", section_style))
    story.append(Paragraph(
        "Se asignan al CONCESIONARIO los espacios de exhibicion segun el detalle que figura "
        "en el Anexo I del presente contrato, el cual forma parte integrante del mismo.",
        body_style
    ))
    
    story.append(Paragraph("V. COMISION Y PAGOS", section_style))
    story.append(Paragraph(
        f"TIENDA CONCEPTO S.A. percibira una comision del <b>{contrato['porcentaje_comision']}%</b> "
        "sobre las ventas netas realizadas por el CONCESIONARIO. Esta comision sera calculada "
        "mensualmente y debitada de los fondos acumulados por el CONCESIONARIO.",
        body_style
    ))
    
    story.append(Paragraph("VI. CONDICIONES GENERALES", section_style))
    condiciones = contrato['condiciones'] or "El presente contrato se rige por las leyes vigentes de la Republica. Cualquier controversia sera resuelta por los tribunales competentes de la ciudad."
    story.append(Paragraph(condiciones, body_style))
    
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Spacer(1, 30))
    
    story.append(Paragraph("VII. FIRMAS", section_style))
    story.append(Spacer(1, 20))
    
    firma_data = [
        [Paragraph("<b>EL CONCESIONARIO</b>", ParagraphStyle('Firma', parent=body_style, alignment=TA_CENTER)),
         "",
         Paragraph("<b>EL CONCEDENTE</b>", ParagraphStyle('Firma', parent=body_style, alignment=TA_CENTER))],
        ["", "", ""],
        ["_________________________", "", "_________________________"],
        [f"{contrato['proveedor_nombre']}", "", "Representante Legal"],
        ["", "", ""],
        ["Fecha: _______________", "", "Fecha: _______________"],
    ]
    
    firma_table = Table(firma_data, colWidths=[2.5*inch, 0.5*inch, 2.5*inch])
    firma_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(firma_table)
    
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.gray))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f"Documento generado el {datetime.now().strftime('%d/%m/%Y %H:%M')} - {tipo_documento}",
        ParagraphStyle('Footer', parent=body_style, alignment=TA_CENTER, fontSize=8, textColor=colors.gray)
    ))
    
    doc.build(story)
    return filepath

if __name__ == "__main__":
    init_database()
    crear_usuario_admin()
    inicializar_monas()
    seed_data_ejemplo()
    print("Base de datos inicializada correctamente")
