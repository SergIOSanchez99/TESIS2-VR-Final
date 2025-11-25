# 🚀 Guía de Ejecución - RehaVR

## 📋 Requisitos Previos

- **Python 3.8+** instalado
- **Node.js 16+** y **npm** instalados
- **MySQL** (opcional, si se usa base de datos)

---

## 🎯 Opción 1: Ejecución Automática (Recomendada)

### Ejecutar todo el proyecto con un solo comando:

```bash
python start_project.py
```

Este script:
- ✅ Verifica requisitos
- ✅ Instala dependencias automáticamente
- ✅ Inicia backend y frontend simultáneamente

**URLs disponibles:**
- 🌐 Backend API: http://localhost:5000
- 🎨 Frontend: http://localhost:3000

---

## 🔧 Opción 2: Ejecución Manual

### **Backend (Flask API)**

```bash
# 1. Navegar al directorio backend
cd backend

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el servidor
python run.py
```

**Backend disponible en:** http://localhost:5000

### **Frontend (React + Vite)**

```bash
# 1. Navegar al directorio frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Ejecutar servidor de desarrollo
npm run dev
```

**Frontend disponible en:** http://localhost:3000

---

## 🐳 Opción 3: Docker Compose

```bash
# Construir y ejecutar contenedores
docker-compose up --build

# O en modo detached (segundo plano)
docker-compose up -d --build
```

**URLs:**
- 🌐 Backend: http://localhost:5000
- 🎨 Frontend: http://localhost:3000

**Detener contenedores:**
```bash
docker-compose down
```

---

## ⚙️ Variables de Entorno (Opcional)

### Backend (.env en raíz del proyecto)

```env
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=rehavr_secret_key_2024
DATA_PATH=data/pacientes
```

### Frontend (.env en directorio frontend)

```env
VITE_API_URL=http://localhost:5000
```

---

## 🔍 Verificar que Funciona

### Backend
```bash
# Verificar API
curl http://localhost:5000/api/health
```

### Frontend
Abrir en navegador: http://localhost:3000

---

## 🛑 Detener Servicios

- **Ejecución automática:** `Ctrl + C` en la terminal
- **Ejecución manual:** `Ctrl + C` en cada terminal
- **Docker:** `docker-compose down`

---

## 📝 Notas Importantes

1. **Backend debe ejecutarse primero** antes del frontend
2. **Puerto 5000** debe estar libre para el backend
3. **Puerto 3000** debe estar libre para el frontend
4. Si usas **entorno virtual**, actívalo antes:
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

---

## 🎯 Endpoints Principales

- `GET /api/auth/paciente` - Obtener paciente actual
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/ejercicios/` - Obtener ejercicios
- `POST /api/ejercicios/resultado` - Registrar resultado

---

## ❌ Solución de Problemas

### Puerto ocupado
```bash
# Cambiar puerto en backend/run.py o frontend/vite.config.js
```

### Dependencias no instaladas
```bash
# Backend
pip install -r backend/requirements.txt

# Frontend
cd frontend && npm install
```

### Error de conexión entre frontend y backend
- Verificar que `VITE_API_URL` apunte a `http://localhost:5000`
- Verificar que CORS esté habilitado en el backend

