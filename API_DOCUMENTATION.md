# 📚 Documentación de APIs - RehaVR

## 🌐 Base URL
```
http://localhost:5000
```

## 📋 Índice
1. [APIs de Autenticación](#apis-de-autenticación)
2. [APIs de Ejercicios](#apis-de-ejercicios)

---

## 🔐 APIs de Autenticación

Base Path: `/api/auth`

### 1. Registrar Paciente

**Endpoint:** `POST /api/auth/registro`

**Descripción:** Registra un nuevo paciente en el sistema

**Autenticación:** No requerida

**Body (JSON):**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "password": "password123",
  "edad": "30"
}
```

**Parámetros:**
- `nombre` (string, requerido): Nombre completo del paciente
- `email` (string, requerido): Correo electrónico único
- `password` (string, requerido): Contraseña (mínimo 6 caracteres)
- `edad` (string, requerido): Edad del paciente

**Respuesta Exitosa (201):**
```json
{
  "success": true,
  "message": "Paciente registrado exitosamente",
  "paciente": {
    "id": "1",
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "edad": "30",
    "fecha_registro": "2024-11-25T10:30:00"
  }
}
```

**Errores:**
- `400`: Datos faltantes o inválidos
- `400`: Email ya registrado
- `500`: Error interno del servidor

**Ejemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/auth/registro \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "password": "password123",
    "edad": "30"
  }'
```

---

### 2. Iniciar Sesión

**Endpoint:** `POST /api/auth/login`

**Descripción:** Autentica un paciente y crea una sesión

**Autenticación:** No requerida

**Body (JSON):**
```json
{
  "email": "juan@example.com",
  "password": "password123"
}
```

**Parámetros:**
- `email` (string, requerido): Correo electrónico del paciente
- `password` (string, requerido): Contraseña del paciente

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Bienvenido/a, Juan Pérez!",
  "paciente": {
    "id": "1",
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "edad": "30",
    "fecha_registro": "2024-11-25T10:30:00"
  }
}
```

**Errores:**
- `400`: Datos faltantes
- `401`: Credenciales incorrectas
- `500`: Error interno del servidor

**Ejemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "password123"
  }' \
  -c cookies.txt
```

---

### 3. Cerrar Sesión

**Endpoint:** `POST /api/auth/logout`

**Descripción:** Cierra la sesión del paciente actual

**Autenticación:** No requerida (pero debe haber sesión activa)

**Body:** Ninguno

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Sesión cerrada exitosamente"
}
```

**Ejemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/auth/logout \
  -b cookies.txt
```

---

### 4. Obtener Paciente Actual

**Endpoint:** `GET /api/auth/paciente`

**Descripción:** Obtiene información completa del paciente autenticado con estadísticas

**Autenticación:** Requerida (sesión activa)

**Parámetros:** Ninguno

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "paciente": {
    "paciente": {
      "id": "1",
      "nombre": "Juan Pérez",
      "email": "juan@example.com",
      "edad": "30",
      "fecha_registro": "2024-11-25T10:30:00"
    },
    "ejercicios": {
      "total": 10,
      "exitosos": 8,
      "porcentaje_exito": 80.0
    },
    "historial_reciente": [
      {
        "paciente_id": "1",
        "tipo_ejercicio": "Nivel 1",
        "nivel": 1,
        "exito": true,
        "fecha": "2024-11-25T10:30:00",
        "tiempo_ejecucion": 45.5,
        "puntuacion": 85
      }
    ]
  }
}
```

**Errores:**
- `401`: No hay sesión activa
- `400`: ID de paciente no válido
- `500`: Error interno del servidor

**Ejemplo cURL:**
```bash
curl -X GET http://localhost:5000/api/auth/paciente \
  -b cookies.txt
```

---

### 5. Verificar Sesión

**Endpoint:** `GET /api/auth/verificar-sesion`

**Descripción:** Verifica si hay una sesión activa

**Autenticación:** No requerida

**Parámetros:** Ninguno

**Respuesta con Sesión Activa (200):**
```json
{
  "success": true,
  "autenticado": true,
  "paciente": {
    "id": "1",
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "edad": "30"
  }
}
```

**Respuesta sin Sesión (200):**
```json
{
  "success": true,
  "autenticado": false
}
```

**Ejemplo cURL:**
```bash
curl -X GET http://localhost:5000/api/auth/verificar-sesion \
  -b cookies.txt
```

---

## 🏋️ APIs de Ejercicios

Base Path: `/api/ejercicios`

### 1. Obtener Todos los Ejercicios

**Endpoint:** `GET /api/ejercicios/`

**Descripción:** Obtiene la lista completa de ejercicios disponibles

**Autenticación:** No requerida

**Parámetros:** Ninguno

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "ejercicios": [
    {
      "id": "ejercicio_1",
      "nombre": "Objetivo Estático",
      "descripcion": "Ejercicio de nivel 1",
      "tipo": "REHABILITACION",
      "nivel": "PRINCIPIANTE",
      "instrucciones": ["Instrucción 1", "Instrucción 2"],
      "parametros": {},
      "activo": true
    }
  ]
}
```

