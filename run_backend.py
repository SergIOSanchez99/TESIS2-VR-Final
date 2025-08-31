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
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detectado")

def install_dependencies():
    """Instala las dependencias del backend"""
    backend_path = Path("backend")
    requirements_file = backend_path / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Error: No se encontró requirements.txt en el directorio backend")
        sys.exit(1)
    
    print("📦 Instalando dependencias del backend...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True)
        print("✅ Dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        sys.exit(1)

def setup_environment():
    """Configura las variables de entorno"""
    env_vars = {
        'FLASK_ENV': 'development',
        'FLASK_DEBUG': 'True',
        'SECRET_KEY': 'rehavr_secret_key_2024',
        'DATA_PATH': 'data/pacientes'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("🔧 Variables de entorno configuradas")

def create_directories():
    """Crea los directorios necesarios"""
    directories = [
        "data/pacientes/historial",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("📁 Directorios creados/verificados")

def run_backend():
    """Ejecuta el backend"""
    backend_path = Path("backend")
    
    if not backend_path.exists():
        print("❌ Error: No se encontró el directorio backend")
        sys.exit(1)
    
    run_file = backend_path / "run.py"
    
    if not run_file.exists():
        print("❌ Error: No se encontró run.py en el directorio backend")
        sys.exit(1)
    
    print("🚀 Iniciando RehaVR Backend...")
    print("📍 Servidor: http://localhost:5000")
    print("🔧 Modo: Desarrollo")
    print("=" * 50)
    
    try:
        # Cambiar al directorio backend
        os.chdir(backend_path)
        
        # Ejecutar el backend
        subprocess.run([sys.executable, "run.py"])
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al ejecutar el backend: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    print("🦾 RehaVR - Sistema de Rehabilitación Motora")
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
