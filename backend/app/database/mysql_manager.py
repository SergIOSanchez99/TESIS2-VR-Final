#!/usr/bin/env python3
"""
Gestor de Base de Datos MySQL - Sistema de Rehabilitación Virtual
Autor: Sistema de Rehabilitación Virtual
Fecha: 2024
"""

import mysql.connector
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
import hashlib
import json
import uuid
from contextlib import contextmanager
from mysql.connector import pooling
import logging

# Agregar el directorio raíz al path para importar configuraciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import get_mysql_config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MySQLConnectionManager:
    """Gestor de conexiones MySQL con pool de conexiones"""
    
    def __init__(self):
        self.config = get_mysql_config()
        self.connection_pool = None
        self._create_connection_pool()
    
    def _create_connection_pool(self):
        """Crea el pool de conexiones"""
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="rehabilitacion_pool",
                pool_size=self.config.get('pool_size', 5),
                pool_reset_session=True,
                **{k: v for k, v in self.config.items() if k not in ['pool_size', 'pool_recycle']}
            )
            logger.info("✅ Pool de conexiones MySQL creado exitosamente")
        except Exception as e:
            logger.error(f"❌ Error al crear pool de conexiones: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Obtiene una conexión del pool"""
        connection = None
        try:
            connection = self.connection_pool.get_connection()
            yield connection
        except Exception as e:
            logger.error(f"❌ Error en conexión MySQL: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()


class MySQLDatabaseManager:
    """Gestor principal de la base de datos MySQL"""
    
    def __init__(self):
        self.connection_manager = MySQLConnectionManager()
        self._ensure_database_exists()
        self._create_tables()
    
    def _ensure_database_exists(self):
        """Asegura que la base de datos existe"""
        config = get_mysql_config()
        try:
            # Conectar sin especificar base de datos
            connection = mysql.connector.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password']
            )
            cursor = connection.cursor()
            
            # Crear base de datos si no existe
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{config['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            logger.info(f"✅ Base de datos '{config['database']}' verificada/creada")
            
            cursor.close()
            connection.close()
        except Exception as e:
            logger.error(f"❌ Error al verificar base de datos: {e}")
            raise
    
    def _create_tables(self):
        """Crea las tablas necesarias"""
        tables_sql = {
            'pacientes': """
                CREATE TABLE IF NOT EXISTS `pacientes` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                    `uuid` varchar(36) NOT NULL,
                    `nombre` varchar(100) NOT NULL,
                    `email` varchar(100) NOT NULL UNIQUE,
                    `password_hash` varchar(255) NOT NULL,
                    `edad` int(3) NOT NULL,
                    `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP,
                    `fecha_actualizacion` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    `activo` tinyint(1) DEFAULT 1,
                    `notas` text,
                    PRIMARY KEY (`id`),
                    UNIQUE KEY `uk_uuid` (`uuid`),
                    UNIQUE KEY `uk_email` (`email`),
                    KEY `idx_activo` (`activo`),
                    KEY `idx_fecha_registro` (`fecha_registro`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            'historial_ejercicios': """
                CREATE TABLE IF NOT EXISTS `historial_ejercicios` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                    `paciente_id` int(11) NOT NULL,
                    `nivel_ejercicio` varchar(50) NOT NULL,
                    `exito` tinyint(1) NOT NULL DEFAULT 0,
                    `fecha_ejercicio` datetime DEFAULT CURRENT_TIMESTAMP,
                    `duracion_segundos` int(11) DEFAULT 0,
                    `puntuacion` int(11) DEFAULT 0,
                    `observaciones` text,
                    PRIMARY KEY (`id`),
                    KEY `fk_historial_paciente` (`paciente_id`),
                    KEY `idx_fecha_ejercicio` (`fecha_ejercicio`),
                    CONSTRAINT `fk_historial_paciente` FOREIGN KEY (`paciente_id`) REFERENCES `pacientes` (`id`) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            'sesiones_terapia': """
                CREATE TABLE IF NOT EXISTS `sesiones_terapia` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                    `paciente_id` int(11) NOT NULL,
                    `fecha_sesion` datetime DEFAULT CURRENT_TIMESTAMP,
                    `duracion_minutos` int(11) DEFAULT 0,
                    `tipo_terapia` varchar(50) NOT NULL,
                    `observaciones` text,
                    PRIMARY KEY (`id`),
                    KEY `fk_sesiones_paciente` (`paciente_id`),
                    KEY `idx_fecha_sesion` (`fecha_sesion`),
                    CONSTRAINT `fk_sesiones_paciente` FOREIGN KEY (`paciente_id`) REFERENCES `pacientes` (`id`) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        }
        
        try:
            with self.connection_manager.get_connection() as connection:
                cursor = connection.cursor()
                
                for table_name, sql in tables_sql.items():
                    cursor.execute(sql)
                    logger.info(f"✅ Tabla '{table_name}' verificada/creada")
                
                connection.commit()
                cursor.close()
        except Exception as e:
            logger.error(f"❌ Error al crear tablas: {e}")
            raise
    
    def _hash_password(self, password: str) -> str:
        """Genera hash de contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_uuid(self) -> str:
        """Genera un UUID único"""
        return str(uuid.uuid4())


class PacienteManager(MySQLDatabaseManager):
    """Gestor específico para pacientes"""
    
    def crear_paciente(self, nombre: str, email: str, password: str, edad: int, notas: str = None) -> Dict[str, Any]:
        """Crea un nuevo paciente"""
        try:
            with self.connection_manager.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                
                paciente_uuid = self._generate_uuid()
                password_hash = self._hash_password(password)
                
                sql = """
                    INSERT INTO pacientes (uuid, nombre, email, password_hash, edad, notas)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (paciente_uuid, nombre, email, password_hash, edad, notas)
                
                cursor.execute(sql, values)
                paciente_id = cursor.lastrowid
                
                connection.commit()
                cursor.close()
                
                logger.info(f"✅ Paciente '{nombre}' creado con ID: {paciente_id}")
                
                return {
                    'id': paciente_id,
                    'uuid': paciente_uuid,
                    'nombre': nombre,
                    'email': email,
                    'edad': edad,
                    'fecha_registro': datetime.now().isoformat()
                }
        except mysql.connector.IntegrityError as e:
            if "Duplicate entry" in str(e):
                raise ValueError("El email ya está registrado")
            raise
        except Exception as e:
            logger.error(f"❌ Error al crear paciente: {e}")
            raise
    
    def autenticar_paciente(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Autentica un paciente"""
        try:
            with self.connection_manager.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                
                password_hash = self._hash_password(password)
                
                sql = """
                    SELECT id, uuid, nombre, email, edad, fecha_registro, activo
                    FROM pacientes 
                    WHERE email = %s AND password_hash = %s AND activo = 1
                """
                cursor.execute(sql, (email, password_hash))
                
                paciente = cursor.fetchone()
                cursor.close()
                
                if paciente:
                    logger.info(f"✅ Paciente '{email}' autenticado correctamente")
                    return paciente
                else:
                    logger.warning(f"⚠️ Intento de autenticación fallido para '{email}'")
                    return None
        except Exception as e:
            logger.error(f"❌ Error al autenticar paciente: {e}")
            raise
    
    def obtener_paciente_por_id(self, paciente_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un paciente por ID"""
        try:
            with self.connection_manager.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                
                sql = "SELECT * FROM pacientes WHERE id = %s AND activo = 1"
                cursor.execute(sql, (paciente_id,))
                
                paciente = cursor.fetchone()
                cursor.close()
                
                return paciente
        except Exception as e:
            logger.error(f"❌ Error al obtener paciente: {e}")
            raise
    
    def obtener_todos_pacientes(self) -> List[Dict[str, Any]]:
        """Obtiene todos los pacientes activos"""
        try:
            with self.connection_manager.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                
                sql = "SELECT * FROM pacientes WHERE activo = 1 ORDER BY fecha_registro DESC"
                cursor.execute(sql)
                
                pacientes = cursor.fetchall()
                cursor.close()
                
                return pacientes
        except Exception as e:
            logger.error(f"❌ Error al obtener pacientes: {e}")
            raise
    
    def verificar_email_existe(self, email: str) -> bool:
        """Verifica si un email ya existe en la base de datos"""
        try:
            with self.connection_manager.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                
                sql = "SELECT id FROM pacientes WHERE email = %s AND activo = 1"
                cursor.execute(sql, (email.lower(),))
                
                paciente = cursor.fetchone()
                cursor.close()
                
                return paciente is not None
        except Exception as e:
            logger.error(f"❌ Error al verificar email: {e}")
            raise


class HistorialManager(MySQLDatabaseManager):
    """Gestor específico para historial de ejercicios"""
    
    def registrar_ejercicio(self, paciente_id: int, nivel_ejercicio: str, exito: bool, 
                          duracion_segundos: int, puntuacion: int, observaciones: str = None) -> Dict[str, Any]:
        """Registra un nuevo ejercicio"""
        try:
            with self.connection_manager.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                
                sql = """
                    INSERT INTO historial_ejercicios 
                    (paciente_id, nivel_ejercicio, exito, duracion_segundos, puntuacion, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (paciente_id, nivel_ejercicio, exito, duracion_segundos, puntuacion, observaciones)
                
                cursor.execute(sql, values)
                ejercicio_id = cursor.lastrowid
                
                connection.commit()
                cursor.close()
                
                logger.info(f"✅ Ejercicio registrado para paciente {paciente_id}")
                
                return {
                    'id': ejercicio_id,
                    'paciente_id': paciente_id,
                    'nivel_ejercicio': nivel_ejercicio,
                    'exito': exito,
                    'fecha_ejercicio': datetime.now().isoformat(),
                    'duracion_segundos': duracion_segundos,
                    'puntuacion': puntuacion,
                    'observaciones': observaciones
                }
        except Exception as e:
            logger.error(f"❌ Error al registrar ejercicio: {e}")
            raise
    
    def obtener_historial_paciente(self, paciente_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtiene el historial de ejercicios de un paciente"""
        try:
            with self.connection_manager.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                
                sql = """
                    SELECT * FROM historial_ejercicios 
                    WHERE paciente_id = %s 
                    ORDER BY fecha_ejercicio DESC 
                    LIMIT %s
                """
                cursor.execute(sql, (paciente_id, limit))
                
                historial = cursor.fetchall()
                cursor.close()
                
                return historial
        except Exception as e:
            logger.error(f"❌ Error al obtener historial: {e}")
            raise


class SesionTerapiaManager(MySQLDatabaseManager):
    """Gestor específico para sesiones de terapia"""
    
    def crear_sesion(self, paciente_id: int, duracion_minutos: int, 
                    tipo_terapia: str, observaciones: str = None) -> Dict[str, Any]:
        """Crea una nueva sesión de terapia"""
        try:
            with self.connection_manager.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                
                sql = """
                    INSERT INTO sesiones_terapia 
                    (paciente_id, duracion_minutos, tipo_terapia, observaciones)
                    VALUES (%s, %s, %s, %s)
                """
                values = (paciente_id, duracion_minutos, tipo_terapia, observaciones)
                
                cursor.execute(sql, values)
                sesion_id = cursor.lastrowid
                
                connection.commit()
                cursor.close()
                
                logger.info(f"✅ Sesión de terapia creada para paciente {paciente_id}")
                
                return {
                    'id': sesion_id,
                    'paciente_id': paciente_id,
                    'fecha_sesion': datetime.now().isoformat(),
                    'duracion_minutos': duracion_minutos,
                    'tipo_terapia': tipo_terapia,
                    'observaciones': observaciones
                }
        except Exception as e:
            logger.error(f"❌ Error al crear sesión: {e}")
            raise
    
    def obtener_sesiones_paciente(self, paciente_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """Obtiene las sesiones de terapia de un paciente"""
        try:
            with self.connection_manager.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                
                sql = """
                    SELECT * FROM sesiones_terapia 
                    WHERE paciente_id = %s 
                    ORDER BY fecha_sesion DESC 
                    LIMIT %s
                """
                cursor.execute(sql, (paciente_id, limit))
                
                sesiones = cursor.fetchall()
                cursor.close()
                
                return sesiones
        except Exception as e:
            logger.error(f"❌ Error al obtener sesiones: {e}")
            raise


class MySQLDatabaseService:
    """Servicio principal que agrupa todos los gestores"""
    
    def __init__(self):
        self.pacientes = PacienteManager()
        self.historial = HistorialManager()
        self.sesiones = SesionTerapiaManager()
        logger.info("✅ Servicio de base de datos MySQL inicializado")
    
    def test_connection(self) -> bool:
        """Prueba la conexión a la base de datos"""
        try:
            with self.pacientes.connection_manager.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                return result[0] == 1
        except Exception as e:
            logger.error(f"❌ Error en prueba de conexión: {e}")
            return False
    
    def get_database_info(self) -> Dict[str, Any]:
        """Obtiene información de la base de datos"""
        try:
            with self.pacientes.connection_manager.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                
                # Información de tablas
                cursor.execute("""
                    SELECT 
                        TABLE_NAME as tabla,
                        TABLE_ROWS as filas,
                        ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) AS tamaño_mb
                    FROM information_schema.TABLES 
                    WHERE TABLE_SCHEMA = DATABASE()
                    ORDER BY TABLE_NAME
                """)
                tablas = cursor.fetchall()
                
                # Conteo de registros
                cursor.execute("SELECT COUNT(*) as total FROM pacientes WHERE activo = 1")
                total_pacientes = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM historial_ejercicios")
                total_ejercicios = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM sesiones_terapia")
                total_sesiones = cursor.fetchone()['total']
                
                cursor.close()
                
                return {
                    'tablas': tablas,
                    'estadisticas': {
                        'pacientes': total_pacientes,
                        'ejercicios': total_ejercicios,
                        'sesiones': total_sesiones
                    }
                }
        except Exception as e:
            logger.error(f"❌ Error al obtener información de BD: {e}")
            raise
