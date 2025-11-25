#!/usr/bin/env python3
"""
Script para generar el diagrama de arquitectura en formato imagen
Requiere: plantuml (Java) o graphviz
"""

import os
import subprocess
import sys

def generar_con_plantuml():
    """Genera el diagrama usando PlantUML"""
    print("🔄 Generando diagrama con PlantUML...")
    
    # Verificar si PlantUML está instalado
    try:
        result = subprocess.run(['plantuml', '-version'], 
                              capture_output=True, text=True)
        print("✅ PlantUML encontrado")
    except FileNotFoundError:
        print("❌ PlantUML no encontrado. Instalando...")
        print("\n📦 Para instalar PlantUML:")
        print("   1. Descarga Java: https://www.java.com/")
        print("   2. Descarga PlantUML: http://plantuml.com/download")
        print("   3. O instala con: brew install plantuml (macOS)")
        print("   4. O usa el JAR directamente:")
        print("      java -jar plantuml.jar diagrama_arquitectura.puml")
        return False
    
    # Generar diagrama
    try:
        subprocess.run(['plantuml', '-tpng', 'diagrama_arquitectura.puml'], 
                      check=True)
        print("✅ Diagrama generado: diagrama_arquitectura.png")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al generar diagrama: {e}")
        return False

def generar_con_mermaid():
    """Genera el diagrama usando Mermaid CLI"""
    print("🔄 Generando diagrama con Mermaid...")
    
    # Verificar si Mermaid CLI está instalado
    try:
        result = subprocess.run(['mmdc', '--version'], 
                              capture_output=True, text=True)
        print("✅ Mermaid CLI encontrado")
    except FileNotFoundError:
        print("❌ Mermaid CLI no encontrado.")
        print("\n📦 Para instalar Mermaid CLI:")
        print("   npm install -g @mermaid-js/mermaid-cli")
        return False
    
    # Generar diagrama
    try:
        subprocess.run(['mmdc', '-i', 'DIAGRAMA_ARQUITECTURA.md', 
                       '-o', 'diagrama_arquitectura.png'], 
                      check=True)
        print("✅ Diagrama generado: diagrama_arquitectura.png")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al generar diagrama: {e}")
        return False

def mostrar_instrucciones():
    """Muestra instrucciones para generar el diagrama"""
    print("\n" + "="*60)
    print("📊 INSTRUCCIONES PARA GENERAR EL DIAGRAMA")
    print("="*60)
    
    print("\n🔹 OPCIÓN 1: PlantUML (Recomendado para trabajos académicos)")
    print("-" * 60)
    print("1. Instala Java: https://www.java.com/")
    print("2. Descarga PlantUML: http://plantuml.com/download")
    print("3. Genera el diagrama:")
    print("   java -jar plantuml.jar diagrama_arquitectura.puml")
    print("\n   O usa el servidor online:")
    print("   http://www.plantuml.com/plantuml/uml/")
    print("   (Copia el contenido de diagrama_arquitectura.puml)")
    
    print("\n🔹 OPCIÓN 2: PlantUML Online (Recomendado)")
    print("-" * 60)
    print("1. Abre: http://www.plantuml.com/plantuml/uml/")
    print("2. Copia el contenido de cualquier archivo .puml")
    print("3. Pégalo y descarga como PNG o SVG")
    
    print("\n🔹 OPCIÓN 3: VS Code Extension")
    print("-" * 60)
    print("1. Instala extensión: 'PlantUML'")
    print("2. Abre cualquier archivo .puml")
    print("3. Presiona Alt+D para previsualizar")
    print("4. Exporta como imagen")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    print("🎨 Generador de Diagrama de Arquitectura - RehaVR")
    print("="*60)
    
    # Intentar generar con PlantUML
    if os.path.exists('diagrama_arquitectura.puml'):
        if generar_con_plantuml():
            sys.exit(0)
    
    # Intentar generar con Mermaid (ya no existe DIAGRAMA_ARQUITECTURA.md)
    # Los diagramas ahora están en archivos .puml individuales
    
    # Si no se pudo generar, mostrar instrucciones
    mostrar_instrucciones()

