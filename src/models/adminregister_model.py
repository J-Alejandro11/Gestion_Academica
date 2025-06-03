from sqlalchemy import text
from src.database.database import db

class UsuarioModel:
    @staticmethod
    def crear_usuario(nombre, correo, contrasena, rol):
        """
        Inserta un nuevo usuario en la base de datos con el rol especificado.
        """
        try:
            query = text("""
                INSERT INTO Usuarios (Nombre, Correo, Contrasena, IdRol)
                VALUES (
                    :nombre,
                    :correo,
                    HASHBYTES('SHA2_256', CONVERT(VARBINARY(100), :contrasena)),
                    (SELECT IdRol FROM Roles WHERE NombreRol = :rol)
                )
            """)
            db.session.execute(query, {
                'nombre': nombre,
                'correo': correo,
                'contrasena': contrasena,
                'rol': rol
            })
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback()
            print(f"❌ Error al crear usuario: {ex}")
            return False