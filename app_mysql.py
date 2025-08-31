# -*- coding: utf-8 -*-
"""
Aplicación Flask con MySQL - Sistema de Rehabilitación Virtual
Versión actualizada para usar base de datos MySQL
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os
import sys
from datetime import datetime

# Agregar el directorio backend al path para importar el gestor MySQL
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
from app.database.mysql_manager import MySQLDatabaseService

app = Flask(__name__, 
           template_folder='frontend/src/templates',
           static_folder='frontend/src/assets/static',
           static_url_path='/static')
app.secret_key = 'rehavr_secret_key_2024'
CORS(app)

# Inicializar el servicio de base de datos MySQL
try:
    db_service = MySQLDatabaseService()
    print("✅ Servicio de base de datos MySQL inicializado")
except Exception as e:
    print(f"❌ Error al inicializar MySQL: {e}")
    db_service = None

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de pacientes"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            nombre = data.get('nombre', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            edad = data.get('edad', '').strip()
            
            # Validaciones
            if not nombre or not email or not password or not edad:
                return jsonify({'error': 'Completa todos los campos'}), 400
            
            try:
                edad_int = int(edad)
                if edad_int < 1 or edad_int > 120:
                    return jsonify({'error': 'La edad debe estar entre 1 y 120 años'}), 400
            except ValueError:
                return jsonify({'error': 'La edad debe ser un número válido'}), 400
            
            # Verificar si el email ya existe
            try:
                if db_service.pacientes.verificar_email_existe(email):
                    return jsonify({'error': 'Ya existe un paciente con ese email'}), 400
            except Exception as e:
                print(f"Error verificando email existente: {e}")
                # Continuar con el registro si hay error en la verificación
            
            # Crear nuevo paciente en MySQL
            nuevo_paciente = db_service.pacientes.crear_paciente(
                nombre=nombre,
                email=email,
                password=password,
                edad=edad_int,
                notas="Registrado desde la aplicación web"
            )
            
            # Guardar en sesión
            session['paciente'] = {
                'id': nuevo_paciente['id'],
                'nombre': nuevo_paciente['nombre'],
                'email': nuevo_paciente['email'],
                'edad': nuevo_paciente['edad']
            }
            
            return jsonify({
                'success': True, 
                'message': f'Registro exitoso. Bienvenido/a, {nombre}!'
            })
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            print(f"Error en registro: {e}")
            return jsonify({'error': 'Error interno del servidor'}), 500
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            
            if not email or not password:
                return jsonify({'error': 'Completa todos los campos'}), 400
            
            # Autenticar paciente en MySQL
            paciente = db_service.pacientes.autenticar_paciente(email, password)
            
            if paciente:
                # Guardar en sesión
                session['paciente'] = {
                    'id': paciente['id'],
                    'nombre': paciente['nombre'],
                    'email': paciente['email'],
                    'edad': paciente['edad']
                }
                
                return jsonify({
                    'success': True, 
                    'message': f'Bienvenido/a, {paciente["nombre"]}!'
                })
            else:
                return jsonify({'error': 'Email o contraseña incorrectos'}), 401
                
        except Exception as e:
            print(f"Error en login: {e}")
            return jsonify({'error': 'Error interno del servidor'}), 500
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard del paciente"""
    if 'paciente' not in session:
        return redirect(url_for('index'))
    
    try:
        paciente = session['paciente']
        # Obtener historial desde MySQL
        historial = db_service.historial.obtener_historial_paciente(paciente['id'], limit=10)
        
        return render_template('dashboard.html', paciente=paciente, historial=historial)
    except Exception as e:
        print(f"Error en dashboard: {e}")
        return render_template('dashboard.html', paciente=paciente, historial=[])

@app.route('/ejercicio/<int:nivel>')
def ejercicio(nivel):
    """Página de ejercicio"""
    if 'paciente' not in session:
        return redirect(url_for('index'))
    
    paciente = session['paciente']
    return render_template('ejercicio.html', paciente=paciente, nivel=nivel)

@app.route('/api/registrar_resultado', methods=['POST'])
def api_registrar_resultado():
    """API para registrar resultado de ejercicio"""
    if 'paciente' not in session:
        return jsonify({'error': 'No hay sesión activa'}), 401
    
    try:
        data = request.get_json()
        nivel = data.get('nivel')
        exito = data.get('exito', False)
        duracion = data.get('duracion', 0)
        puntuacion = data.get('puntuacion', 0)
        observaciones = data.get('observaciones', '')
        
        paciente = session['paciente']
        
        # Registrar ejercicio en MySQL
        ejercicio_registrado = db_service.historial.registrar_ejercicio(
            paciente_id=paciente['id'],
            nivel_ejercicio=f"Ejercicio nivel {nivel}",
            exito=exito,
            duracion_segundos=duracion,
            puntuacion=puntuacion,
            observaciones=observaciones
        )
        
        return jsonify({
            'success': True,
            'message': 'Ejercicio registrado exitosamente',
            'ejercicio': ejercicio_registrado
        })
        
    except Exception as e:
        print(f"Error al registrar resultado: {e}")
        return jsonify({'error': 'Error al registrar el ejercicio'}), 500

