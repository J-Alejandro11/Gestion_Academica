from src.models.EditNotas_model import EditNotasModel

def actualizar_calificacion(id_estudiante, id_curso_semestre, zona, parcial1, parcial2, final):
    """
    Llama al modelo para actualizar las calificaciones de un estudiante en un curso/semestre específico.
    """
    return EditNotasModel.actualizar_calificacion(
        id_estudiante, id_curso_semestre, zona, parcial1, parcial2, final
    )