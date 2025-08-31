"""
Modelo de Paciente - Patrón de Diseño Model
Responsable de la representación de datos y lógica de negocio de pacientes
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


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
    """Repositorio para manejo de datos de pacientes - Patrón Repository"""
    
    def __init__(self, data_path: str = "data/pacientes"):
        self.data_path = data_path
        self.pacientes_file = os.path.join(data_path, "pacientes.json")
        self.historial_path = os.path.join(data_path, "historial")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Asegura que existan los directorios necesarios"""
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.historial_path, exist_ok=True)
    
    def get_all(self) -> List[Paciente]:
        """Obtiene todos los pacientes"""
        if not os.path.exists(self.pacientes_file):
            return []
        
        try:
            with open(self.pacientes_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Paciente.from_dict(p) for p in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_all(self, pacientes: List[Paciente]):
        """Guarda todos los pacientes"""
        data = [p.to_dict() for p in pacientes]
        with open(self.pacientes_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add(self, paciente: Paciente) -> bool:
        """Agrega un nuevo paciente"""
        pacientes = self.get_all()
        
        # Verificar si ya existe el email
        for p in pacientes:
            if p.email.lower() == paciente.email.lower():
                return False
        
        pacientes.append(paciente)
        self.save_all(pacientes)
        return True
    
    def find_by_email(self, email: str) -> Optional[Paciente]:
        """Busca un paciente por email"""
        pacientes = self.get_all()
        for p in pacientes:
            if p.email.lower() == email.lower():
                return p
        return None
    
    def find_by_credentials(self, email: str, password: str) -> Optional[Paciente]:
        """Busca un paciente por email y contraseña"""
        paciente = self.find_by_email(email)
        if paciente and paciente.password == password:
            return paciente
        return None
    
    def get_historial_path(self, paciente: Paciente) -> str:
        """Obtiene la ruta del archivo de historial del paciente"""
        filename = f"{paciente.nombre.replace(' ', '_').lower()}_{paciente.edad}.json"
        return os.path.join(self.historial_path, filename)
