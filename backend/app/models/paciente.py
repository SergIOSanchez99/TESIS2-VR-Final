"""
Modelo de Paciente - Patrón de Diseño Model
Responsable de la representación de datos y lógica de negocio de pacientes
"""
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# Agregar el directorio raíz al path para importar configuraciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.database.mysql_manager import MySQLDatabaseService


@dataclass
class Paciente:
    """Clase de datos para representar un paciente"""
    nombre: str
    email: str
    password: str
    edad: str
    id: Optional[str] = None
    fecha_registro: Optional[str] = None
    
    def __post_init__(self):
        if not self.id:
            self.id = f"{self.email.lower().replace('@', '_').replace('.', '_')}"
        if not self.fecha_registro:
            self.fecha_registro = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convierte el paciente a diccionario"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Paciente':
        """Crea un paciente desde un diccionario"""
        return cls(**data)
    
    def to_dict_safe(self) -> Dict:
        """Convierte el paciente a diccionario sin la contraseña"""
        data = self.to_dict()
        data.pop('password', None)
        return data


class PacienteRepository:
    """Repositorio para manejo de datos de pacientes - Patrón Repository con MySQL"""
    
    def __init__(self, data_path: str = "data/pacientes"):
        self.data_path = data_path
        self.pacientes_file = os.path.join(data_path, "pacientes.json")
        self.historial_path = os.path.join(data_path, "historial")
        self._ensure_directories()
        
        # Intentar usar MySQL, si falla usar JSON como fallback
        try:
            self.db_service = MySQLDatabaseService()
            self.use_mysql = True
        except Exception as e:
            print(f"⚠️ No se pudo conectar a MySQL, usando archivos JSON: {e}")
            self.use_mysql = False
            self.db_service = None
    
    def _ensure_directories(self):
        """Asegura que existan los directorios necesarios"""
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.historial_path, exist_ok=True)
    
    def get_all(self) -> List[Paciente]:
        """Obtiene todos los pacientes"""
        if self.use_mysql and self.db_service:
            try:
                pacientes_data = self.db_service.pacientes.obtener_todos_pacientes()
                pacientes = []
                for p_data in pacientes_data:
                    # Convertir datos de MySQL a objeto Paciente
                    paciente = Paciente(
                        nombre=p_data['nombre'],
                        email=p_data['email'],
                        password='',  # No devolver contraseña
                        edad=str(p_data['edad']),
                        id=str(p_data['id']),
                        fecha_registro=p_data['fecha_registro'].isoformat() if hasattr(p_data['fecha_registro'], 'isoformat') else str(p_data['fecha_registro'])
                    )
                    pacientes.append(paciente)
                return pacientes
            except Exception as e:
                print(f"⚠️ Error al obtener pacientes de MySQL: {e}")
                # Fallback a JSON
                return self._get_all_json()
        else:
            return self._get_all_json()
    
    def _get_all_json(self) -> List[Paciente]:
        """Obtiene todos los pacientes desde JSON (fallback)"""
        if not os.path.exists(self.pacientes_file):
            return []
        
        try:
            with open(self.pacientes_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Paciente.from_dict(p) for p in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_all(self, pacientes: List[Paciente]):
        """Guarda todos los pacientes (solo para JSON)"""
        data = [p.to_dict() for p in pacientes]
        with open(self.pacientes_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add(self, paciente: Paciente) -> bool:
        """Agrega un nuevo paciente"""
        if self.use_mysql and self.db_service:
            try:
                # Verificar si el email ya existe
                if self.db_service.pacientes.verificar_email_existe(paciente.email):
                    return False
                
                # Crear paciente en MySQL
                edad_int = int(paciente.edad) if paciente.edad.isdigit() else 0
                paciente_data = self.db_service.pacientes.crear_paciente(
                    nombre=paciente.nombre,
                    email=paciente.email,
                    password=paciente.password,
                    edad=edad_int
                )
                
                # Actualizar el ID del paciente
                paciente.id = str(paciente_data['id'])
                paciente.fecha_registro = paciente_data['fecha_registro']
                return True
            except ValueError as e:
                # Email duplicado
                return False
            except Exception as e:
                print(f"⚠️ Error al agregar paciente en MySQL: {e}")
                # Fallback a JSON
                return self._add_json(paciente)
        else:
            return self._add_json(paciente)
    
    def _add_json(self, paciente: Paciente) -> bool:
        """Agrega un paciente usando JSON (fallback)"""
        pacientes = self._get_all_json()
        
        # Verificar si ya existe el email
        for p in pacientes:
            if p.email.lower() == paciente.email.lower():
                return False
        
        pacientes.append(paciente)
        self.save_all(pacientes)
        return True
    
    def find_by_email(self, email: str) -> Optional[Paciente]:
        """Busca un paciente por email"""
        if self.use_mysql and self.db_service:
            try:
                # No hay método directo, buscar en todos
                pacientes = self.get_all()
                for p in pacientes:
                    if p.email.lower() == email.lower():
                        return p
                return None
            except Exception as e:
                print(f"⚠️ Error al buscar paciente en MySQL: {e}")
                return self._find_by_email_json(email)
        else:
            return self._find_by_email_json(email)
    
    def _find_by_email_json(self, email: str) -> Optional[Paciente]:
        """Busca un paciente por email en JSON (fallback)"""
        pacientes = self._get_all_json()
        for p in pacientes:
            if p.email.lower() == email.lower():
                return p
        return None
    
    def find_by_credentials(self, email: str, password: str) -> Optional[Paciente]:
        """Busca un paciente por email y contraseña"""
        if self.use_mysql and self.db_service:
            try:
                paciente_data = self.db_service.pacientes.autenticar_paciente(email, password)
                if paciente_data:
                    # Convertir datos de MySQL a objeto Paciente
                    paciente = Paciente(
                        nombre=paciente_data['nombre'],
                        email=paciente_data['email'],
                        password=password,  # Guardar temporalmente para validación
                        edad=str(paciente_data['edad']),
                        id=str(paciente_data['id']),
                        fecha_registro=paciente_data['fecha_registro'].isoformat() if hasattr(paciente_data['fecha_registro'], 'isoformat') else str(paciente_data['fecha_registro'])
                    )
                    return paciente
                return None
            except Exception as e:
                print(f"⚠️ Error al autenticar en MySQL: {e}")
                return self._find_by_credentials_json(email, password)
        else:
            return self._find_by_credentials_json(email, password)
    
    def _find_by_credentials_json(self, email: str, password: str) -> Optional[Paciente]:
        """Busca un paciente por email y contraseña en JSON (fallback)"""
        paciente = self._find_by_email_json(email)
        if paciente and paciente.password == password:
            return paciente
        return None
    
    def get_historial_path(self, paciente: Paciente) -> str:
        """Obtiene la ruta del archivo de historial del paciente"""
        filename = f"{paciente.nombre.replace(' ', '_').lower()}_{paciente.edad}.json"
        return os.path.join(self.historial_path, filename)
