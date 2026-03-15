# 🦾 RehaVR - Sistema de Rehabilitación Motora

Sistema profesional de rehabilitación motora con arquitectura moderna, patrones de diseño y buenas prácticas de desarrollo.

## 🏗️ Arquitectura del Proyecto

```
RehaVR/
├── backend/                    # Backend API (Flask)
│   ├── app/
│   │   ├── controllers/       # Controladores MVC
│   │   │   ├── auth_controller.py
│   │   │   └── ejercicio_controller.py
│   │   ├── models/           # Modelos de datos
│   │   │   ├── ejercicio.py
│   │   │   └── paciente.py
│   │   ├── services/         # Lógica de negocio
│   │   │   ├── ejercicio_service.py
│   │   │   └── paciente_service.py
│   │   ├── database/         # Gestión de base de datos
│   │   │   └── mysql_manager.py
│   │   ├── utils/            # Utilidades
│   │   └── routes.py         # Definición de rutas y blueprints
│   ├── config/               # Configuración
│   │   └── settings.py
│   ├── data/                 # Datos locales del backend
│   │   └── pacientes/
│   ├── requirements.txt      # Dependencias Python
│   └── run.py               # Entry point del backend
├── frontend/                  # Frontend (Flask Templates + React)
│   ├── src/
│   │   ├── templates/       # Templates Jinja2 (servidos por Flask)
│   │   │   ├── base.html
│   │   │   ├── index.html
│   │   │   ├── login.html
│   │   │   ├── registro.html
│   │   │   ├── dashboard.html
│   │   │   ├── ejercicio.html
│   │   │   └── terapia_ocupacional.html
│   │   ├── components/      # Componentes React (opcionales)
│   │   │   ├── EjercicioCanvas.jsx
│   │   │   └── Layout.jsx
│   │   ├── pages/          # Páginas React (opcionales)
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Ejercicio.jsx
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── TerapiaOcupacional.jsx
│   │   └── assets/         # Recursos estáticos
│   │       └── static/
│   │           ├── css/
│   │           └── js/
│   ├── vite.config.js      # Configuración de Vite
│   ├── package.json        # Dependencias Node.js
│   └── index.html          # Entry point React (opcional)
├── modules/                  # Módulos legacy
│   └── ejercicios.py       # Implementación Pygame (legacy)
├── data/                     # Datos del sistema
│   ├── pacientes/          # Datos de pacientes
│   │   ├── pacientes.json
│   │   └── historial/
│   └── sessions/           # Sesiones de Flask
│       └── .gitkeep
├── venv/                     # Entorno virtual Python
├── logs/                     # Logs de la aplicación
├── run_backend.py           # Script de ejecución del backend
├── start_project.py         # Script de inicio automático
├── docker-compose.yml       # Orquestación Docker
└── .gitignore              # Archivos ignorados por Git
```

## 🎯 Patrones Arquitectónicos Implementados

### Backend (Flask)
- **Factory Pattern**: Creación de aplicación Flask (`create_app()`)
- **MVC Pattern**: Separación de Modelos, Vistas y Controladores
- **Repository Pattern**: Acceso a datos mediante repositorios
- **Service Layer Pattern**: Lógica de negocio en servicios
- **Blueprint Pattern**: Organización de rutas en blueprints
- **Configuration Pattern**: Gestión de configuraciones por entorno

### Frontend
- **Template Pattern**: Templates Jinja2 servidos por Flask
- **Component Pattern**: Componentes React reutilizables (opcionales)
- **Static Assets Pattern**: Recursos estáticos organizados

## 🚀 Tecnologías Utilizadas

### Backend
- **Python 3.8+**: Lenguaje principal
- **Flask 2.3+**: Framework web
- **Flask-CORS**: Manejo de CORS
- **Flask-Session**: Gestión de sesiones (almacenadas en `data/sessions/`)
- **Marshmallow**: Serialización y validación de datos
- **mysql-connector-python**: Conexión a MySQL
- **python-dotenv**: Gestión de variables de entorno
- **Pytest**: Testing automatizado
- **Black**: Formateo de código Python
- **Flake8**: Linting de código Python

### Frontend
- **Jinja2**: Motor de templates (servido por Flask)
- **Bootstrap 5**: Framework CSS
- **JavaScript (Vanilla)**: Lógica del frontend
- **HTML5 Canvas**: Renderizado de juegos de rehabilitación
- **React 18** (opcional): Componentes React para futuras mejoras
- **Vite**: Build tool para desarrollo React
- **Chart.js**: Gráficos y visualizaciones
- **Axios**: Cliente HTTP para llamadas API

### Módulos Legacy
- **Pygame**: Implementación legacy de ejercicios (`modules/ejercicios.py`)

## 📦 Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- Node.js 16+ y npm (opcional, para desarrollo React)
- MySQL (opcional, para base de datos)

### Opción 1: Ejecución Automática (Recomendada)

El script `start_project.py` automatiza todo el proceso:

```bash
# Windows
py start_project.py

# Linux/Mac
python3 start_project.py
```

