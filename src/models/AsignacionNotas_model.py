from src.database.database import db

class Calificacion(db.Model):
    __tablename__ = 'Calificaciones'

    id = db.Column('IdCalificacion', db.Integer, primary_key=True)
    id_curso_semestre = db.Column('IdCursoSemestre', db.Integer, db.ForeignKey('CursosSemestre.IdCursoSemestre'), nullable=False)
    id_estudiante = db.Column('IdEstudiante', db.Integer, db.ForeignKey('Usuarios.IdUsuario'), nullable=False)
    nota = db.Column('Nota', db.Float, nullable=True)  # Nota asignada al estudiante

    # Relaciones
    curso_semestre = db.relationship('CursoSemestre', backref='calificaciones')
    estudiante = db.relationship('Usuario', backref='calificaciones')

    def __init__(self, id_curso_semestre, id_estudiante, nota=None):
        self.id_curso_semestre = id_curso_semestre
        self.id_estudiante = id_estudiante
        self.nota = nota