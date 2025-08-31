# 🏗️ Arquitectura de RehaVR

## 📋 Resumen Ejecutivo

RehaVR ha sido refactorizado siguiendo patrones arquitectónicos profesionales y buenas prácticas de desarrollo. La nueva arquitectura separa claramente el frontend del backend, implementa patrones de diseño robustos y proporciona una base escalable para futuras mejoras.

## 🎯 Objetivos de la Refactorización

### ✅ Separación de Responsabilidades
- **Backend**: API REST con lógica de negocio
- **Frontend**: Interfaz de usuario moderna y responsiva
- **Datos**: Almacenamiento estructurado y persistente

### ✅ Patrones de Diseño Implementados
- **MVC Pattern**: Separación clara de Modelos, Vistas y Controladores
- **Repository Pattern**: Abstracción del acceso a datos
- **Service Layer Pattern**: Lógica de negocio centralizada
- **Factory Pattern**: Creación de objetos y configuración
- **Blueprint Pattern**: Organización modular de rutas

### ✅ Escalabilidad y Mantenibilidad
- **Código modular**: Componentes reutilizables
- **Configuración centralizada**: Gestión de entornos
- **Testing**: Estructura preparada para pruebas
- **Documentación**: Código autodocumentado

## 🏛️ Arquitectura del Backend

### 📁 Estructura de Directorios
```
backend/
├── app/
│   ├── controllers/          # Controladores MVC
│   │   ├── auth_controller.py
│   │   └── ejercicio_controller.py
│   ├── models/              # Modelos de datos
│   │   ├── paciente.py
│   │   └── ejercicio.py
│   ├── services/            # Lógica de negocio
│   │   ├── paciente_service.py
│   │   └── ejercicio_service.py
│   ├── utils/               # Utilidades
│   ├── routes.py            # Definición de rutas
│   └── __init__.py          # Factory de aplicación
├── config/
│   └── settings.py          # Configuración
├── tests/                   # Pruebas unitarias
└── run.py                   # Entry point
```

### 🔧 Patrones Implementados

#### 1. Factory Pattern (`app/__init__.py`)
```python
def create_app(config_name='development'):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    config = get_config(config_name)
    app.config.from_object(config)
    # ... configuración adicional
    return app
```

#### 2. MVC Pattern
- **Models**: Representación de datos y lógica de persistencia
- **Views**: Plantillas HTML y respuestas JSON
- **Controllers**: Manejo de peticiones HTTP y coordinación

#### 3. Repository Pattern (`models/paciente.py`)
```python
class PacienteRepository:
    """Repositorio para manejo de datos de pacientes"""
    def get_all(self) -> List[Paciente]:
    def add(self, paciente: Paciente) -> bool:
    def find_by_credentials(self, nombre: str, edad: str) -> Optional[Paciente]:
```

#### 4. Service Layer Pattern (`services/paciente_service.py`)
```python
class PacienteService:
    """Servicio para gestión de pacientes"""
    def registrar_paciente(self, nombre: str, edad: str) -> Tuple[bool, str, Optional[Paciente]]:
    def autenticar_paciente(self, nombre: str, edad: str) -> Tuple[bool, str, Optional[Paciente]]:
```

#### 5. Blueprint Pattern (`routes.py`)
```python
# Blueprints organizados por funcionalidad
main_bp = Blueprint('main', __name__)      # Rutas principales
auth_bp = Blueprint('auth', __name__)      # Autenticación
ejercicio_bp = Blueprint('ejercicios', __name__)  # Ejercicios
```

### 🔐 Gestión de Configuración

#### Configuración por Entornos (`config/settings.py`)
```python
class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    SECRET_KEY = os.environ.get('SECRET_KEY')
```

## 🎨 Arquitectura del Frontend

### 📁 Estructura de Directorios
```
frontend/
├── src/
│   ├── components/          # Componentes React
│   ├── pages/              # Páginas principales
│   ├── utils/              # Utilidades y helpers
│   ├── assets/             # Recursos estáticos
│   └── templates/          # Plantillas HTML (legacy)
├── public/                 # Archivos públicos
├── package.json            # Dependencias
└── vite.config.js          # Configuración de Vite
```

