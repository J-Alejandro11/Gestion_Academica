from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from src.controllers.docentes_controller import verificar_credenciales_docente
from src.controllers.estudiantes_controller import verificar_credenciales
from src.controllers.calificaciones_controller import obtener_calificaciones_por_semestre
from src.controllers.administrador_controller import verificar_credenciales_administrador
from src.controllers.CursoEstudiante_controller import obtener_cursos_y_estudiantes_por_docente
from src.controllers.AsignacionNotas_controller import obtener_asignacion_notas
from src.controllers.EditNotas_controller import actualizar_calificacion
from src.controllers.bitacora_controller import registrar_bitacora
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['email']
        contrasena = request.form['password']

        if not correo or not contrasena:
            flash('Por favor, completa todos los campos.', 'danger')
            return render_template('Estudiantes/LoginEstudiante.html')

        # Verificar credenciales y rol de estudiante
        if verificar_credenciales(correo, contrasena, rol_esperado=1):  # Rol de estudiante
            session['correo'] = correo
            session['rol'] = 1

            # Registrar bitácora
            from src.models.AsignarDocente_model import Usuario
            usuario = Usuario.query.filter_by(Correo=correo).first()
            if usuario:
                from src.controllers.bitacora_controller import registrar_bitacora
                registrar_bitacora(usuario.IdUsuario, "Login Estudiante", "Inicio de sesión exitoso desde el portal de estudiantes")

            flash('Inicio de sesión exitoso como Estudiante', 'success')
            return redirect(url_for('main.estudiante_dashboard'))  # Redirige al DashboardEstudiante
        else:
            flash('Correo o contraseña incorrectos', 'danger')

    return render_template('Estudiantes/LoginEstudiante.html')

@bp.route('/login-docentes', methods=['GET', 'POST'])
def login_docentes():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        if verificar_credenciales_docente(correo, contrasena):
            session['correo'] = correo
            session['rol'] = 2

            # Registrar bitácora
            from src.models.AsignarDocente_model import Usuario
            usuario = Usuario.query.filter_by(Correo=correo).first()
            if usuario:
                from src.controllers.bitacora_controller import registrar_bitacora
                registrar_bitacora(usuario.IdUsuario, "Login Docente", "Inicio de sesión exitoso desde el portal de docentes")

            print(f"✅ Sesión iniciada para el correo: {correo}")  # Depuración
            return redirect(url_for('main.panel_docente'))
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.', 'danger')

    return render_template('Docentes/LoginDocente.html')

@bp.route('/loginAdministrador', methods=['GET', 'POST'])
def login_administrador():
    if request.method == 'POST':
        correo = request.form.get('email')
        contrasena = request.form.get('password')

        if not correo or not contrasena:
            flash('Por favor, completa todos los campos.', 'danger')
            return render_template('Administradores/LoginAdministrador.html')

        if verificar_credenciales(correo, contrasena, rol_esperado=3):  # Rol de administrador
            session['correo'] = correo
            session['rol'] = 3

            # Registrar bitácora
            from src.models.AsignarDocente_model import Usuario
            usuario = Usuario.query.filter_by(Correo=correo).first()
            if usuario:
                from src.controllers.bitacora_controller import registrar_bitacora
                registrar_bitacora(usuario.IdUsuario, "Login Administrador", "Inicio de sesión exitoso ")

            flash('Inicio de sesión exitoso como Administrador', 'success')
            return redirect(url_for('main.administrador_dashboard'))
        else:
            flash('No tienes permiso para iniciar sesión como Administrador.', 'danger')

    return render_template('Administradores/LoginAdministrador.html')

@bp.route('/estudiante/dashboard')
def estudiante_dashboard():
    if session.get('rol') != 1:  # Verifica si el usuario es un estudiante
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('main.index'))

    # Redirige al dashboard (Calificaciones.html)
    return redirect(url_for('main.calificaciones'))

@bp.route('/calificaciones', methods=['GET', 'POST'])
def calificaciones():
    if 'correo' not in session or session.get('rol') != 1:  # Verifica si es un estudiante
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('main.index'))

    correo = session['correo']
    calificaciones = []
    id_semestre = None

    if request.method == 'POST':
        id_semestre = request.form.get('id_semestre')
        if id_semestre:
            calificaciones = obtener_calificaciones_por_semestre(correo, id_semestre)

    # Opciones de semestres (puedes obtenerlas dinámicamente de la base de datos si es necesario)
    semestres = [
        {'id': 1, 'nombre': 'Primer Semestre'},
        {'id': 2, 'nombre': 'Segundo Semestre'},
        {'id': 3, 'nombre': 'Tercer Semestre'},
        {'id': 4, 'nombre': 'Cuarto Semestre'},
        {'id': 5, 'nombre': 'Quinto Semestre'},
    ]

    return render_template('Estudiantes/Calificaciones.html', calificaciones=calificaciones, semestres=semestres, id_semestre=id_semestre)

