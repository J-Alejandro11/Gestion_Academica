from src.models.AsignarDocente_model import db, Semestre, CursoSemestre, Curso, Usuario

def obtener_semestres():
    return Semestre.query.all()

def obtener_docentes():
    return Usuario.query.all()

def obtener_cursos_por_semestre(nombre_semestre):
    semestre = Semestre.query.filter_by(Nombre=nombre_semestre).first()
    if not semestre:
        return []
    cursos_semestre = CursoSemestre.query.filter_by(IdSemestre=semestre.IdSemestre).all()
    cursos = []
    for cs in cursos_semestre:
        curso = Curso.query.get(cs.IdCurso)
        if curso:
            cursos.append(curso)
    return cursos

def asignar_docente_a_cursos(semestre_nombre, seccion, correo_docente, cursos_ids):
    semestre = Semestre.query.filter_by(Nombre=semestre_nombre).first()
    docente = Usuario.query.filter_by(Correo=correo_docente).first()
    if not semestre or not docente or not cursos_ids:
        return False, 'Debe seleccionar semestre, docente y al menos un curso.'

    for curso_id in cursos_ids:
        asignacion = CursoSemestre(
            IdSemestre=semestre.IdSemestre,
            IdCurso=int(curso_id),
            IdDocente=docente.IdUsuario,
            Seccion=seccion
        )
        db.session.add(asignacion)
    db.session.commit()
    return True, 'Asignación realizada correctamente.'

def obtener_cursos_asignados_por_semestre(nombre_semestre):
    semestre = Semestre.query.filter_by(Nombre=nombre_semestre).first()
    if not semestre:
        return []
    cursos_semestre = CursoSemestre.query.filter_by(IdSemestre=semestre.IdSemestre).all()
    cursos_asignados = []
    for cs in cursos_semestre:
        curso = Curso.query.get(cs.IdCurso)
        docente = Usuario.query.get(cs.IdDocente)
        cursos_asignados.append({
            'codigo': curso.CodigoCurso if curso else '',
            'nombre': curso.NombreCurso if curso else '',
            'docente': docente.Nombre if docente else '',
            'seccion': cs.Seccion
        })
    return cursos_asignados