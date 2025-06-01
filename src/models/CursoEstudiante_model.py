from src.database.database import db

class CursoEstudiante:
    def __init__(self, estudiante, curso, seccion, semestre):
        self.estudiante = estudiante
        self.curso = curso
        self.seccion = seccion
        self.semestre = semestre