@bp.route('/panel-docente', methods=['GET', 'POST'])
def panel_docente():
    if 'correo' not in session or session.get('rol') != 2:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('main.index'))

    correo_docente = session['correo']
    estudiantes = obtener_cursos_y_estudiantes_por_docente()
    asignaciones = []
    id_semestre = None

    if request.method == 'POST':
        if 'actualizar_calificacion' in request.form:
            print("Formulario recibido:", request.form)
            id_estudiante = request.form.get('id_estudiante')
            id_curso_semestre = request.form.get('id_curso_semestre')
            zona = request.form.get('zona')
            parcial1 = request.form.get('parcial1')
            parcial2 = request.form.get('parcial2')
            final = request.form.get('final')

            if id_estudiante and id_curso_semestre:
                exito = actualizar_calificacion(
                    id_estudiante,
                    id_curso_semestre,
                    zona,
                    parcial1,
                    parcial2,
                    final
                )
                if exito:
                    try:
                        from src.models.AsignarDocente_model import Usuario
                        usuario = Usuario.query.filter_by(Correo=correo_docente).first()
                        if usuario:
                            from src.controllers.bitacora_controller import registrar_bitacora
                            registrar_bitacora(
                                usuario.IdUsuario,
                                "Asignación/Actualización de Calificación",
                                f"Docente actualizó calificación para estudiante ID {id_estudiante} en curso_semestre ID {id_curso_semestre}"
                            )
                    except Exception as e:
                        print(f"Error al registrar en bitácora: {e}")
                    flash('Calificación actualizada correctamente.', 'success')
                else:
                    flash('Error al actualizar la calificación.', 'danger')
            else:
                flash('Datos incompletos para actualizar la calificación.', 'danger')

            # Mantener el semestre seleccionado después de actualizar
            id_semestre = request.form.get('id_semestre')
            if id_semestre:
                asignaciones = obtener_asignacion_notas(correo_docente, id_semestre)
        else:
            # Selección de semestre
            id_semestre = request.form.get('id_semestre')
            if id_semestre:
                asignaciones = obtener_asignacion_notas(correo_docente, id_semestre)

    semestres = [
        {'id': 1, 'nombre': 'Primer Semestre'},
        {'id': 2, 'nombre': 'Segundo Semestre'},
        {'id': 3, 'nombre': 'Tercer Semestre'},
        {'id': 4, 'nombre': 'Cuarto Semestre'},
        {'id': 5, 'nombre': 'Quinto Semestre'},
    ]

    return render_template(
        'Docentes/PanelDocente.html',
        estudiantes=estudiantes,
        asignaciones=asignaciones,
        semestres=semestres,
        id_semestre=id_semestre
    )

@bp.route('/administrador/dashboard', methods=['GET', 'POST'])
def administrador_dashboard():
    if session.get('rol') != 3:  # Solo administradores
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('main.index'))

    cursos_asignados = []
    semestre_nombre = None

    if request.method == 'POST':
        semestre_nombre = request.form.get('semestre_nombre')
        if semestre_nombre:
            from src.controllers.AsignarDocente_controller import obtener_cursos_asignados_por_semestre
            cursos_asignados = obtener_cursos_asignados_por_semestre(semestre_nombre)

    # Opciones de semestres (puedes obtenerlas dinámicamente si lo prefieres)
    semestres = [
        {'id': 1, 'nombre': '2025 - Primer Semestre'},
        {'id': 2, 'nombre': '2025 - Segundo Semestre'},
        {'id': 3, 'nombre': '2026 - Tercer Semestre'},
        {'id': 4, 'nombre': '2026 - Cuarto Semestre'},
        {'id': 5, 'nombre': '2027 - Quinto Semestre'},
    ]

    return render_template(
        'Administradores/DashboardAdministrador.html',
        cursos_asignados=cursos_asignados,
        semestres=semestres,
        semestre_nombre=semestre_nombre
    )

@bp.route('/administrador/registrar-usuario', methods=['GET', 'POST'])
def registrar_usuario():
    if session.get('rol') != 3:  # Solo administradores
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        rol = request.form.get('rol')

        if not nombre or not correo or not contrasena or not rol:
            flash('Por favor, completa todos los campos.', 'danger')
        else:
            from src.controllers.adminregister_controller import crear_usuario
            exito = crear_usuario(nombre, correo, contrasena, rol)
            if exito:
                flash('Usuario registrado exitosamente.', 'success')
            else:
                flash('Error al registrar el usuario.', 'danger')

    return render_template('Administradores/DashboardAdministrador.html')

@bp.route('/administrador/asignar-docente', methods=['POST'])
def asignar_docente():
    if session.get('rol') != 3:  # Solo administradores
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('main.index'))

    cursos_ids = request.form.getlist('cursos_ids')  # Debe ser una lista de IDs de cursos
    semestre_nombre = request.form.get('semestre_nombre')
    correo_docente = request.form.get('correo_docente')
    seccion = request.form.get('seccion')

    from src.controllers.AsignarDocente_controller import asignar_cursos_a_docente
    exito = asignar_cursos_a_docente(cursos_ids, semestre_nombre, correo_docente, seccion)

    if exito:
        flash('Cursos asignados correctamente.', 'success')
    else:
        flash('Error al asignar los cursos.', 'danger')

    return redirect(url_for('main.administrador_dashboard'))

@bp.route('/api/cursos_por_semestre', methods=['GET'])
def api_cursos_por_semestre():
    semestre_nombre = request.args.get('semestre_nombre')
    if not semestre_nombre:
        return jsonify({'cursos': []})
    from src.controllers.AsignarDocente_controller import obtener_cursos_por_semestre
    cursos = obtener_cursos_por_semestre(semestre_nombre)
    # Devuelve solo los datos necesarios
    cursos_json = [
        {'id': c.IdCurso, 'codigo': c.CodigoCurso, 'nombre': c.NombreCurso}
        for c in cursos
    ]
    return jsonify({'cursos': cursos_json})

@bp.route('/respaldo-bd', methods=['POST'])
def respaldo_bd():
    ruta = r"C:\RespaldoSQL\seguridad.bat"
    if os.path.exists(ruta):
        os.startfile(ruta)
        return jsonify({'mensaje': 'Respaldo Finalizado correctamente.'})
    else:
        return jsonify({'mensaje': 'El archivo de respaldo no existe.'}), 404
    
@bp.route('/logout')
def logout():
    session.clear()  # Limpia la sesión
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('main.index'))  # Redirige al inicio