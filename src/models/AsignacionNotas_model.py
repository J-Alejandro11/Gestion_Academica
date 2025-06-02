from sqlalchemy import text
from src.database.database import db

class AsignacionNotasModel:
    @staticmethod
    def asignacion_notas(correo_docente, id_semestre):
        """
        Obtiene las asignaciones de notas de los estudiantes para un docente en un semestre específico.
        """
        try:
            query = text("""
                SELECT 
                    Cal.IdEstudiante,
                    Cal.IdCursoSemestre,
                    U.Nombre AS Estudiante,
                    C.NombreCurso,
                    CS.Seccion,
                    S.Nombre AS Semestre,
                    Cal.Zona,
                    Cal.Parcial1,
                    Cal.Parcial2,
                    Cal.Final,
                    Cal.Total
                FROM Calificaciones Cal
                JOIN Usuarios U ON Cal.IdEstudiante = U.IdUsuario
                JOIN CursosSemestre CS ON Cal.IdCursoSemestre = CS.IdCursoSemestre
                JOIN Cursos C ON CS.IdCurso = C.IdCurso
                JOIN Semestres S ON CS.IdSemestre = S.IdSemestre
                JOIN Usuarios Docente ON CS.IdDocente = Docente.IdUsuario
                WHERE Docente.Correo = :correo_docente
                  AND S.IdSemestre = :id_semestre
                ORDER BY C.NombreCurso, U.Nombre;
            """)
            result = db.session.execute(query, {'correo_docente': correo_docente, 'id_semestre': id_semestre}).fetchall()
            return result
        except Exception as ex:
            print(f"❌ Error al obtener asignaciones de notas: {ex}")
            return []