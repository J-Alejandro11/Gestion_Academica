from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.controllers.estudiantes_controller import verificar_credenciales
from src.controllers.calificaciones_controller import obtener_calificaciones_por_semestre

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

@bp.route('/login/estudiantes', methods=['GET', 'POST'])
def login_estudiantes():
    if request.method == 'POST':
        correo = request.form.get('email')
        contrasena = request.form.get('password')

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
            flash('No tienes permiso para iniciar sesión como Estudiante.', 'danger')

    return render_template('Estudiantes/LoginEstudiante.html')

@bp.route('/login/docentes', methods=['GET', 'POST'])
def login_docentes():
    if request.method == 'POST':
        correo = request.form.get('email')
        contrasena = request.form.get('password')

        if not correo or not contrasena:
            flash('Por favor, completa todos los campos.', 'danger')
            return render_template('Docentes/LoginDocente.html')

        # Verificar credenciales y rol de docente
        if verificar_credenciales(correo, contrasena, rol_esperado=2):  # Rol de docente
            session['correo'] = correo
            session['rol'] = 2
            flash('Inicio de sesión exitoso como Docente', 'success')
            return redirect(url_for('main.docente_dashboard'))
        else:
            flash('No tienes permiso para iniciar sesión como Docente.', 'danger')

    return render_template('Docentes/LoginDocente.html')

@bp.route('/login/administradores', methods=['GET', 'POST'])
def login_administradores():
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

@bp.route('/logout')
def logout():
    session.clear()  # Limpia la sesión
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('main.index'))  # Redirige al inicio