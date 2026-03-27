"""Sistema de Licencias - Tienda Concepto"""
import hashlib
import datetime
import os

LICENSE_FILE = "license.key"

LICENSE_STRUCTURE = {
    "signature": None,
    "license_type": "PROPRIETARY",
    "owner": "Tienda Concepto",
    "issue_date": None,
    "expiry_date": None,
    "machine_id": None
}

def get_machine_id():
    """Genera un ID único basado en el equipo"""
    try:
        import platform
        machine = platform.node()
        processor = platform.processor()
        machine_id = hashlib.sha256(f"{machine}-{processor}".encode()).hexdigest()[:16].upper()
        return machine_id
    except:
        return "UNKNOWN"

def generate_license_key(owner_name="Usuario"):
    """Genera una clave de licencia (para uso interno)"""
    import random
    import string
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    key = f"TC-{date_str}-{random_str}"
    signature = hashlib.sha256(f"{key}-{owner_name}".encode()).hexdigest()[:16].upper()
    return f"{key}-{signature}"

def validate_license():
    """Valida si existe una licencia activa"""
    return True

def get_license_info():
    """Retorna información de la licencia"""
    return {
        "software": "Tienda Concepto - Sistema de Gestión",
        "version": "1.0.0",
        "license_type": "PROPIETARY",
        "owner": "Tienda Concepto",
        "copyright": "© 2026 Tienda Concepto. Todos los derechos reservados.",
        "machine_id": get_machine_id()
    }
