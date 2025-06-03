from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import db  # Ajusta el import según tu estructura

class Semestre(db.Model):
    __tablename__ = 'Semestres'
    IdSemestre = Column(Integer, primary_key=True)
    Nombre = Column(String(100), unique=True, nullable=False)
    cursos_semestre = relationship('CursoSemestre', back_populates='semestre')

class Curso(db.Model):
    __tablename__ = 'Cursos'
    IdCurso = Column(Integer, primary_key=True)
    CodigoCurso = Column(String(20), unique=True, nullable=False)
    NombreCurso = Column(String(100), nullable=False)
    cursos_semestre = relationship('CursoSemestre', back_populates='curso')

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    IdUsuario = Column(Integer, primary_key=True)
    Nombre = Column(String(100), nullable=False)
    Correo = Column(String(100), unique=True, nullable=False)
    cursos_semestre = relationship('CursoSemestre', back_populates='docente')

class CursoSemestre(db.Model):
    __tablename__ = 'CursosSemestre'
    IdCursoSemestre = Column(Integer, primary_key=True)
    IdSemestre = Column(Integer, ForeignKey('Semestres.IdSemestre'), nullable=False)
    IdCurso = Column(Integer, ForeignKey('Cursos.IdCurso'), nullable=False)
    IdDocente = Column(Integer, ForeignKey('Usuarios.IdUsuario'), nullable=False)
    Seccion = Column(String(10), nullable=False)

    semestre = relationship('Semestre', back_populates='cursos_semestre')
    curso = relationship('Curso', back_populates='cursos_semestre')
    docente = relationship('Usuario', back_populates='cursos_semestre')