from src.database.database import db
from sqlalchemy import text

def registrar_bitacora(id_usuario, accion, detalles=None):
    sql = text("EXEC sp_RegistrarBitacora :id_usuario, :accion, :detalles")
    db.session.execute(
        sql,
        {'id_usuario': id_usuario, 'accion': accion, 'detalles': detalles}
    )
    db.session.commit()