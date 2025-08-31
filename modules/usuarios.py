import json
import os
from datetime import datetime

RUTA_PACIENTES = os.path.join("data", "pacientes", "pacientes.json")
RUTA_HISTORIAL = os.path.join("data", "pacientes", "historial")
paciente_actual = None

def cargar_pacientes():
    if not os.path.exists(RUTA_PACIENTES):
        return []
    with open(RUTA_PACIENTES, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_pacientes(pacientes):
    with open(RUTA_PACIENTES, "w", encoding="utf-8") as f:
        json.dump(pacientes, f, ensure_ascii=False, indent=2)

def registrar_paciente():
    global paciente_actual
    print("\n--- Registro de Paciente ---")
    nombre = input("Nombre: ").strip()
    edad = input("Edad: ").strip()
    pacientes = cargar_pacientes()
    for p in pacientes:
        if p["nombre"].lower() == nombre.lower() and p["edad"] == edad:
            print("Ya existe un paciente con ese nombre y edad. Inicia sesión.")
            return False
    paciente = {"nombre": nombre, "edad": edad}
    pacientes.append(paciente)
    guardar_pacientes(pacientes)
    paciente_actual = paciente
    print("Registro exitoso.")
    return True

def iniciar_sesion():
    global paciente_actual
    print("\n--- Inicio de Sesión ---")
    nombre = input("Nombre: ").strip()
    edad = input("Edad: ").strip()
    pacientes = cargar_pacientes()
    for p in pacientes:
        if p["nombre"].lower() == nombre.lower() and p["edad"] == edad:
            paciente_actual = p
            print("Inicio de sesión exitoso.")
            return True
    print("Paciente no encontrado. Regístrate primero.")
    return False

def menu_usuarios():
    while True:
        print("\n1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            if registrar_paciente():
                break
        elif opcion == "2":
            if iniciar_sesion():
                break
        elif opcion == "3":
            exit()
        else:
            print("Opción no válida.")

def obtener_paciente_actual():
    return paciente_actual

# --- Registro y consulta de historial ---
def _ruta_historial_paciente(paciente):
    if not os.path.exists(RUTA_HISTORIAL):
        os.makedirs(RUTA_HISTORIAL)
    nombre_archivo = f"{paciente['nombre'].replace(' ', '_').lower()}_{paciente['edad']}.json"
    return os.path.join(RUTA_HISTORIAL, nombre_archivo)

def registrar_resultado(paciente, nivel, exito):
    ruta = _ruta_historial_paciente(paciente)
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            historial = json.load(f)
    else:
        historial = []
    registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "nivel": nivel,
        "exito": exito
    }
    historial.append(registro)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

def obtener_historial(paciente):
    ruta = _ruta_historial_paciente(paciente)
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return [] 