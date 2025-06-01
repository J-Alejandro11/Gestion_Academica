from sqlalchemy import text
from src.database.database import db

def verificar_credenciales_administrador(correo, contrasena):
    """
    Verifica si el correo y la contraseña ingresados corresponden a un administrador en la base de datos.
    Retorna True si las credenciales son correctas, de lo contrario False.
    """
    try:
        query = text("""
            SELECT IdRol
            FROM Usuarios
            WHERE Correo = :correo
              AND Contrasena = HASHBYTES('SHA2_256', :contrasena)
              AND IdRol = 3 
        """)
        result = db.session.execute(query, {'correo': correo, 'contrasena': contrasena}).fetchone()
        return result is not None
    except Exception as ex:
        print(f"❌ Error al verificar credenciales de administrador: {ex}")
        return False