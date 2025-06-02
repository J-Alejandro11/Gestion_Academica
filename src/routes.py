from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from src.controllers.docentes_controller import verificar_credenciales_docente
from src.controllers.estudiantes_controller import verificar_credenciales
from src.controllers.calificaciones_controller import obtener_calificaciones_por_semestre
from src.controllers.administrador_controller import verificar_credenciales_administrador
from src.controllers.CursoEstudiante_controller import obtener_cursos_y_estudiantes_por_docente
from src.controllers.AsignacionNotas_controller import obtener_asignacion_notas

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
            session['correo'] = correo  # Guardar el correo en la sesión
            session['rol'] = 2
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

        # Verificar credenciales y rol de administrador
        if verificar_credenciales(correo, contrasena, rol_esperado=3):  # Rol de administrador
            session['correo'] = correo
            session['rol'] = 3
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

@bp.route('/logout')
def logout():
    session.clear()  # Limpia la sesión
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('main.index'))  # Redirige al inicio
