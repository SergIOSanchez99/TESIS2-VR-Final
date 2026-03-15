#!/usr/bin/env python3
"""
Script para ejecutar RehaVR - Sistema de Rehabilitación Motora
Versión Refactorizada con Arquitectura Profesional
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def print_banner():
    """Imprime el banner del proyecto"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║  🦾 RehaVR - Sistema de Rehabilitación Motora               ║
    ║  🏗️  Versión Refactorizada con Arquitectura Profesional     ║
    ║                                                              ║
    ║  Backend: Flask API con patrones MVC                        ║
    ║  Frontend: React + Vite con componentes modernos           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Verifica los requisitos del sistema"""
    print("🔍 Verificando requisitos del sistema...")
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detectado")
    
    # Verificar Node.js (para frontend)
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} detectado")
        else:
            print("⚠️  Node.js no detectado (opcional para desarrollo)")
    except FileNotFoundError:
        print("⚠️  Node.js no detectado (opcional para desarrollo)")
    
    # Verificar npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm {result.stdout.strip()} detectado")
        else:
            print("⚠️  npm no detectado (opcional para desarrollo)")
    except FileNotFoundError:
        print("⚠️  npm no detectado (opcional para desarrollo)")

def setup_directories():
    """Crea los directorios necesarios"""
    print("📁 Creando directorios necesarios...")

    directories = [
        "backend/data/pacientes/historial",
        "data/sessions",
        "logs",
        "backend/logs"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    print("✅ Directorios creados/verificados")

def get_python_executable():
    """Obtiene el ejecutable de Python del entorno virtual o del sistema"""
    venv_python = Path("venv") / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable

def install_backend_dependencies():
    """Instala las dependencias del backend"""
    print("📦 Instalando dependencias del backend...")
    
    backend_path = Path("backend")
    requirements_file = backend_path / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Error: No se encontró requirements.txt en el directorio backend")
        return False
    
    python_exe = get_python_executable()
    
    try:
        subprocess.run([
            python_exe, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True)
        print("✅ Dependencias del backend instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias del backend: {e}")
        return False

def install_frontend_dependencies():
    """Instala las dependencias del frontend"""
    print("📦 Instalando dependencias del frontend...")
    
    frontend_path = Path("frontend")
    package_json = frontend_path / "package.json"
    
    if not package_json.exists():
        print("⚠️  No se encontró package.json en el directorio frontend")
        return False
    
    try:
        subprocess.run(['npm', 'install'], cwd=frontend_path, check=True)
        print("✅ Dependencias del frontend instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias del frontend: {e}")
        return False
    except FileNotFoundError:
        print("⚠️  npm no está disponible, omitiendo instalación del frontend")
        return False

def run_backend():
    """Ejecuta el backend en un hilo separado"""
    print("🚀 Iniciando Backend...")
    
    backend_path = Path("backend")
    run_file = backend_path / "run.py"
    
    if not run_file.exists():
        print("❌ Error: No se encontró run.py en el directorio backend")
        return
    
    python_exe = get_python_executable()
    
    # Configurar variables de entorno
    env = os.environ.copy()
    env.update({
        'FLASK_ENV': 'development',
        'FLASK_DEBUG': 'True',
        'SECRET_KEY': 'rehavr_secret_key_2024',
        'DATA_PATH': 'data/pacientes',           # relativo a backend/
        'HISTORIAL_PATH': 'data/pacientes/historial'  # relativo a backend/
    })
    
    try:
        subprocess.run([python_exe, "run.py"], cwd=backend_path, env=env)
    except KeyboardInterrupt:
        print("\n🛑 Backend detenido")

def run_frontend():
    """Ejecuta el frontend en un hilo separado"""
    print("🎨 Iniciando Frontend...")
    
    frontend_path = Path("frontend")
    package_json = frontend_path / "package.json"
    
    if not package_json.exists():
        print("⚠️  No se encontró package.json en el directorio frontend")
        return
    
    try:
        subprocess.run(['npm', 'run', 'dev'], cwd=frontend_path)
    except KeyboardInterrupt:
        print("\n🛑 Frontend detenido")
    except FileNotFoundError:
        print("⚠️  npm no está disponible, omitiendo frontend")

def show_instructions():
    """Muestra las instrucciones de uso"""
    instructions = """
    📋 Instrucciones de Uso:
    
    🌐 Backend API: http://localhost:5000
    🎨 Frontend: http://localhost:3000
    
    📚 Endpoints principales:
    - GET  /api/auth/paciente          # Obtener paciente actual
    - POST /api/auth/login             # Iniciar sesión
    - GET  /api/ejercicios/            # Obtener ejercicios
    - POST /api/ejercicios/resultado   # Registrar resultado
    
    🛑 Para detener: Ctrl+C
    
    📖 Documentación:
    - README.md: Guía general
    - ARQUITECTURA.md: Documentación técnica
    """
    print(instructions)

def main():
    """Función principal"""
    print_banner()
    
    # Verificar requisitos
    check_requirements()
    
    # Crear directorios
    setup_directories()
    
    # Instalar dependencias
    backend_ok = install_backend_dependencies()
    frontend_ok = install_frontend_dependencies()
    
    if not backend_ok:
        print("❌ No se pudieron instalar las dependencias del backend")
        sys.exit(1)
    
    # Mostrar instrucciones
    show_instructions()
    
    print("🚀 Iniciando servicios...")
    print("=" * 60)
    
    # Ejecutar servicios en hilos separados
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    frontend_thread = threading.Thread(target=run_frontend, daemon=True)
    
    backend_thread.start()
    time.sleep(2)  # Esperar un poco para que el backend inicie
    
    if frontend_ok:
        frontend_thread.start()
    
    try:
        # Mantener el script ejecutándose
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servicios...")
        print("✅ Servicios detenidos correctamente")

if __name__ == "__main__":
    main()
