# 🚀 Guía de Despliegue - RehaVR
## Metodología Scrum - Sprint de Despliegue

Esta guía documenta el proceso completo de despliegue del sistema RehaVR, diseñada para capturar cada paso con screenshots para la documentación del proyecto.

---

## 📋 Índice de Capturas Necesarias

1. [Requisitos Previos](#1-requisitos-previos)
2. [Instalación de Dependencias](#2-instalación-de-dependencias)
3. [Configuración de Base de Datos](#3-configuración-de-base-de-datos)
4. [Configuración del Backend](#4-configuración-del-backend)
5. [Configuración del Frontend](#5-configuración-del-frontend)
6. [Ejecución del Sistema](#6-ejecución-del-sistema)
7. [Verificación y Pruebas](#7-verificación-y-pruebas)
8. [Despliegue con Docker](#8-despliegue-con-docker-opcional)

---

## 1. Requisitos Previos

### 📸 Captura 1: Verificar Versiones Instaladas

**Paso a seguir:**
```powershell
# Abrir PowerShell o Terminal
python --version
node --version
npm --version
mysql --version
```

**Qué capturar:**
- Terminal mostrando las versiones instaladas
- Versiones requeridas:
  - Python 3.8+
  - Node.js 16+
  - npm 8+
  - MySQL 8.0+

**Ejemplo de salida esperada:**
```
Python 3.11.0
v18.17.0
9.6.7
mysql  Ver 8.0.44
```

---

## 2. Instalación de Dependencias

### 📸 Captura 2: Instalación de Dependencias del Backend

**Paso a seguir:**
```powershell
cd backend
pip install -r requirements.txt
```

**Qué capturar:**
- Terminal mostrando la instalación de paquetes
- Progreso de instalación
- Mensaje de "Successfully installed"

**Ubicación:** `backend/requirements.txt`

---

### 📸 Captura 3: Instalación de Dependencias del Frontend

**Paso a seguir:**
```powershell
cd frontend
npm install
```

**Qué capturar:**
- Terminal mostrando la instalación de node_modules
- Progreso de instalación
- Mensaje de "added X packages"

**Ubicación:** `frontend/package.json`

---

## 3. Configuración de Base de Datos

### 📸 Captura 4: Verificar MySQL en Ejecución

**Paso a seguir:**
```powershell
# Verificar servicio MySQL
Get-Service -Name MySQL*

# O verificar conexión
mysql -u root -p -e "SELECT VERSION();"
```

**Qué capturar:**
- Servicio MySQL ejecutándose
- O conexión exitosa a MySQL

---

### 📸 Captura 5: Crear Base de Datos

**Paso a seguir:**
```sql
-- Conectar a MySQL
mysql -u root -p

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS rehabilitacion_virtual 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verificar creación
SHOW DATABASES;
```

**Qué capturar:**
- Terminal MySQL mostrando la base de datos creada
- Lista de bases de datos incluyendo `rehabilitacion_virtual`

---

### 📸 Captura 6: Importar Estructura de Tablas

**Paso a seguir:**
```sql
-- Seleccionar base de datos
USE rehabilitacion_virtual;

-- Importar scripts SQL (si los tienes)
SOURCE ruta/al/script.sql;

-- Verificar tablas creadas
SHOW TABLES;
```

**Qué capturar:**
- Tablas creadas: `pacientes`, `historial_ejercicios`, `sesiones_terapia`
- Estructura de cada tabla con `DESCRIBE nombre_tabla;`

---

## 4. Configuración del Backend

### 📸 Captura 7: Estructura del Backend

**Paso a seguir:**
```powershell
# Mostrar estructura
tree backend /F
# O
Get-ChildItem -Path backend -Recurse -Directory | Select-Object FullName
```

**Qué capturar:**
- Estructura de directorios del backend
- Archivos principales visibles

**Estructura esperada:**
```
backend/
├── app/
│   ├── controllers/
│   ├── models/
│   ├── services/
│   ├── database/
│   └── routes.py
├── config/
│   └── settings.py
└── run.py
```

---

### 📸 Captura 8: Configuración de Variables de Entorno

**Paso a seguir:**
```powershell
# Crear archivo .env en backend/ (opcional)
# O verificar configuración en config/settings.py
```

**Qué capturar:**
- Archivo de configuración abierto
- Variables de entorno o configuración visible

**Configuración esperada:**
```python
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=overload
MYSQL_DATABASE=rehabilitacion_virtual
```

---

## 5. Configuración del Frontend

### 📸 Captura 9: Estructura del Frontend

**Paso a seguir:**
```powershell
# Mostrar estructura
tree frontend /F
# O
Get-ChildItem -Path frontend -Recurse -Directory | Select-Object FullName
```

**Qué capturar:**
- Estructura de directorios del frontend
- Archivos React visibles

**Estructura esperada:**
```
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── assets/
│   └── main.jsx
├── index.html
└── package.json
```

---

### 📸 Captura 10: Configuración de Vite

**Paso a seguir:**
```powershell
# Abrir archivo de configuración
code frontend/vite.config.js
```

**Qué capturar:**
- Archivo `vite.config.js` abierto
- Configuración de proxy y puerto visible

---

## 6. Ejecución del Sistema

### 📸 Captura 11: Iniciar Backend

**Paso a seguir:**
```powershell
cd backend
python run.py
```

**Qué capturar:**
- Terminal mostrando el inicio del servidor
- Mensajes de inicio:
  - "🚀 Iniciando RehaVR Backend..."
  - "📍 Servidor: http://0.0.0.0:5000"
  - "✅ Pool de conexiones MySQL creado exitosamente"

**Mantener esta terminal abierta**

---

### 📸 Captura 12: Iniciar Frontend

**Paso a seguir:**
```powershell
# Nueva terminal
cd frontend
npm run dev
```

**Qué capturar:**
- Terminal mostrando el servidor de desarrollo
- Mensajes:
  - "VITE vX.X.X ready in XXX ms"
  - "➜ Local: http://localhost:3000/"

**Mantener esta terminal abierta**

---

### 📸 Captura 13: Verificar Servicios en Ejecución

**Paso a seguir:**
```powershell
# Verificar puertos en uso
netstat -ano | findstr :5000
netstat -ano | findstr :3000
```

**Qué capturar:**
- Puertos 5000 y 3000 en uso
- Procesos Python y Node ejecutándose

---

## 7. Verificación y Pruebas

### 📸 Captura 14: Página Principal (Home)

**Paso a seguir:**
1. Abrir navegador
2. Ir a: http://localhost:3000

**Qué capturar:**
- Página principal del sistema
- Logo "RehaVR"
- Botones "Registrarse" e "Iniciar Sesión"
- Imagen de realidad virtual

---

### 📸 Captura 15: Página de Registro

**Paso a seguir:**
1. Hacer clic en "Registrarse"
2. Completar formulario

**Qué capturar:**
- Formulario de registro
- Campos: Nombre, Email, Contraseña, Edad
- Botón "Registrarse"

---

### 📸 Captura 16: Registro Exitoso

**Paso a seguir:**
1. Completar y enviar formulario
2. Esperar respuesta

**Qué capturar:**
- Mensaje de éxito
- Redirección al Dashboard
- O mensaje de error si hay problema

---

### 📸 Captura 17: Dashboard del Usuario

**Paso a seguir:**
1. Después del registro/login
2. Ver dashboard

**Qué capturar:**
- Dashboard con mensaje "Bienvenido, [Nombre]"
- Tarjetas de ejercicios disponibles
- Botones "Comenzar Ejercicio"

---

### 📸 Captura 18: Ejercicio en Funcionamiento

**Paso a seguir:**
1. Hacer clic en "Comenzar Ejercicio"
2. Presionar ESPACIO para iniciar
3. Jugar el ejercicio

**Qué capturar:**
- Canvas del juego visible
- Mano azul y objetivo rojo
- Contadores de tiempo, puntuación y aciertos
- Instrucciones del juego

---

### 📸 Captura 19: Verificar Base de Datos

**Paso a seguir:**
```sql
-- Conectar a MySQL
mysql -u root -p

USE rehabilitacion_virtual;

-- Verificar paciente registrado
SELECT * FROM pacientes;

-- Verificar historial (después de ejercicio)
SELECT * FROM historial_ejercicios;
```

**Qué capturar:**
- Datos del paciente en la tabla `pacientes`
- Registros en `historial_ejercicios` después de completar ejercicio

---

### 📸 Captura 20: Verificar APIs Funcionando

**Paso a seguir:**
```powershell
# Probar API de pacientes
curl http://localhost:5000/api/auth/pacientes

# O usar Postman/Insomnia
```

**Qué capturar:**
- Respuesta JSON de la API
- Lista de pacientes registrados
- O interfaz de Postman/Insomnia con respuesta

---

## 8. Despliegue con Docker (Opcional)

### 📸 Captura 21: Docker Compose

**Paso a seguir:**
```powershell
# Verificar Docker instalado
docker --version
docker-compose --version

# Construir y ejecutar
docker-compose up --build
```

**Qué capturar:**
- Versiones de Docker
- Construcción de imágenes
- Contenedores iniciándose

---

### 📸 Captura 22: Contenedores en Ejecución

**Paso a seguir:**
```powershell
# Ver contenedores
docker ps
```

**Qué capturar:**
- Lista de contenedores ejecutándose
- Estados: "Up", puertos mapeados

---

## 📝 Checklist de Capturas para Scrum

### Sprint Planning - Documentación de Deploy

- [ ] Captura 1: Versiones instaladas
- [ ] Captura 2: Instalación backend
- [ ] Captura 3: Instalación frontend
- [ ] Captura 4: MySQL ejecutándose
- [ ] Captura 5: Base de datos creada
- [ ] Captura 6: Tablas creadas
- [ ] Captura 7: Estructura backend
- [ ] Captura 8: Configuración backend
- [ ] Captura 9: Estructura frontend
- [ ] Captura 10: Configuración frontend
- [ ] Captura 11: Backend ejecutándose
- [ ] Captura 12: Frontend ejecutándose
- [ ] Captura 13: Puertos en uso
- [ ] Captura 14: Página principal
- [ ] Captura 15: Formulario registro
- [ ] Captura 16: Registro exitoso
- [ ] Captura 17: Dashboard
- [ ] Captura 18: Ejercicio funcionando
- [ ] Captura 19: Datos en MySQL
- [ ] Captura 20: APIs funcionando
- [ ] Captura 21: Docker (opcional)
- [ ] Captura 22: Contenedores (opcional)

---

## 🎯 Guía Rápida para Capturas

### Orden Recomendado de Capturas:

1. **Preparación** (Capturas 1-3)
   - Verificar requisitos
   - Instalar dependencias

2. **Configuración** (Capturas 4-10)
   - Base de datos
   - Backend
   - Frontend

3. **Ejecución** (Capturas 11-13)
   - Servidores iniciando

4. **Verificación Funcional** (Capturas 14-18)
   - Interfaz de usuario
   - Funcionalidades

5. **Verificación Técnica** (Capturas 19-20)
   - Base de datos
   - APIs

6. **Docker** (Capturas 21-22) - Opcional

---

## 📸 Herramientas Recomendadas para Capturas

1. **Windows:**
   - `Win + Shift + S` - Herramienta de recorte
   - `Snipping Tool` - Herramienta de recorte avanzada
   - `ShareX` - Captura y anotación avanzada

2. **Anotaciones:**
   - Agregar flechas a elementos importantes
   - Resaltar números/valores clave
   - Agregar texto explicativo

3. **Organización:**
   - Nombrar archivos: `01-verificar-versiones.png`
   - Crear carpeta: `capturas-deploy/`
   - Ordenar por secuencia numérica

---

## 📋 Template para Documento de Deploy

```
# Deploy del Sistema RehaVR
## Sprint: [Nombre del Sprint]

### 1. Preparación del Entorno
[Captura 1: Versiones]
[Captura 2: Instalación Backend]
[Captura 3: Instalación Frontend]

### 2. Configuración
[Captura 4-6: Base de Datos]
[Captura 7-8: Backend]
[Captura 9-10: Frontend]

### 3. Ejecución
[Captura 11-13: Servidores]

### 4. Verificación
[Captura 14-18: Funcionalidades]
[Captura 19-20: Verificación Técnica]

### 5. Resultado Final
- Sistema funcionando correctamente
- Todos los servicios activos
- Base de datos conectada
```

---

**Nota:** Esta guía está diseñada para que puedas seguir cada paso y tomar capturas de pantalla que documenten el proceso completo de despliegue para tu metodología Scrum.

