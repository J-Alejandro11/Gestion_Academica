from sqlalchemy import text
from src.database.database import db

def verificar_credenciales_docente(correo, contrasena):
    """
    Verifica si el correo y la contraseña ingresados corresponden a un docente en la base de datos.
    Retorna True si las credenciales son correctas, de lo contrario False.
    """
    try:
        query = text("""
            SELECT IdRol
            FROM Usuarios
            WHERE Correo = :correo
              AND Contrasena = HASHBYTES('SHA2_256', :contrasena)
              AND IdRol = 2 -- Suponiendo que el rol de docente tiene el IdRol = 2
        """)
        result = db.session.execute(query, {'correo': correo, 'contrasena': contrasena}).fetchone()
        return result is not None
    except Exception as ex:
        print(f"❌ Error al verificar credenciales de docente: {ex}")
        return False