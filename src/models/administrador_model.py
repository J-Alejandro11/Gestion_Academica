from src.database.database import db

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column('IdUsuario', db.Integer, primary_key=True)
    nombre = db.Column('Nombre', db.String(100), nullable=False)
    correo = db.Column('Correo', db.String(255), unique=True, nullable=False)
    contrasena = db.Column('Contrasena', db.LargeBinary, nullable=False)  # Contraseña encriptada
    id_rol = db.Column('IdRol', db.Integer, nullable=False)