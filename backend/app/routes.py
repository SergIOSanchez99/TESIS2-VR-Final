"""
Rutas de la Aplicación - Blueprint Pattern
Responsable de definir las rutas de la API
"""
from flask import Blueprint, render_template, redirect, url_for, session
from functools import wraps

from .controllers.auth_controller import AuthController
from .controllers.ejercicio_controller import EjercicioController


# Blueprint principal
main_bp = Blueprint('main', __name__)

# Blueprint de autenticación
auth_bp = Blueprint('auth', __name__)

# Blueprint de ejercicios
ejercicio_bp = Blueprint('ejercicios', __name__)

# Instanciar controladores
auth_controller = AuthController()
ejercicio_controller = EjercicioController()


def login_required(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'paciente' not in session:
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# RUTAS PRINCIPALES (FRONTEND)
# ============================================================================

@main_bp.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@main_bp.route('/registro')
def registro():
    """Página de registro"""
    return render_template('registro.html')


@main_bp.route('/login')
def login():
    """Página de inicio de sesión"""
    return render_template('login.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard del paciente"""
    paciente = session.get('paciente')
    return render_template('dashboard.html', paciente=paciente)


@main_bp.route('/ejercicio/<int:nivel>')
@login_required
def ejercicio(nivel):
    """Página de ejercicio"""
    paciente = session.get('paciente')
    return render_template('ejercicio.html', paciente=paciente, nivel=nivel)


@main_bp.route('/terapia_ocupacional')
@login_required
def terapia_ocupacional():
    """Página de terapia ocupacional"""
    paciente = session.get('paciente')
    return render_template('terapia_ocupacional.html', paciente=paciente)


@main_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.pop('paciente', None)
    return redirect(url_for('main.index'))


# ============================================================================
# RUTAS DE AUTENTICACIÓN (API)
# ============================================================================

@auth_bp.route('/registro', methods=['POST'])
def registrar_paciente():
    """API para registrar paciente"""
    return auth_controller.registrar_paciente()


@auth_bp.route('/login', methods=['POST'])
def iniciar_sesion():
    """API para iniciar sesión"""
    return auth_controller.iniciar_sesion()


@auth_bp.route('/logout', methods=['POST'])
def cerrar_sesion():
    """API para cerrar sesión"""
    return auth_controller.cerrar_sesion()


@auth_bp.route('/paciente', methods=['GET'])
def obtener_paciente_actual():
    """API para obtener paciente actual"""
    return auth_controller.obtener_paciente_actual()


@auth_bp.route('/verificar-sesion', methods=['GET'])
def verificar_sesion():
    """API para verificar sesión"""
    return auth_controller.verificar_sesion()


@auth_bp.route('/pacientes', methods=['GET'])
def obtener_todos_pacientes():
    """API para obtener lista de todos los pacientes"""
    return auth_controller.obtener_todos_pacientes()


# ============================================================================
# RUTAS DE EJERCICIOS (API)
# ============================================================================

@ejercicio_bp.route('/', methods=['GET'])
def obtener_ejercicios():
    """API para obtener todos los ejercicios"""
    return ejercicio_controller.obtener_ejercicios()


@ejercicio_bp.route('/rehabilitacion', methods=['GET'])
def obtener_ejercicios_rehabilitacion():
    """API para obtener ejercicios de rehabilitación"""
    return ejercicio_controller.obtener_ejercicios_rehabilitacion()


@ejercicio_bp.route('/terapia-ocupacional', methods=['GET'])
def obtener_ejercicios_terapia_ocupacional():
    """API para obtener ejercicios de terapia ocupacional"""
    return ejercicio_controller.obtener_ejercicios_terapia_ocupacional()


@ejercicio_bp.route('/<ejercicio_id>', methods=['GET'])
def obtener_ejercicio_por_id(ejercicio_id):
    """API para obtener ejercicio por ID"""
    return ejercicio_controller.obtener_ejercicio_por_id(ejercicio_id)


@ejercicio_bp.route('/resultado', methods=['POST'])
def registrar_resultado():
    """API para registrar resultado de ejercicio"""
    return ejercicio_controller.registrar_resultado()


@ejercicio_bp.route('/historial', methods=['GET'])
def obtener_historial():
    """API para obtener historial de ejercicios"""
    return ejercicio_controller.obtener_historial()


@ejercicio_bp.route('/<ejercicio_id>/estadisticas', methods=['GET'])
def obtener_estadisticas_ejercicio(ejercicio_id):
    """API para obtener estadísticas de un ejercicio"""
    return ejercicio_controller.obtener_estadisticas_ejercicio(ejercicio_id)


@ejercicio_bp.route('/recomendacion', methods=['GET'])
def obtener_recomendacion():
    """API para obtener recomendación de ejercicio"""
    return ejercicio_controller.obtener_recomendacion()
