#!/usr/bin/env python3
"""
Script para ejecutar el Backend de RehaVR
Sistema de Rehabilitación Motora - Versión Refactorizada
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    if sys.version_info < (3, 8):
        print("Error: Se requiere Python 3.8 o superior")
        print(f"Versión actual: {sys.version}")
        sys.exit(1)
    print(f"Python {sys.version.split()[0]} detectado")

def get_python_executable():
    """Obtiene el ejecutable de Python del entorno virtual o del sistema"""
    # Usar ruta absoluta para que funcione desde cualquier directorio
    venv_python = Path(__file__).parent / "venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python.resolve())
    return sys.executable

def install_dependencies():
    """Instala las dependencias del backend"""
    backend_path = Path("backend")
    requirements_file = backend_path / "requirements.txt"
    
    if not requirements_file.exists():
        print("Error: No se encontró requirements.txt en el directorio backend")
        sys.exit(1)
    
    python_exe = get_python_executable()
    
    print("Instalando dependencias del backend...")
    try:
        result = subprocess.run([
            python_exe, "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error al instalar dependencias:")
            print(result.stderr)
            sys.exit(1)
        
        print("Dependencias instaladas correctamente")
    except Exception as e:
        print(f"Error al instalar dependencias: {e}")
        print("Intenta instalar manualmente con: .\\venv\\Scripts\\python.exe -m pip install -r backend/requirements.txt")
        sys.exit(1)

def setup_environment():
    """Configura las variables de entorno"""
    env_vars = {
        'FLASK_ENV': 'development',
        'FLASK_DEBUG': 'True',
        'SECRET_KEY': 'rehavr_secret_key_2024',
        'DATA_PATH': 'data/pacientes',         # relativo a backend/
        'HISTORIAL_PATH': 'data/pacientes/historial',  # relativo a backend/
        'FLASK_PORT': '5000'
    }

    for key, value in env_vars.items():
        os.environ[key] = value

    print("Variables de entorno configuradas")

def create_directories():
    """Crea los directorios necesarios"""
    directories = [
        "backend/data/pacientes/historial",
        "data/sessions",
        "logs"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    print("Directorios creados/verificados")

def run_backend():
    """Ejecuta el backend"""
    backend_path = Path("backend")
    
    if not backend_path.exists():
        print("Error: No se encontró el directorio backend")
        sys.exit(1)
    
    run_file = backend_path / "run.py"
    
    if not run_file.exists():
        print("Error: No se encontró run.py en el directorio backend")
        sys.exit(1)
    
    python_exe = get_python_executable()
    
    # Resolver ruta absoluta del archivo run.py
    run_file_abs = run_file.resolve()
    
    print("Iniciando RehaVR Backend...")
    print("Servidor: http://localhost:5000")
    print("Modo: Desarrollo")
    print("=" * 50)
    
    try:
        # Cambiar al directorio backend
        original_dir = os.getcwd()
        os.chdir(backend_path)
        
        try:
            # Ejecutar el backend usando la ruta absoluta del ejecutable
            subprocess.run([python_exe, str(run_file_abs)])
        finally:
            # Restaurar el directorio original
            os.chdir(original_dir)
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
        os.chdir(original_dir)
    except Exception as e:
        print(f"Error al ejecutar el backend: {e}")
        print(f"Python ejecutable: {python_exe}")
        print(f"Archivo run.py: {run_file_abs}")
        os.chdir(original_dir)
        sys.exit(1)

def main():
    """Función principal"""
    print("RehaVR - Sistema de Rehabilitación Motora")
    print("=" * 50)
    
    # Verificar versión de Python
    check_python_version()
    
    # Crear directorios
    create_directories()
    
    # Configurar entorno
    setup_environment()
    
    # Instalar dependencias
    install_dependencies()
    
    # Ejecutar backend
    run_backend()

if __name__ == "__main__":
    main()
