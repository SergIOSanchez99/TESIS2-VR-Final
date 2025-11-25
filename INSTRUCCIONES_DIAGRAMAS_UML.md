# 📊 Instrucciones para Generar Diagramas UML - RehaVR

## 📁 Archivos de Diagramas UML Creados

1. **`diagrama_uml_academico.puml`** - Diagrama de Clases UML completo
2. **`diagrama_componentes_uml.puml`** - Diagrama de Componentes UML
3. **`diagrama_secuencia_uml.puml`** - Diagrama de Secuencia UML

## 🎯 Diagrama Principal para Trabajo Académico

**Recomendado**: `diagrama_uml_academico.puml`

Este diagrama incluye:
- ✅ Todas las clases del sistema
- ✅ Relaciones entre capas
- ✅ Patrones de diseño identificados
- ✅ Colores diferenciados por capa
- ✅ Notas explicativas
- ✅ Formato académico profesional

## 🚀 Métodos para Generar las Imágenes

### Método 1: PlantUML Online (Más Rápido) ⭐ RECOMENDADO

1. Abre: **http://www.plantuml.com/plantuml/uml/**
2. Abre el archivo `diagrama_uml_academico.puml`
3. Copia todo su contenido
4. Pégalo en el editor de PlantUML Online
5. Haz clic en "Submit" o presiona `Ctrl+Enter`
6. Descarga la imagen:
   - Clic derecho en el diagrama → "Guardar imagen como..."
   - O usa el botón "Download PNG"

**Ventajas**: 
- ✅ No requiere instalación
- ✅ Funciona inmediatamente
- ✅ Alta calidad de imagen
- ✅ Formato PNG o SVG

---

### Método 2: PlantUML Local (Para Trabajos Académicos)

#### Requisitos:
- Java instalado: https://www.java.com/
- PlantUML JAR: http://plantuml.com/download

#### Pasos:

1. Descarga `plantuml.jar` desde http://plantuml.com/download
2. Colócalo en la carpeta del proyecto
3. Ejecuta en la terminal:

```bash
# Diagrama de Clases (Principal)
java -jar plantuml.jar diagrama_uml_academico.puml

# Diagrama de Componentes
java -jar plantuml.jar diagrama_componentes_uml.puml

# Diagrama de Secuencia
java -jar plantuml.jar diagrama_secuencia_uml.puml
```

4. Se generarán archivos PNG:
   - `diagrama_uml_academico.png`
   - `diagrama_componentes_uml.png`
   - `diagrama_secuencia_uml.png`

**Ventajas**: 
- ✅ Formato estándar académico
- ✅ Alta calidad
- ✅ Control total sobre la generación

---

### Método 3: VS Code Extension

1. Instala la extensión: **"PlantUML"** en VS Code
2. Abre `diagrama_uml_academico.puml`
3. Presiona `Alt+D` para previsualizar
4. Clic derecho en el diagrama → "Export Current Diagram" → PNG

**Ventajas**: 
- ✅ Integrado en el editor
- ✅ Vista previa en tiempo real

---

## 📋 Contenido de los Diagramas

### 1. Diagrama de Clases UML (`diagrama_uml_academico.puml`)

**Incluye:**
- Capa de Configuración (Config, DevelopmentConfig, ProductionConfig, TestingConfig)
- Capa de Aplicación (FlaskApp con Factory Pattern)
- Capa de Rutas (MainBlueprint, AuthBlueprint, EjercicioBlueprint)
- Capa de Controladores (AuthController, EjercicioController)
- Capa de Servicios (PacienteService, EjercicioService)
- Capa de Modelos (Paciente, Ejercicio, ResultadoEjercicio)
- Capa de Repositorios (PacienteRepository, EjercicioRepository)
- Capa de Base de Datos (MySQLConnectionManager, MySQLDatabaseManager, etc.)

**Características:**
- Colores diferenciados por capa
- Relaciones claramente definidas
- Notas explicativas de patrones
- Formato académico profesional

### 2. Diagrama de Componentes UML (`diagrama_componentes_uml.puml`)

**Muestra:**
- Componentes del sistema
- Dependencias entre componentes
- Separación Frontend/Backend
- Flujo de datos

### 3. Diagrama de Secuencia UML (`diagrama_secuencia_uml.puml`)

**Ilustra:**
- Flujo de registro de paciente
- Interacción entre capas
- Secuencia de llamadas
- Validaciones y respuestas

## 🎨 Personalización

### Cambiar Colores

Edita las líneas `BackgroundColor` en `diagrama_uml_academico.puml`:

```plantuml
skinparam class {
    BackgroundColor<<Config>> #E3F2FD
    BackgroundColor<<Controller>> #FFF3E0
    ...
}
```

### Cambiar Tamaño

Agrega al inicio del archivo:

```plantuml
scale 1.5
```

### Cambiar Formato de Salida

```bash
# PNG (por defecto)
java -jar plantuml.jar diagrama_uml_academico.puml

# SVG (vectorial, mejor calidad)
java -jar plantuml.jar -tsvg diagrama_uml_academico.puml

# PDF
java -jar plantuml.jar -tpdf diagrama_uml_academico.puml
```

## 📝 Para Trabajos Académicos

### Recomendaciones:

1. **Usa el Diagrama de Clases** como diagrama principal
2. **Incluye el Diagrama de Componentes** para mostrar la arquitectura general
3. **Añade el Diagrama de Secuencia** para explicar un flujo específico
4. **Exporta en alta resolución** (PNG o SVG)
5. **Incluye leyenda** explicando los colores y patrones

### Formato para Documento:

- **Tamaño**: A4 o Letter
- **Resolución**: Mínimo 300 DPI
- **Formato**: PNG o PDF
- **Orientación**: Horizontal (landscape) para diagramas grandes

## 🔧 Solución de Problemas

### Error: "Java no encontrado"
- Instala Java desde: https://www.java.com/
- Verifica con: `java -version`

### Error: "PlantUML no encontrado"
- Descarga el JAR desde: http://plantuml.com/download
- O usa el método online (Método 1)

### El diagrama se ve mal
- Verifica que el archivo no tenga errores de sintaxis
- Usa la versión más reciente de PlantUML
- Prueba con el método online primero

### Diagrama muy grande
- Usa `scale 0.8` para reducir tamaño
- O divide en múltiples diagramas

---

## 📞 Soporte

Si tienes problemas generando los diagramas, prueba primero el **Método 1 (PlantUML Online)** que es el más simple y no requiere instalación.

---

**Generado para**: Sistema de Rehabilitación Virtual (RehaVR)  
**Fecha**: 2024  
**Formato**: Diagramas UML estándar (PlantUML)  
**Uso**: Trabajo académico / Documentación técnica






