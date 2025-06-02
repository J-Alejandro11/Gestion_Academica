from sqlalchemy import text
from src.database.database import db

class EditNotasModel:
    @staticmethod
    def actualizar_calificacion(id_estudiante, id_curso_semestre, zona, parcial1, parcial2, final):
        """
        Actualiza las calificaciones de un estudiante en un curso/semestre específico.
        """
        try:
            query = text("""
                UPDATE Calificaciones
                SET Zona = :zona,
                    Parcial1 = :parcial1,
                    Parcial2 = :parcial2,
                    Final = :final
                WHERE IdEstudiante = :id_estudiante
                  AND IdCursoSemestre = :id_curso_semestre
            """)
            db.session.execute(query, {
                'zona': zona,
                'parcial1': parcial1,
                'parcial2': parcial2,
                'final': final,
                'id_estudiante': id_estudiante,
                'id_curso_semestre': id_curso_semestre
            })
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback()
            print(f"❌ Error al actualizar calificación: {ex}")
            return False