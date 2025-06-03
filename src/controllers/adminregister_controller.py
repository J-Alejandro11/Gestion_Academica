from src.models.adminregister_model import UsuarioModel

def crear_usuario(nombre, correo, contrasena, rol):
    """
    Llama al modelo para crear un nuevo usuario con el rol especificado.
    """
    return UsuarioModel.crear_usuario(nombre, correo, contrasena, rol)