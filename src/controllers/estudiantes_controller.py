from sqlalchemy import text
from src.database.database import db

def verificar_credenciales(correo, contrasena, rol_esperado):
    """
    Verifica si el correo, la contraseña y el rol ingresados coinciden con un usuario en la base de datos.
    Retorna True si las credenciales y el rol son correctos, de lo contrario False.
    """
    try:
        query = text("""
            SELECT IdRol
            FROM Usuarios
            WHERE Correo = :correo
              AND Contrasena = HASHBYTES('SHA2_256', :contrasena)
              AND IdRol = :rol
        """)
        result = db.session.execute(query, {'correo': correo, 'contrasena': contrasena, 'rol': rol_esperado}).fetchone()
        return result is not None
    except Exception as ex:
        print(f"❌ Error al verificar credenciales: {ex}")
        return False
    