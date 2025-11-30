# Script para configurar Python 3.11 en el proyecto
# Ejecutar en PowerShell: .\configurar_python311.ps1

Write-Host "🐍 Configurando Python 3.11 para RehaVR" -ForegroundColor Cyan
Write-Host "=" * 50

# Verificar si Python 3.11 está instalado
Write-Host "`n📋 Verificando Python 3.11..." -ForegroundColor Yellow
$version = py -3.11 --version 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ $version encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ Python 3.11 no está instalado" -ForegroundColor Red
    Write-Host "`n📥 Para instalar Python 3.11:" -ForegroundColor Yellow
    Write-Host "   1. Descarga desde: https://www.python.org/downloads/release/python-3119/" -ForegroundColor White
    Write-Host "   2. O usa winget: winget install Python.Python.3.11" -ForegroundColor White
    exit 1
}

# Crear o recrear entorno virtual
if (Test-Path ".venv") {
    Write-Host "`n⚠️  El entorno virtual ya existe. ¿Eliminarlo y recrearlo? (S/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "S" -or $response -eq "s") {
        Remove-Item -Recurse -Force .venv
        Write-Host "✅ Entorno virtual anterior eliminado" -ForegroundColor Green
    } else {
        Write-Host "⏭️  Usando entorno virtual existente" -ForegroundColor Yellow
        $recreate = $false
    }
} else {
    $recreate = $true
}

if ($recreate) {
    # Crear entorno virtual con Python 3.11
    Write-Host "`n🔧 Creando entorno virtual con Python 3.11..." -ForegroundColor Yellow
    py -3.11 -m venv .venv
    
    if (Test-Path ".venv\Scripts\python.exe") {
        Write-Host "✅ Entorno virtual creado exitosamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Error al crear el entorno virtual" -ForegroundColor Red
        exit 1
    }
}

# Activar entorno virtual
Write-Host "`n🔄 Activando entorno virtual..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1

# Verificar versión
$venvVersion = python --version
Write-Host "✅ Versión de Python en entorno virtual: $venvVersion" -ForegroundColor Green

# Actualizar pip
Write-Host "`n📦 Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Instalar dependencias
Write-Host "`n📦 Instalando dependencias..." -ForegroundColor Yellow
if (Test-Path "backend\requirements.txt") {
    pip install -r backend\requirements.txt
    Write-Host "✅ Dependencias instaladas desde backend\requirements.txt" -ForegroundColor Green
} elseif (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "✅ Dependencias instaladas desde requirements.txt" -ForegroundColor Green
} else {
    Write-Host "⚠️  No se encontró archivo requirements.txt" -ForegroundColor Yellow
}

Write-Host "`n✅ Configuración completada!" -ForegroundColor Green
Write-Host "`n📝 Para activar el entorno virtual en el futuro:" -ForegroundColor Cyan
Write-Host "   .venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "`n📝 Para seleccionar el intérprete en VS Code/Cursor:" -ForegroundColor Cyan
Write-Host "   Ctrl+Shift+P -> 'Python: Select Interpreter' -> Selecciona .venv\Scripts\python.exe" -ForegroundColor White

