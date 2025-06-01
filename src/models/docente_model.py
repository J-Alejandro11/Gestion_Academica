from src.database.database import db

class Docente(db.Model):
    __tablename__ = 'Docentes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(256), nullable=False)
    id_rol = db.Column(db.Integer, nullable=False)  # Relacionado con la tabla de roles

    def __init__(self, nombre, correo, contrasena, id_rol):
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.id_rol = id_rol