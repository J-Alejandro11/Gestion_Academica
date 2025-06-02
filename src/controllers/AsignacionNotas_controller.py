from src.models.AsignacionNotas_model import AsignacionNotasModel

def obtener_asignacion_notas(correo_docente, id_semestre):
    """
    Llama al modelo para obtener las asignaciones de notas de los estudiantes para un docente.
    """
    return AsignacionNotasModel.asignacion_notas(correo_docente, id_semestre)