**Ejemplo cURL:**
```bash
curl -X GET http://localhost:5000/api/ejercicios/
```

---

### 2. Obtener Ejercicios de Rehabilitación

**Endpoint:** `GET /api/ejercicios/rehabilitacion`

**Descripción:** Obtiene solo los ejercicios de tipo rehabilitación

**Autenticación:** No requerida

**Parámetros:** Ninguno

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "ejercicios": [
    {
      "id": "ejercicio_1",
      "nombre": "Objetivo Estático",
      "tipo": "REHABILITACION",
      "nivel": "PRINCIPIANTE"
    }
  ]
}
```

**Ejemplo cURL:**
```bash
curl -X GET http://localhost:5000/api/ejercicios/rehabilitacion
```

---

### 3. Obtener Ejercicios de Terapia Ocupacional

**Endpoint:** `GET /api/ejercicios/terapia-ocupacional`

**Descripción:** Obtiene solo los ejercicios de terapia ocupacional

**Autenticación:** No requerida

**Parámetros:** Ninguno

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "ejercicios": [
    {
      "id": "ejercicio_to_1",
      "nombre": "Actividades de la Vida Diaria",
      "tipo": "TERAPIA_OCUPACIONAL",
      "nivel": "INTERMEDIO"
    }
  ]
}
```

**Ejemplo cURL:**
```bash
curl -X GET http://localhost:5000/api/ejercicios/terapia-ocupacional
```

---

### 4. Obtener Ejercicio por ID

**Endpoint:** `GET /api/ejercicios/<ejercicio_id>`

**Descripción:** Obtiene información detallada de un ejercicio específico

**Autenticación:** No requerida

**Parámetros URL:**
- `ejercicio_id` (string): ID del ejercicio

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "ejercicio": {
    "id": "ejercicio_1",
    "nombre": "Objetivo Estático",
    "descripcion": "Ejercicio de nivel 1",
    "tipo": "REHABILITACION",
    "nivel": "PRINCIPIANTE",
    "instrucciones": ["Instrucción 1", "Instrucción 2"],
    "parametros": {},
    "activo": true
  }
}
```

**Errores:**
- `404`: Ejercicio no encontrado
- `500`: Error interno del servidor

**Ejemplo cURL:**
```bash
curl -X GET http://localhost:5000/api/ejercicios/ejercicio_1
```

---

### 5. Registrar Resultado de Ejercicio

**Endpoint:** `POST /api/ejercicios/resultado`

**Descripción:** Registra el resultado de un ejercicio realizado por el paciente

**Autenticación:** Requerida (sesión activa)

**Body (JSON):**
```json
{
  "ejercicio_id": "ejercicio_1",
  "exito": true,
  "tiempo_ejecucion": 45.5,
  "puntuacion": 85,
  "observaciones": "Ejercicio completado correctamente"
}
```

**Parámetros:**
- `ejercicio_id` (string, requerido): ID del ejercicio realizado
- `exito` (boolean, requerido): Si el ejercicio fue exitoso
- `tiempo_ejecucion` (float, opcional): Tiempo en segundos
- `puntuacion` (integer, opcional): Puntuación obtenida
- `observaciones` (string, opcional): Observaciones adicionales

**Respuesta Exitosa (201):**
```json
{
  "success": true,
  "message": "Resultado registrado exitosamente",
  "resultado": {
    "paciente_id": "1",
    "tipo_ejercicio": "ejercicio_1",
    "nivel": 1,
    "exito": true,
    "fecha": "2024-11-25T10:30:00",
    "tiempo_ejecucion": 45.5,
    "puntuacion": 85,
    "observaciones": "Ejercicio completado correctamente"
  }
}
```

**Errores:**
- `401`: No hay sesión activa
- `400`: Datos faltantes o inválidos
- `500`: Error interno del servidor

**Ejemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/ejercicios/resultado \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "ejercicio_id": "ejercicio_1",
    "exito": true,
    "tiempo_ejecucion": 45.5,
    "puntuacion": 85
  }'
```

---

### 6. Obtener Historial de Ejercicios

**Endpoint:** `GET /api/ejercicios/historial`

**Descripción:** Obtiene el historial completo de ejercicios del paciente autenticado

**Autenticación:** Requerida (sesión activa)

**Parámetros:** Ninguno

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "historial": [
    {
      "paciente_id": "1",
      "tipo_ejercicio": "ejercicio_1",
      "nivel": 1,
      "exito": true,
      "fecha": "2024-11-25T10:30:00",
      "tiempo_ejecucion": 45.5,
      "puntuacion": 85,
      "observaciones": "Ejercicio completado correctamente"
    },
    {
      "paciente_id": "1",
      "tipo_ejercicio": "ejercicio_2",
      "nivel": 2,
      "exito": false,
      "fecha": "2024-11-24T09:15:00",
      "tiempo_ejecucion": 30.0,
      "puntuacion": 60
    }
  ]
}
```

**Errores:**
- `401`: No hay sesión activa
- `400`: ID de paciente no válido
- `500`: Error interno del servidor

**Ejemplo cURL:**
```bash
curl -X GET http://localhost:5000/api/ejercicios/historial \
  -b cookies.txt