Este script:
- ✅ Detecta/crea el entorno virtual (`venv/`)
- ✅ Instala dependencias del backend automáticamente
- ✅ Configura variables de entorno
- ✅ Inicia el servidor Flask en `http://localhost:5000`

### Opción 2: Ejecución Manual del Backend

```bash
# Usar el script de ejecución (recomendado)
py run_backend.py

# O ejecutar directamente
cd backend
py run.py
```

El backend se ejecutará en `http://localhost:5000` y servirá:
- Templates HTML desde `frontend/src/templates/`
- Archivos estáticos desde `frontend/src/assets/static/`
- API REST en `/api/auth/` y `/api/ejercicios/`

### Opción 3: Desarrollo con React (Opcional)

Si quieres usar los componentes React:

```bash
cd frontend
npm install
npm run dev
```

Esto iniciará Vite en `http://localhost:5000` (proxy a backend en puerto 5001).

### Opción 4: Docker Compose

```bash
docker-compose up --build
```

## 🔧 Configuración

### Variables de Entorno

El proyecto usa variables de entorno con valores por defecto. Puedes crear un archivo `.env` en la raíz:

#### Backend (.env)
```env
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=tu_clave_secreta_aqui
DATA_PATH=data/pacientes
HISTORIAL_PATH=data/pacientes/historial

# MySQL (opcional)
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=tu_password
MYSQL_DATABASE=rehabilitacion_virtual
```

### Estructura de Datos

Los datos se almacenan en:
- `data/pacientes/pacientes.json`: Información de pacientes
- `data/pacientes/historial/`: Historial de ejercicios por paciente
- `data/sessions/`: Sesiones de Flask (generadas automáticamente)

## 📊 Características

### 🔐 Autenticación y Autorización
- Registro de pacientes con validación
- Inicio de sesión seguro con sesiones Flask
- Gestión de sesiones en `data/sessions/`
- Protección de rutas con decoradores

### 🎮 Ejercicios de Rehabilitación Motora
- **Nivel 1**: Objetivo estático - Ejercicio básico de precisión
- **Nivel 2**: Objetivo en movimiento lento - Mejora de coordinación
- **Nivel 3**: Objetivo en movimiento rápido - Desafío avanzado
- **Métricas avanzadas**: Precisión, velocidad promedio, rango de movimiento, tiempo de reacción, consistencia, combo máximo

### 🏥 Terapia Ocupacional
- Ejercicios funcionales específicos
- Actividades de la vida diaria
- Seguimiento de progreso personalizado

### 📈 Seguimiento y Análisis
- Historial personalizado por paciente
- Estadísticas en tiempo real durante ejercicios
- Métricas médicas avanzadas
- Almacenamiento en JSON estructurado

### 🎨 Interfaz Moderna
- Diseño responsive con Bootstrap 5
- Animaciones fluidas en los juegos
- UX optimizada para pacientes
- Accesibilidad mejorada

## 🛠️ Desarrollo

### Estructura de Código
- **Type Hints**: Tipado estático en Python
- **ESLint/Prettier**: Formateo de código JavaScript
- **Black**: Formateo de código Python
- **Flake8**: Linting de código Python
- **Pytest**: Testing automatizado

### Comandos de Desarrollo

#### Backend
```bash
# Activar entorno virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Formatear código
black backend/

# Ejecutar tests
pytest backend/tests/

# Linting
flake8 backend/
```

#### Frontend
```bash
cd frontend

# Formatear código
npm run format

# Linting
npm run lint

# Build de producción (React)
npm run build
```

### Estructura de Archivos Importantes

- `backend/app/__init__.py`: Factory de la aplicación Flask
- `backend/app/routes.py`: Definición de rutas y blueprints
- `backend/config/settings.py`: Configuración por entorno
- `frontend/src/templates/`: Templates Jinja2 servidos por Flask
- `frontend/src/assets/static/js/main.js`: JavaScript principal
- `run_backend.py`: Script de ejecución con manejo de venv
- `start_project.py`: Script de inicio completo

## 📚 Documentación

- **[Guía de Despliegue](./GUIA_DEPLOY.md)** - Guía completa con pasos para capturas (Scrum)

## 🔒 Seguridad

- Validación de datos en frontend y backend
- Sanitización de inputs
- Gestión segura de sesiones
- Headers de seguridad configurados
- Logging de auditoría en `logs/`

## 📈 Monitoreo y Logging

- Logs estructurados en `logs/rehavr.log`
- Rotación automática de logs
- Manejo de errores centralizado
- Health checks disponibles

## 🚀 Despliegue

### Producción

```bash
# Backend con Gunicorn
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 backend.run:app

# O usando el script
FLASK_ENV=production py run_backend.py
```

### Docker

```bash
docker-compose up -d
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Equipo

- **Desarrollador Principal**: [Tu Nombre]
- **Mentor**: [Nombre del Mentor]
- **Instituciones**: [Universidad/Institución]

## 📞 Contacto

- **Email**: [tu-email@ejemplo.com]
- **Proyecto**: [https://github.com/SergIOSanchez99/TESIS2-VR-Final]

---

**RehaVR** - Transformando la rehabilitación motora con tecnología de vanguardia 🦾✨