### ⚛️ Patrones React Implementados

#### 1. Component Pattern
```javascript
// Componentes reutilizables y modulares
const Button = ({ children, onClick, variant = 'primary' }) => {
  return (
    <button className={`btn btn-${variant}`} onClick={onClick}>
      {children}
    </button>
  );
};
```

#### 2. Custom Hooks Pattern
```javascript
// Lógica reutilizable en hooks personalizados
const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Lógica de autenticación
  return { user, loading, login, logout };
};
```

#### 3. Container/Presentational Pattern
```javascript
// Separación de lógica y presentación
const DashboardContainer = () => {
  const { data, loading } = useQuery('dashboard');
  return <Dashboard data={data} loading={loading} />;
};
```

## 🔄 Flujo de Datos

### 1. Autenticación
```
Frontend → AuthController → PacienteService → PacienteRepository → JSON Files
```

### 2. Ejercicios
```
Frontend → EjercicioController → EjercicioService → EjercicioRepository → JSON Files
```

### 3. API REST
```
GET    /api/auth/paciente          # Obtener paciente actual
POST   /api/auth/login             # Iniciar sesión
GET    /api/ejercicios/            # Obtener ejercicios
POST   /api/ejercicios/resultado   # Registrar resultado
```

## 🛡️ Seguridad y Validación

### Validación de Datos
- **Backend**: Validación en servicios y controladores
- **Frontend**: Validación en formularios y componentes
- **API**: Sanitización de inputs y outputs

### Gestión de Sesiones
```python
# Configuración de sesiones seguras
SESSION_TYPE = 'filesystem'
PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
```

### CORS y Headers
```python
# Configuración de CORS
CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
```

## 📊 Persistencia de Datos

### Estructura de Archivos JSON
```
data/
├── pacientes/
│   ├── pacientes.json           # Lista de pacientes
│   └── historial/
│       ├── paciente1_25.json    # Historial individual
│       └── paciente2_30.json
```

### Modelos de Datos
```python
@dataclass
class Paciente:
    nombre: str
    edad: str
    id: Optional[str] = None
    fecha_registro: Optional[str] = None

@dataclass
class ResultadoEjercicio:
    paciente_id: str
    tipo_ejercicio: str
    nivel: int
    exito: bool
    fecha: str
    tiempo_ejecucion: Optional[float] = None
```

## 🧪 Testing y Calidad

### Estructura de Pruebas
```
backend/tests/
├── test_models/
├── test_services/
├── test_controllers/
└── conftest.py
```

### Herramientas de Calidad
- **Black**: Formateo de código Python
- **Flake8**: Linting de Python
- **ESLint**: Linting de JavaScript
- **Prettier**: Formateo de JavaScript

## 🚀 Despliegue y Configuración

### Variables de Entorno
```bash
# Backend
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=rehavr_secret_key_2024
DATA_PATH=data/pacientes

# Frontend
REACT_APP_API_URL=http://localhost:5000
```

### Docker Compose
```yaml
services:
  backend:
    build: ./backend
    ports: ["5000:5000"]
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
```

## 📈 Métricas y Monitoreo

### Logging Estructurado
```python
# Configuración de logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

### Health Checks
- Endpoints de verificación de estado
- Monitoreo de dependencias
- Métricas de rendimiento

## 🔮 Futuras Mejoras

### Base de Datos
- Migración a PostgreSQL o MongoDB
- ORM con SQLAlchemy o similar
- Migraciones automáticas

### Autenticación Avanzada
- JWT tokens
- OAuth 2.0
- Autenticación multifactor

### Realidad Virtual
- Integración con hardware VR
- WebXR para ejercicios inmersivos
- Tracking de movimientos

### Machine Learning
- Análisis de patrones de movimiento
- Recomendaciones personalizadas
- Predicción de progreso

## 📚 Documentación Adicional

- [API Documentation](./API.md)
- [Development Guide](./DEVELOPMENT.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Testing Guide](./TESTING.md)

---

**RehaVR** - Arquitectura profesional para el futuro de la rehabilitación motora 🦾✨