```

---

### 7. Obtener Estadísticas de Ejercicio

**Endpoint:** `GET /api/ejercicios/<ejercicio_id>/estadisticas`

**Descripción:** Obtiene estadísticas específicas de un ejercicio para el paciente autenticado

**Autenticación:** Requerida (sesión activa)

**Parámetros URL:**
- `ejercicio_id` (string): ID del ejercicio

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "estadisticas": {
    "ejercicio_id": "ejercicio_1",
    "total_intentos": 10,
    "exitosos": 8,
    "fallidos": 2,
    "porcentaje_exito": 80.0,
    "puntuacion_promedio": 82.5,
    "tiempo_promedio": 42.3
  }
}
```

**Errores:**
- `401`: No hay sesión activa
- `400`: ID de paciente no válido
- `500`: Error interno del servidor

**Ejemplo cURL:**
```bash
curl -X GET http://localhost:5000/api/ejercicios/ejercicio_1/estadisticas \
  -b cookies.txt
```

---

### 8. Obtener Recomendación de Ejercicio

**Endpoint:** `GET /api/ejercicios/recomendacion`

**Descripción:** Obtiene una recomendación de ejercicio basada en el historial del paciente

**Autenticación:** Requerida (sesión activa)

**Parámetros:** Ninguno

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "recomendacion": {
    "id": "ejercicio_2",
    "nombre": "Objetivo en Movimiento",
    "descripcion": "Ejercicio de nivel 2",
    "tipo": "REHABILITACION",
    "nivel": "INTERMEDIO",
    "razon": "Basado en tu progreso, te recomendamos este ejercicio"
  }
}
```

**Respuesta sin Recomendación (200):**
```json
{
  "success": true,
  "recomendacion": null,
  "message": "No hay recomendaciones disponibles"
}
```

**Errores:**
- `401`: No hay sesión activa
- `400`: ID de paciente no válido
- `500`: Error interno del servidor

**Ejemplo cURL:**
```bash
curl -X GET http://localhost:5000/api/ejercicios/recomendacion \
  -b cookies.txt
```

---

## 🔒 Autenticación

El sistema usa **sesiones basadas en cookies**. Después de iniciar sesión exitosamente, las cookies se envían automáticamente en las siguientes peticiones.

### Manejo de Sesiones

- Las sesiones se crean automáticamente al iniciar sesión
- Las cookies se envían automáticamente con `withCredentials: true` en el frontend
- Las sesiones expiran después de 1 hora de inactividad
- Para cerrar sesión, usar el endpoint `/api/auth/logout`

### Headers Requeridos

Para peticiones que requieren autenticación, asegúrate de incluir las cookies de sesión:

```bash
curl -b cookies.txt -c cookies.txt http://localhost:5000/api/auth/login
```

---

## 📊 Códigos de Estado HTTP

- `200`: Petición exitosa
- `201`: Recurso creado exitosamente
- `400`: Solicitud incorrecta (datos inválidos)
- `401`: No autorizado (sesión requerida)
- `403`: Acceso prohibido
- `404`: Recurso no encontrado
- `500`: Error interno del servidor

---

## 🧪 Ejemplos de Uso Completo

### Flujo Completo: Registro → Login → Ejercicio

```bash
# 1. Registrar paciente
curl -X POST http://localhost:5000/api/auth/registro \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "password": "password123",
    "edad": "30"
  }' \
  -c cookies.txt

# 2. Iniciar sesión
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "password123"
  }' \
  -b cookies.txt -c cookies.txt

# 3. Obtener ejercicios disponibles
curl -X GET http://localhost:5000/api/ejercicios/ \
  -b cookies.txt

# 4. Registrar resultado de ejercicio
curl -X POST http://localhost:5000/api/ejercicios/resultado \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "ejercicio_id": "ejercicio_1",
    "exito": true,
    "tiempo_ejecucion": 45.5,
    "puntuacion": 85
  }'

# 5. Ver historial
curl -X GET http://localhost:5000/api/ejercicios/historial \
  -b cookies.txt

# 6. Cerrar sesión
curl -X POST http://localhost:5000/api/auth/logout \
  -b cookies.txt
```

---

## 📝 Notas Importantes

1. **Base URL**: Todas las URLs son relativas a `http://localhost:5000`
2. **Content-Type**: Todas las peticiones POST requieren `Content-Type: application/json`
3. **Cookies**: Las cookies se manejan automáticamente en el navegador, pero en cURL necesitas usar `-b` y `-c`
4. **Sesiones**: Las sesiones se almacenan en el servidor y se identifican mediante cookies
5. **CORS**: El backend está configurado para aceptar peticiones desde `http://localhost:3000`

---

**Última actualización:** 25 de Noviembre, 2024

