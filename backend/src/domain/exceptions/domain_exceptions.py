"""
Excepciones del Dominio
========================
Excepciones que representan violaciones de reglas de negocio
"""


class DomainException(Exception):
    """Excepción base para todas las excepciones del dominio"""
    pass


# Excepciones de Paciente
class InvalidPacienteDataException(DomainException):
    """Se lanza cuando los datos del paciente son inválidos"""
    pass


class PacienteNotFoundException(DomainException):
    """Se lanza cuando no se encuentra un paciente"""
    pass


class PacienteInactivoException(DomainException):
    """Se lanza cuando se intenta operar con un paciente inactivo"""
    pass


# Excepciones de Email
class InvalidEmailException(DomainException):
    """Se lanza cuando el formato del email es inválido"""
    pass


class EmailDuplicadoException(DomainException):
    """Se lanza cuando se intenta registrar un email ya existente"""
    pass


# Excepciones de Edad
class InvalidEdadException(DomainException):
    """Se lanza cuando la edad está fuera del rango válido"""
    pass


# Excepciones de Ejercicio
class InvalidEjercicioDataException(DomainException):
    """Se lanza cuando los datos del ejercicio son inválidos"""
    pass


class EjercicioNotFoundException(DomainException):
    """Se lanza cuando no se encuentra un ejercicio"""
    pass


class EjercicioInactivoException(DomainException):
    """Se lanza cuando se intenta ejecutar un ejercicio inactivo"""
    pass


# Excepciones de Sesión
class InvalidSesionStateException(DomainException):
    """Se lanza cuando se intenta una operación inválida en el estado actual de la sesión"""
    pass


class SesionNotFoundException(DomainException):
    """Se lanza cuando no se encuentra una sesión"""
    pass


class SesionYaFinalizadaException(DomainException):
    """Se lanza cuando se intenta operar con una sesión ya finalizada"""
    pass


class LimitesSeguridadExcedidosException(DomainException):
    """Se lanza cuando se exceden los límites de seguridad en una sesión"""
    pass


# Excepciones de Autenticación
class CredencialesInvalidasException(DomainException):
    """Se lanza cuando las credenciales de autenticación son inválidas"""
    pass


class UsuarioNoAutenticadoException(DomainException):
    """Se lanza cuando se requiere autenticación"""
    pass


# Excepciones de Autorización
class UsuarioNoAutorizadoException(DomainException):
    """Se lanza cuando el usuario no tiene permisos para una operación"""
    pass


# Excepciones de Gamificación
class LogroYaOtorgadoException(DomainException):
    """Se lanza cuando se intenta otorgar un logro ya obtenido"""
    pass


class PuntosInsuficientesException(DomainException):
    """Se lanza cuando no hay suficientes puntos para una operación"""
    pass


# Excepciones de Configuración
class ConfiguracionInvalidaException(DomainException):
    """Se lanza cuando la configuración es inválida"""
    pass


class LimitesFisiologicosExcedidosException(DomainException):
    """Se lanza cuando los valores exceden límites fisiológicos"""
    pass

