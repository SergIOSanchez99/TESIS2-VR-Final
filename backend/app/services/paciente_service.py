"""
Servicio de Pacientes - Patrón de Diseño Service Layer
Responsable de la lógica de negocio relacionada con pacientes
"""
from typing import List, Optional, Dict, Tuple
from ..models.paciente import Paciente, PacienteRepository
from ..models.ejercicio import EjercicioRepository, ResultadoEjercicio


class PacienteService:
    """Servicio para gestión de pacientes - Patrón Service Layer"""
    
    def __init__(self):
        self.paciente_repo = PacienteRepository()
        self.ejercicio_repo = EjercicioRepository()
    
    def registrar_paciente(self, nombre: str, email: str, password: str, edad: str) -> Tuple[bool, str, Optional[Paciente]]:
        """
        Registra un nuevo paciente
        
        Returns:
            Tuple[bool, str, Optional[Paciente]]: (éxito, mensaje, paciente)
        """
        # Validaciones
        if not nombre or not nombre.strip():
            return False, "El nombre es requerido", None
        
        if not email or not email.strip():
            return False, "El correo electrónico es requerido", None
        
        if not self._validar_email(email):
            return False, "El formato del correo electrónico no es válido", None
        
        if not password or not password.strip():
            return False, "La contraseña es requerida", None
        
        if len(password.strip()) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres", None
        
        if not edad or not edad.strip():
            return False, "La edad es requerida", None
        
        try:
            int(edad)
        except ValueError:
            return False, "La edad debe ser un número válido", None
        
        # Crear paciente
        paciente = Paciente(
            nombre=nombre.strip(), 
            email=email.strip().lower(), 
            password=password.strip(),
            edad=edad.strip()
        )
        
        # Intentar agregar
        if self.paciente_repo.add(paciente):
            return True, "Paciente registrado exitosamente", paciente
        else:
            return False, "Ya existe un paciente con ese correo electrónico", None
    
    def autenticar_paciente(self, email: str, password: str) -> Tuple[bool, str, Optional[Paciente]]:
        """
        Autentica un paciente
        
        Returns:
            Tuple[bool, str, Optional[Paciente]]: (éxito, mensaje, paciente)
        """
        if not email or not password:
            return False, "Correo electrónico y contraseña son requeridos", None
        
        paciente = self.paciente_repo.find_by_credentials(email.strip().lower(), password.strip())
        
        if paciente:
            return True, f"Bienvenido/a, {paciente.nombre}!", paciente
        else:
            return False, "Correo electrónico o contraseña incorrectos", None
    
    def obtener_paciente(self, paciente_id: str) -> Optional[Paciente]:
        """Obtiene un paciente por ID"""
        pacientes = self.paciente_repo.get_all()
        for paciente in pacientes:
            if paciente.id == paciente_id:
                return paciente
        return None
    
    def obtener_todos_pacientes(self) -> List[Paciente]:
        """Obtiene todos los pacientes"""
        return self.paciente_repo.get_all()
    
    def obtener_estadisticas_paciente(self, paciente_id: str) -> Dict:
        """Obtiene estadísticas completas del paciente"""
        paciente = self.obtener_paciente(paciente_id)
        if not paciente:
            return {}
        
        # Estadísticas básicas del paciente
        stats = {
            'paciente': paciente.to_dict(),
            'ejercicios': self.ejercicio_repo.obtener_estadisticas(paciente_id),
            'historial_reciente': self._obtener_historial_reciente(paciente_id)
        }
        
        return stats
    
    def _obtener_historial_reciente(self, paciente_id: str, limite: int = 5) -> List[Dict]:
        """Obtiene el historial reciente del paciente"""
        historial = self.ejercicio_repo.obtener_historial(paciente_id)
        historial_ordenado = sorted(historial, key=lambda x: x.fecha, reverse=True)
        return [r.to_dict() for r in historial_ordenado[:limite]]
    
    def registrar_resultado_ejercicio(self, paciente_id: str, ejercicio: str, 
                                    exito: bool, tiempo_ejecucion: Optional[float] = None,
                                    puntuacion: Optional[int] = None,
                                    observaciones: Optional[str] = None) -> ResultadoEjercicio:
        """Registra un resultado de ejercicio para un paciente"""
        return self.ejercicio_repo.registrar_resultado(
            paciente_id, ejercicio, exito, tiempo_ejecucion, puntuacion, observaciones
        )
    
    def obtener_historial_completo(self, paciente_id: str) -> List[ResultadoEjercicio]:
        """Obtiene el historial completo de ejercicios del paciente"""
        return self.ejercicio_repo.obtener_historial(paciente_id)
    
    def _validar_email(self, email: str) -> bool:
        """Valida el formato del email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
