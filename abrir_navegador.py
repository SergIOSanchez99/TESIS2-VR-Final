#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para abrir automáticamente el navegador con la aplicación
"""

import webbrowser
import time
import requests

def verificar_servidor():
    """Verifica que el servidor esté funcionando"""
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def abrir_aplicacion():
    """Abre la aplicación en el navegador"""
    print("🌐 Verificando que el servidor esté funcionando...")
    
    # Esperar hasta que el servidor esté listo
    for i in range(30):  # Esperar máximo 30 segundos
        if verificar_servidor():
            print("✅ Servidor funcionando correctamente")
            break
        print(f"⏳ Esperando servidor... ({i+1}/30)")
        time.sleep(1)
    else:
        print("❌ No se pudo conectar al servidor")
        print("💡 Asegúrate de que la aplicación esté ejecutándose con: python app_mysql.py")
        return
    
    # URLs disponibles
    urls = {
        "Página Principal": "http://localhost:5000/",
        "Registro": "http://localhost:5000/registro",
        "Login": "http://localhost:5000/login",
        "Dashboard": "http://localhost:5000/dashboard",
        "Ejercicio Nivel 1": "http://localhost:5000/ejercicio/1",
        "Terapia Ocupacional": "http://localhost:5000/terapia_ocupacional",
        "API Health": "http://localhost:5000/api/health"
    }
    
    print("\n🚀 Abriendo aplicación en el navegador...")
    print("📋 URLs disponibles:")
    
    for nombre, url in urls.items():
        print(f"   • {nombre}: {url}")
    
    # Abrir la página principal
    print(f"\n🌐 Abriendo: {urls['Página Principal']}")
    webbrowser.open(urls['Página Principal'])
    
    print("\n✅ ¡Aplicación abierta en el navegador!")
    print("💡 Si el navegador no se abre automáticamente, copia y pega esta URL:")
    print(f"   {urls['Página Principal']}")

if __name__ == '__main__':
    abrir_aplicacion()
