# ------------------------------------------------------------------
# 1. Inyección de SQL (CWE‑89)
# ------------------------------------------------------------------
def obtener_usuario_por_nombre(nombre: str) -> dict:
    """
    Recupera la información de un usuario a partir de su nombre.
    
    Vulnerabilidad: Se construye la consulta SQL concatenando directamente
    el parámetro `nombre`. Un atacante puede inyectar código SQL y
    manipular la base de datos (CWE‑89).
    
    Parámetros:
        nombre (str): Nombre del usuario a buscar.
    
    Retorna:
        dict: Registro del usuario o None si no existe.
    """
    # ❌ Vulnerable
    query = f"SELECT * FROM usuarios WHERE nombre = '{nombre}'"
    
    # Supongamos que `db` es un cursor de SQLite
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchone()


# ------------------------------------------------------------------
# 2. XSS en salida HTML (CWE‑79)
# ------------------------------------------------------------------
def generar_mensaje_html(mensaje: str) -> str:
    """
    Devuelve un fragmento HTML que muestra el mensaje del usuario.
    
    Vulnerabilidad: El contenido de `mensaje` se inserta directamente
    en el HTML sin escapar. Un atacante puede enviar un script que
    se ejecutará en el navegador del visitante (CWE‑79).
    
    Parámetros:
        mensaje (str): Texto que el usuario desea mostrar.
    
    Retorna:
        str: Fragmento HTML seguro (si se corrige).
    """
    # ❌ Vulnerable
    return f"<p>{mensaje}</p>"