@app.route('/api/historial')
def api_historial():
    """API para obtener historial del paciente"""
    if 'paciente' not in session:
        return jsonify({'error': 'No hay sesión activa'}), 401
    
    try:
        paciente = session['paciente']
        historial = db_service.historial.obtener_historial_paciente(paciente['id'], limit=50)
        
        return jsonify({'historial': historial})
        
    except Exception as e:
        print(f"Error al obtener historial: {e}")
        return jsonify({'error': 'Error al obtener el historial'}), 500

@app.route('/api/paciente')
def api_paciente():
    """API para obtener información del paciente actual"""
    if 'paciente' not in session:
        return jsonify({'error': 'No hay sesión activa'}), 401
    
    return jsonify({'paciente': session['paciente']})

@app.route('/api/estadisticas')
def api_estadisticas():
    """API para obtener estadísticas del paciente"""
    if 'paciente' not in session:
        return jsonify({'error': 'No hay sesión activa'}), 401
    
    try:
        paciente = session['paciente']
        historial = db_service.historial.obtener_historial_paciente(paciente['id'])
        
        # Calcular estadísticas
        total_ejercicios = len(historial)
        ejercicios_exitosos = len([e for e in historial if e['exito']])
        promedio_puntuacion = sum(e['puntuacion'] for e in historial) / total_ejercicios if total_ejercicios > 0 else 0
        
        estadisticas = {
            'total_ejercicios': total_ejercicios,
            'ejercicios_exitosos': ejercicios_exitosos,
            'tasa_exito': (ejercicios_exitosos / total_ejercicios * 100) if total_ejercicios > 0 else 0,
            'promedio_puntuacion': round(promedio_puntuacion, 2)
        }
        
        return jsonify({'estadisticas': estadisticas})
        
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return jsonify({'error': 'Error al obtener estadísticas'}), 500

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.pop('paciente', None)
    return redirect(url_for('index'))

@app.route('/terapia_ocupacional')
def terapia_ocupacional():
    """Página de terapia ocupacional"""
    if 'paciente' not in session:
        return redirect(url_for('index'))
    
    paciente = session['paciente']
    return render_template('terapia_ocupacional.html', paciente=paciente)

@app.route('/api/crear_sesion_terapia', methods=['POST'])
def api_crear_sesion_terapia():
    """API para crear una sesión de terapia"""
    if 'paciente' not in session:
        return jsonify({'error': 'No hay sesión activa'}), 401
    
    try:
        data = request.get_json()
        duracion = data.get('duracion', 0)
        tipo_terapia = data.get('tipo_terapia', 'Terapia general')
        observaciones = data.get('observaciones', '')
        
        paciente = session['paciente']
        
        # Crear sesión en MySQL
        sesion = db_service.sesiones.crear_sesion(
            paciente_id=paciente['id'],
            duracion_minutos=duracion,
            tipo_terapia=tipo_terapia,
            observaciones=observaciones
        )
        
        return jsonify({
            'success': True,
            'message': 'Sesión de terapia registrada exitosamente',
            'sesion': sesion
        })
        
    except Exception as e:
        print(f"Error al crear sesión de terapia: {e}")
        return jsonify({'error': 'Error al registrar la sesión'}), 500

@app.route('/api/sesiones_terapia')
def api_sesiones_terapia():
    """API para obtener sesiones de terapia del paciente"""
    if 'paciente' not in session:
        return jsonify({'error': 'No hay sesión activa'}), 401
    
    try:
        paciente = session['paciente']
        sesiones = db_service.sesiones.obtener_sesiones_paciente(paciente['id'], limit=20)
        
        return jsonify({'sesiones': sesiones})
        
    except Exception as e:
        print(f"Error al obtener sesiones: {e}")
        return jsonify({'error': 'Error al obtener las sesiones'}), 500

@app.route('/api/health')
def api_health():
    """API para verificar el estado del sistema"""
    try:
        # Verificar conexión a MySQL
        mysql_status = db_service.test_connection() if db_service else False
        
        # Obtener información de la base de datos
        db_info = db_service.get_database_info() if db_service else None
        
        return jsonify({
            'status': 'healthy',
            'mysql_connected': mysql_status,
            'database_info': db_info,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    if db_service is None:
        print("❌ No se pudo inicializar la base de datos MySQL")
        print("💡 Verifica la configuración de MySQL")
        exit(1)
    
    print("🚀 Iniciando aplicación Flask con MySQL...")
    print("🌐 Backend: http://localhost:5000")
    print("📊 Health check: http://localhost:5000/api/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
