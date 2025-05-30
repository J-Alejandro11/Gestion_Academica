from sqlalchemy import text
from src.database.database import db

class CalificacionesModel:
    @staticmethod
    def obtener_calificaciones(correo, id_semestre):
        """
        Obtiene las calificaciones del estudiante para un semestre específico.
        """
        try:
            query = text("""
                SELECT 
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
                WHERE U.Correo = :correo
                  AND S.IdSemestre = :id_semestre
                ORDER BY C.NombreCurso;
            """)
            result = db.session.execute(query, {'correo': correo, 'id_semestre': id_semestre}).fetchall()
            return result
        except Exception as ex:
            print(f"❌ Error al obtener calificaciones: {ex}")
            return []