"""
PostgreSQL Paciente Repository
===============================
Implementación concreta del repositorio de pacientes para PostgreSQL
"""
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

from ....domain.entities.paciente import Paciente
from ....domain.value_objects.email import Email
from ....domain.value_objects.edad import Edad
from ....domain.repositories.paciente_repository import IPacienteRepository


class PostgreSQLPacienteRepository(IPacienteRepository):
    """
    Implementación del repositorio de pacientes usando PostgreSQL
    
    Ejemplo de Adapter Pattern:
    - Implementa la interface IPacienteRepository (del dominio)
    - Adapta las llamadas a PostgreSQL
    - Convierte entre entidades del dominio y registros de BD
    """
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
    
    def _get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return psycopg2.connect(self.connection_string, cursor_factory=RealDictCursor)
    
    def _to_entity(self, row: dict) -> Paciente:
        """Convierte un registro de BD a entidad del dominio"""
        return Paciente(
            id=row['id'],
            nombre=row['nombre'],
            email=Email(row['email']),
            edad=Edad(row['edad']),
            fecha_registro=row['fecha_registro'],
            activo=row['activo'],
            notas=row.get('notas')
        )
    
    def guardar(self, paciente: Paciente) -> Paciente:
        """Guarda o actualiza un paciente en PostgreSQL"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                # Verificar si existe
                cur.execute(
                    "SELECT id FROM pacientes WHERE id = %s",
                    (paciente.id,)
                )
                existe = cur.fetchone() is not None
                
                if existe:
                    # UPDATE
                    cur.execute("""
                        UPDATE pacientes 
                        SET nombre = %s, edad = %s, activo = %s, notas = %s
                        WHERE id = %s
                    """, (
                        paciente.nombre,
                        paciente.edad.valor,
                        paciente.activo,
                        paciente.notas,
                        paciente.id
                    ))
                else:
                    # INSERT
                    cur.execute("""
                        INSERT INTO pacientes (id, nombre, email, edad, activo, notas)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        paciente.id,
                        paciente.nombre,
                        paciente.email.valor,
                        paciente.edad.valor,
                        paciente.activo,
                        paciente.notas
                    ))
                
                conn.commit()
                return paciente
        finally:
            conn.close()
    
    def obtener_por_id(self, paciente_id: str) -> Optional[Paciente]:
        """Obtiene un paciente por ID"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM pacientes WHERE id = %s",
                    (paciente_id,)
                )
                row = cur.fetchone()
                return self._to_entity(row) if row else None
        finally:
            conn.close()
    
    def obtener_por_email(self, email: Email) -> Optional[Paciente]:
        """Obtiene un paciente por email"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM pacientes WHERE email = %s",
                    (email.valor,)
                )
                row = cur.fetchone()
                return self._to_entity(row) if row else None
        finally:
            conn.close()
    
    def obtener_todos(self) -> List[Paciente]:
        """Obtiene todos los pacientes"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM pacientes ORDER BY nombre")
                rows = cur.fetchall()
                return [self._to_entity(row) for row in rows]
        finally:
            conn.close()
    
    def obtener_activos(self) -> List[Paciente]:
        """Obtiene solo pacientes activos"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM pacientes WHERE activo = TRUE ORDER BY nombre"
                )
                rows = cur.fetchall()
                return [self._to_entity(row) for row in rows]
        finally:
            conn.close()
    
    def existe_email(self, email: Email) -> bool:
        """Verifica si existe un paciente con ese email"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(*) as count FROM pacientes WHERE email = %s",
                    (email.valor,)
                )
                result = cur.fetchone()
                return result['count'] > 0
        finally:
            conn.close()
    
    def eliminar(self, paciente_id: str) -> bool:
        """Elimina (desactiva) un paciente"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE pacientes SET activo = FALSE WHERE id = %s",
                    (paciente_id,)
                )
                conn.commit()
                return cur.rowcount > 0
        finally:
            conn.close()
    
    def contar_total(self) -> int:
        """Cuenta el total de pacientes"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) as count FROM pacientes")
                result = cur.fetchone()
                return result['count']
        finally:
            conn.close()

