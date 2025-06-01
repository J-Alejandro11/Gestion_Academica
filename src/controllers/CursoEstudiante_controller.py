from flask import session
from sqlalchemy import text
from src.database.database import db
from src.models.CursoEstudiante_model import CursoEstudiante

def obtener_cursos_y_estudiantes_por_docente():
    """
    Obtiene los cursos y estudiantes asociados al docente que ha iniciado sesión.
    """
    try:
        # Obtener el correo del docente desde la sesión
        correo_docente = session.get('correo')
        print(f"📧 Correo del docente en la sesión: {correo_docente}")  # Depuración
        if not correo_docente:
            print("❌ No se encontró el correo del docente en la sesión.")
            return []

        # Consulta SQL
        query = text("""
            SELECT 
                e.Nombre AS Estudiante,
                c.NombreCurso AS Curso,
                cs.Seccion AS Seccion,
                s.Nombre AS Semestre
            FROM CursosSemestre cs
            INNER JOIN Cursos c ON cs.IdCurso = c.IdCurso
            INNER JOIN Semestres s ON cs.IdSemestre = s.IdSemestre
            INNER JOIN Calificaciones cal ON cs.IdCursoSemestre = cal.IdCursoSemestre
            INNER JOIN Usuarios e ON cal.IdEstudiante = e.IdUsuario
            INNER JOIN Usuarios d ON cs.IdDocente = d.IdUsuario
            WHERE d.Correo = :correo_docente
            ORDER BY e.Nombre, c.NombreCurso, cs.Seccion, s.Nombre;
        """)

        # Ejecutar la consulta y devolver resultados como diccionarios
        result = db.session.execute(query, {'correo_docente': correo_docente}).mappings().all()
        print(f"📋 Resultados de la consulta: {result}")  # Depuración

        # Convertir los resultados en una lista de objetos CursoEstudiante
        cursos_estudiantes = [
            CursoEstudiante(
                estudiante=row['Estudiante'],
                curso=row['Curso'],
                seccion=row['Seccion'],
                semestre=row['Semestre']
            )
            for row in result
        ]

        print(f"✅ Cursos y estudiantes obtenidos: {cursos_estudiantes}")  # Depuración
        return cursos_estudiantes
    except Exception as ex:
        print(f"❌ Error al obtener cursos y estudiantes: {ex}")
        return []