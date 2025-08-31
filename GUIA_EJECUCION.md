# 🚀 Guía de Ejecución - Sistema de Rehabilitación Virtual

## 📋 **Resumen del Proyecto**

Este es un **sistema completo de rehabilitación motora** que incluye:

- **Backend:** Aplicación Flask con MySQL
- **Frontend:** Interfaz web con Bootstrap y JavaScript
- **Base de Datos:** MySQL con gestión de pacientes, ejercicios y sesiones

## ✅ **Estado Actual: FUNCIONANDO**

### **🌐 URLs Disponibles:**

- **Página Principal:** http://localhost:5000/
- **Registro:** http://localhost:5000/registro
- **Login:** http://localhost:5000/login
- **Dashboard:** http://localhost:5000/dashboard
- **Ejercicios:** http://localhost:5000/ejercicio/1
- **Terapia Ocupacional:** http://localhost:5000/terapia_ocupacional
- **API Health:** http://localhost:5000/api/health

---

## 🔧 **Configuración del Backend**

### **1. Requisitos Previos**

```bash
# Python 3.8+ instalado
# MySQL Server ejecutándose
# Dependencias Python instaladas
```

### **2. Configuración de MySQL**

- **Host:** 127.0.0.1
- **Puerto:** 3306
- **Usuario:** root
- **Contraseña:** overload
- **Base de datos:** rehabilitacion_virtual

### **3. Instalación de Dependencias**

```bash
pip install -r requirements.txt
```

### **4. Ejecutar el Backend**

```bash
# Opción 1: Ejecutar directamente
python app_mysql.py

# Opción 2: Usar el script de backend
python run_backend.py
```

### **5. Verificar Funcionamiento**

```bash
# Verificar que el servidor esté corriendo
curl http://localhost:5000/api/health

# Verificar la página principal
curl http://localhost:5000/
```

---

## 🎨 **Configuración del Frontend**

### **1. Estructura del Frontend**

```
frontend/
├── src/
│   ├── templates/          # Plantillas HTML
│   │   ├── base.html       # Plantilla base
│   │   ├── index.html      # Página principal
│   │   ├── login.html      # Página de login
│   │   ├── registro.html   # Página de registro
│   │   ├── dashboard.html  # Dashboard del paciente
│   │   ├── ejercicio.html  # Página de ejercicios
│   │   └── terapia_ocupacional.html
│   ├── assets/
│   │   ├── css/           # Estilos CSS
│   │   ├── js/            # JavaScript
│   │   └── images/        # Imágenes
│   └── utils/             # Utilidades
```

### **2. Características del Frontend**

- **Framework:** Bootstrap 5.3.0
- **Iconos:** Font Awesome 6.0.0
- **Responsive:** Diseño adaptativo
- **Interactivo:** JavaScript para ejercicios
- **Temas:** Colores personalizados para rehabilitación

### **3. Acceso al Frontend**

El frontend se sirve automáticamente desde el backend Flask en:

- **URL Principal:** http://localhost:5000/
- **Puerto:** 5000 (mismo que el backend)

---

## 🗄️ **Base de Datos MySQL**

### **1. Estructura de Tablas**

```sql
-- Tabla de pacientes
pacientes (id, uuid, nombre, email, password_hash, edad, fecha_registro, notas, activo)

-- Tabla de historial de ejercicios
historial_ejercicios (id, paciente_id, nivel_ejercicio, exito, fecha_ejercicio, duracion_segundos, puntuacion, observaciones)

-- Tabla de sesiones de terapia
sesiones_terapia (id, paciente_id, fecha_sesion, duracion_minutos, tipo_terapia, observaciones)
```

### **2. Datos Actuales**

- **Pacientes:** 7 registrados
- **Ejercicios:** 7 registros en historial
- **Sesiones:** 5 sesiones de terapia

### **3. Vistas y Procedimientos**

- Vistas para estadísticas
- Procedimientos almacenados
- Triggers para auditoría

---

## 🎯 **Funcionalidades Principales**

### **1. Gestión de Pacientes**

- ✅ Registro de nuevos pacientes
- ✅ Inicio de sesión con autenticación
- ✅ Validación de emails duplicados
- ✅ Gestión de sesiones

### **2. Ejercicios de Rehabilitación**

- ✅ 3 niveles de dificultad
- ✅ Ejercicios interactivos con mouse
- ✅ Registro de resultados
- ✅ Seguimiento de progreso

### **3. Dashboard y Estadísticas**

- ✅ Vista general del paciente
- ✅ Historial de ejercicios
- ✅ Estadísticas de rendimiento
- ✅ Gráficos de progreso

### **4. Terapia Ocupacional**

- ✅ Sesiones de terapia
- ✅ Registro de actividades diarias
- ✅ Seguimiento de objetivos

### **5. API REST**

- ✅ Endpoints para todas las funcionalidades
- ✅ Autenticación por sesión
- ✅ Respuestas JSON
- ✅ Manejo de errores

---

## 🚀 **Comandos de Ejecución**

### **Ejecutar Todo el Sistema**

```bash
# 1. Activar entorno virtual (si existe)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 2. Ejecutar el backend
python app_mysql.py

# 3. Abrir navegador
# Ir a: http://localhost:5000/
```

### **Verificar Estado**

```bash
# Verificar API
curl http://localhost:5000/api/health

# Verificar página principal
curl http://localhost:5000/

# Verificar base de datos
mysql -u root -p -e "USE rehabilitacion_virtual; SHOW TABLES;"
```

---

## 🔍 **Troubleshooting**

### **Problema: No se conecta a MySQL**

```bash
# Verificar que MySQL esté ejecutándose
mysql -u root -p -e "SELECT VERSION();"

# Verificar configuración en .env
cat .env
```

### **Problema: Plantillas no encontradas**

```bash
# Verificar estructura de directorios
ls frontend/src/templates/

# Verificar configuración en app_mysql.py
# template_folder='frontend/src/templates'
```

### **Problema: Puerto 5000 ocupado**

```bash
# Cambiar puerto en app_mysql.py
app.run(debug=True, host='0.0.0.0', port=5001)

# O matar proceso existente
taskkill /f /im python.exe
```

---

## 📊 **Monitoreo y Logs**

### **Logs del Backend**

- Los logs aparecen en la consola donde ejecutas `python app_mysql.py`
- Incluyen información de conexión a MySQL
- Errores y advertencias de Flask

### **Estado de la Base de Datos**

```bash
# Verificar estadísticas
curl http://localhost:5000/api/health | python -m json.tool

# Verificar pacientes
mysql -u root -p -e "USE rehabilitacion_virtual; SELECT COUNT(*) FROM pacientes;"
```

---

## 🎉 **¡Sistema Listo para Usar!**

El proyecto está **completamente funcional** con:

- ✅ Backend Flask ejecutándose
- ✅ Frontend web accesible
- ✅ Base de datos MySQL conectada
- ✅ Todas las funcionalidades operativas
- ✅ API REST funcionando
- ✅ Interfaz de usuario responsive

**¡Puedes comenzar a usar el sistema de rehabilitación virtual!** 🚀
