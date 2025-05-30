from src.models.calificaciones_model import CalificacionesModel

def obtener_calificaciones_por_semestre(correo, id_semestre):
    """
    Llama al modelo para obtener las calificaciones del estudiante.
    """
    return CalificacionesModel.obtener_calificaciones(correo, id_semestre)