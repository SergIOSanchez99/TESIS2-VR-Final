# Estructura del Proyecto RehaVR

## 📁 Organización de Carpetas

```
TESIS II- Proyecto/
├── 📄 app.py                    # Servidor Flask principal
├── 📄 main.py                   # Aplicación desktop (Tkinter)
├── 📄 requirements.txt          # Dependencias Python
├── 📄 README.md                # Documentación principal
├── 📄 ESTRUCTURA_PROYECTO.md   # Este archivo
│
├── 📁 static/                  # Archivos estáticos (CSS, JS, imágenes)
│   ├── 📁 css/
│   │   └── 📄 style.css        # Estilos personalizados
│   ├── 📁 js/
│   │   └── 📄 main.js          # JavaScript personalizado
│   └── 📁 images/
│       └── 📄 README.md        # Guía para imágenes
│
├── 📁 templates/               # Plantillas HTML
│   ├── 📄 base.html           # Plantilla base
│   ├── 📄 index.html          # Página principal
│   ├── 📄 registro.html       # Formulario de registro
│   ├── 📄 login.html          # Formulario de login
│   ├── 📄 dashboard.html      # Panel principal
│   ├── 📄 ejercicio.html      # Ejercicios interactivos
│   └── 📄 terapia_ocupacional.html # Terapia ocupacional
│
├── 📁 modules/                # Módulos Python
│   ├── 📄 usuarios.py         # Gestión de usuarios
│   └── 📄 ejercicios.py       # Lógica de ejercicios
│
└── 📁 data/                   # Datos del sistema
    └── 📁 pacientes/
        ├── 📄 pacientes.json   # Registro de pacientes
        └── 📁 historial/       # Historial individual
```

## 🎨 Archivos de Estilo y Scripts

### CSS Personalizado (`static/css/style.css`)
- **Variables CSS** para colores consistentes
- **Estilos responsivos** para móviles y tablets
- **Animaciones** y transiciones suaves
- **Estilos específicos** para ejercicios y terapia
- **Modo oscuro/claro** (preparado)
- **Accesibilidad** mejorada

### JavaScript Personalizado (`static/js/main.js`)
- **Inicialización** de componentes Bootstrap
- **Sistema de notificaciones** en tiempo real
- **Animaciones** de entrada y salida
- **Gestión de formularios** mejorada
- **Preferencias del usuario** (tema, tamaño de fuente)
- **Funciones de accesibilidad**
- **Temporizador de sesión**
- **Exportación de datos**

## 🖼️ Gestión de Imágenes (`static/images/`)

### Organización recomendada:
```
static/images/
├── 📁 icons/          # Iconos del sistema
├── 📁 exercises/      # Imágenes de ejercicios
├── 📁 therapy/        # Imágenes de terapia ocupacional
├── 📁 ui/             # Elementos de interfaz
├── 📁 backgrounds/    # Fondos y texturas
└── 📁 avatars/        # Avatares de usuarios
```

## 🔧 Configuración de Bootstrap

### CDN Incluido:
- **Bootstrap 5.3.0** - Framework CSS principal
- **Font Awesome 6.0.0** - Iconos
- **JavaScript personalizado** - Funcionalidades adicionales

### Características implementadas:
- ✅ **Navbar responsivo** con navegación dinámica
- ✅ **Cards con hover effects** y animaciones
- ✅ **Formularios estilizados** con validación
- ✅ **Botones personalizados** con efectos
- ✅ **Alertas y notificaciones** mejoradas
- ✅ **Progress bars** y indicadores
- ✅ **Modales** y popovers

## 📱 Responsive Design

### Breakpoints implementados:
- **Mobile First** - Diseño optimizado para móviles
- **Tablet** - Adaptación para tablets
- **Desktop** - Experiencia completa en PC

### Características responsive:
- ✅ **Navegación colapsable** en móviles
- ✅ **Botones de ancho completo** en pantallas pequeñas
- ✅ **Cards apiladas** en dispositivos móviles
- ✅ **Canvas adaptativo** para ejercicios
- ✅ **Formularios optimizados** para touch

## 🎯 Funcionalidades Implementadas

### Sistema de Usuarios:
- ✅ **Registro** con validación
- ✅ **Login** con sesiones
- ✅ **Dashboard** personalizado
- ✅ **Logout** seguro

### Ejercicios Interactivos:
- ✅ **3 niveles de dificultad**
- ✅ **Canvas HTML5** para juegos
- ✅ **Puntuación** en tiempo real
- ✅ **Historial** de actividades

### Terapia Ocupacional:
- ✅ **Abotonar camisa** interactivo
- ✅ **Arrastrar y soltar** objetos
- ✅ **Feedback visual** inmediato
- ✅ **Progreso** registrado

## 🚀 Cómo Ejecutar

### 1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### 2. Ejecutar servidor web:
```bash
python app.py
```

### 3. Acceder al sistema:
- **URL:** http://localhost:5000
- **Registro:** http://localhost:5000/registro
- **Login:** http://localhost:5000/login

## 📊 Estructura de Datos

### Archivos JSON:
- `data/pacientes/pacientes.json` - Registro de pacientes
- `data/pacientes/historial/[DNI].json` - Historial individual

### Formato de datos:
```json
{
  "dni": "12345678",
  "nombre": "Juan Pérez",
  "edad": 45,
  "email": "juan@email.com",
  "fecha_registro": "2024-01-15"
}
```

## 🔒 Seguridad

### Implementado:
- ✅ **Validación** de formularios
- ✅ **Sesiones** seguras
- ✅ **Sanitización** de datos
- ✅ **CORS** configurado
- ✅ **Headers** de seguridad

## 📈 Próximas Mejoras

### Funcionalidades planificadas:
- [ ] **Modo oscuro** completo
- [ ] **Exportación** de datos
- [ ] **Gráficos** de progreso
- [ ] **Notificaciones** push
- [ ] **Modo offline** básico
- [ ] **Accesibilidad** avanzada
- [ ] **Multilenguaje** (ES/EN)
- [ ] **Backup automático** de datos

---

**Nota:** Esta estructura está optimizada para desarrollo y producción, con separación clara de responsabilidades y organización modular. 