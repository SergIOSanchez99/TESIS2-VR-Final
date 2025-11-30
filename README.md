# 🦾 RehaVR - Sistema de Rehabilitación Motora

Sistema profesional de rehabilitación motora con arquitectura moderna, patrones de diseño y buenas prácticas de desarrollo.

## 🏗️ Arquitectura del Proyecto

```
RehaVR/
├── backend/                    # Backend API (Flask)
│   ├── app/
│   │   ├── controllers/       # Controladores MVC
│   │   ├── models/           # Modelos de datos
│   │   ├── services/         # Lógica de negocio
│   │   ├── utils/            # Utilidades
│   │   └── routes.py         # Definición de rutas
│   ├── config/               # Configuración
│   ├── tests/                # Pruebas unitarias
│   └── run.py               # Entry point
├── frontend/                  # Frontend (React + Vite)
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   ├── pages/           # Páginas
│   │   ├── utils/           # Utilidades
│   │   └── assets/          # Recursos estáticos
│   ├── public/              # Archivos públicos
│   └── package.json         # Dependencias
├── data/                     # Datos del sistema
└── docker-compose.yml       # Orquestación
```

## 🎯 Patrones Arquitectónicos Implementados

### Backend (Flask)
- **Factory Pattern**: Creación de aplicación Flask
- **MVC Pattern**: Separación de Modelos, Vistas y Controladores
- **Repository Pattern**: Acceso a datos
- **Service Layer Pattern**: Lógica de negocio
- **Blueprint Pattern**: Organización de rutas
- **Configuration Pattern**: Gestión de configuraciones

### Frontend (React)
- **Component Pattern**: Componentes reutilizables
- **Hooks Pattern**: Gestión de estado
- **Container/Presentational Pattern**: Separación de lógica y presentación
- **Custom Hooks Pattern**: Lógica reutilizable

## 🚀 Tecnologías Utilizadas

### Backend
- **Python 3.8+**: Lenguaje principal
- **Flask 2.3**: Framework web
- **Flask-CORS**: Manejo de CORS
- **Flask-Session**: Gestión de sesiones
- **Marshmallow**: Serialización y validación
- **Pytest**: Testing

### Frontend
- **React 18**: Framework de UI
- **Vite**: Build tool
- **React Router**: Navegación
- **Axios**: Cliente HTTP
- **Chart.js**: Gráficos
- **Bootstrap 5**: Framework CSS
- **Framer Motion**: Animaciones

## 📦 Instalación y Ejecución

### Opción 1: Ejecución Automática (Recomendada)
```bash
python start_project.py
```

### Opción 2: Ejecución Manual

#### Backend
```bash
cd backend
pip install -r requirements.txt
python run.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Opción 3: Docker Compose
```bash
docker-compose up --build
```

**📖 Para más detalles, consulta:** [EJECUTAR_PROYECTO.md](./EJECUTAR_PROYECTO.md)

## 🔧 Configuración

### Variables de Entorno

#### Backend (.env)
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu_clave_secreta
DATA_PATH=data/pacientes
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000
```

## 📊 Características

### 🔐 Autenticación y Autorización
- Registro de pacientes
- Inicio de sesión seguro
- Gestión de sesiones
- Protección de rutas

### 🎮 Ejercicios de Rehabilitación
- **Nivel 1**: Objetivo estático
- **Nivel 2**: Objetivo en movimiento lento
- **Nivel 3**: Objetivo en movimiento rápido
- **Terapia Ocupacional**: Ejercicios específicos

### 📈 Seguimiento y Análisis
- Historial personalizado
- Estadísticas en tiempo real
- Gráficos de progreso
- Recomendaciones inteligentes

### 🎨 Interfaz Moderna
- Diseño responsive
- Animaciones fluidas
- UX optimizada
- Accesibilidad

## 🛠️ Desarrollo

### Estructura de Código
- **Type Hints**: Tipado estático en Python
- **ESLint/Prettier**: Formateo de código JavaScript
- **Black**: Formateo de código Python
- **Pytest**: Testing automatizado

### Comandos de Desarrollo

#### Backend
```bash
# Formatear código
black backend/

# Ejecutar tests
pytest backend/tests/

# Linting
flake8 backend/
```

#### Frontend
```bash
# Formatear código
npm run format

# Linting
npm run lint

# Build de producción
npm run build
```

## 📚 Documentación

- **[Guía de Despliegue](./GUIA_DEPLOY.md)** - Guía completa con pasos para capturas (Scrum)
- **[Arquitectura](./ARQUITECTURA.md)** - Arquitectura del sistema
- **[Diagramas UML](./INSTRUCCIONES_DIAGRAMAS_UML.md)** - Instrucciones para generar diagramas

## 🔒 Seguridad

- Validación de datos en frontend y backend
- Sanitización de inputs
- Protección CSRF
- Headers de seguridad
- Logging de auditoría

## 📈 Monitoreo y Logging

- Logs estructurados
- Métricas de rendimiento
- Manejo de errores centralizado
- Health checks

## 🚀 Despliegue

### Producción
```bash
# Backend
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 backend.run:app

# Frontend
npm run build
serve -s dist -l 3000
```

### Docker
```bash
docker-compose -f docker-compose.prod.yml up -d
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
- **Proyecto**: [https://github.com/tu-usuario/rehavr]

---

**RehaVR** - Transformando la rehabilitación motora con tecnología de vanguardia 🦾✨
