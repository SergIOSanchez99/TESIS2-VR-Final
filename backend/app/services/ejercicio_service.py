"""
Servicio de Ejercicios - Patrón de Diseño Service Layer
Responsable de la lógica de negocio relacionada con ejercicios
"""
from typing import List, Dict, Optional
from ..models.ejercicio import Ejercicio, TipoEjercicio, NivelDificultad, EjercicioRepository
from ..models.paciente import Paciente


class EjercicioService:
    """Servicio para gestión de ejercicios - Patrón Service Layer"""
    
    def __init__(self):
        self.ejercicio_repo = EjercicioRepository()
        self._ejercicios_disponibles = self._inicializar_ejercicios()
    
    def _inicializar_ejercicios(self) -> List[Ejercicio]:
        """Inicializa los ejercicios disponibles en el sistema"""
        ejercicios = [
            Ejercicio(
                id="rehabilitacion_nivel_1",
                nombre="Objetivo Estático",
                descripcion="Ejercicio de precisión con objetivo fijo",
                tipo=TipoEjercicio.REHABILITACION,
                nivel=NivelDificultad.PRINCIPIANTE,
                instrucciones=[
                    "Usa las flechas del teclado para mover la mano azul",
                    "Toca el objetivo rojo para completar el ejercicio",
                    "Mantén la precisión y control"
                ],
                parametros={
                    "velocidad_mano": 10,
                    "tamaño_objetivo": 60,
                    "tiempo_limite": None
                }
            ),
            Ejercicio(
                id="rehabilitacion_nivel_2",
                nombre="Objetivo en Movimiento Lento",
                descripcion="Ejercicio de precisión con objetivo en movimiento lento",
                tipo=TipoEjercicio.REHABILITACION,
                nivel=NivelDificultad.INTERMEDIO,
                instrucciones=[
                    "Usa las flechas del teclado para mover la mano azul",
                    "El objetivo rojo se mueve lentamente",
                    "Anticipa el movimiento y mantén la precisión"
                ],
                parametros={
                    "velocidad_mano": 10,
                    "velocidad_objetivo": 3,
                    "tamaño_objetivo": 60,
                    "tiempo_limite": None
                }
            ),
            Ejercicio(
                id="rehabilitacion_nivel_3",
                nombre="Objetivo en Movimiento Rápido",
                descripcion="Ejercicio de precisión con objetivo en movimiento rápido",
                tipo=TipoEjercicio.REHABILITACION,
                nivel=NivelDificultad.AVANZADO,
                instrucciones=[
                    "Usa las flechas del teclado para mover la mano azul",
                    "El objetivo rojo se mueve rápidamente",
                    "Requiere máxima concentración y velocidad de reacción"
                ],
                parametros={
                    "velocidad_mano": 10,
                    "velocidad_objetivo": 7,
                    "tamaño_objetivo": 60,
                    "tiempo_limite": None
                }
            ),
            Ejercicio(
                id="terapia_abotonar_camisa",
                nombre="Abotonar Camisa",
                descripcion="Ejercicio de coordinación fina para mejorar la destreza manual y la precisión en movimientos pequeños.",
                tipo=TipoEjercicio.TERAPIA_OCUPACIONAL,
                nivel=NivelDificultad.PRINCIPIANTE,
                instrucciones=[
                    "Haz clic en los botones en orden de arriba a abajo",
                    "Sigue la secuencia correcta",
                    "Practica la coordinación mano-ojo"
                ],
                parametros={
                    "numero_botones": 5,
                    "tiempo_limite": None
                }
            ),
            Ejercicio(
                id="terapia_arrastrar_objeto",
                nombre="Arrastrar y Soltar",
                descripcion="Ejercicio de coordinación mano-ojo para mejorar la capacidad de manipulación de objetos.",
                tipo=TipoEjercicio.TERAPIA_OCUPACIONAL,
                nivel=NivelDificultad.INTERMEDIO,
                instrucciones=[
                    "Arrastra cada objeto a su área de destino correspondiente",
                    "Mantén el control durante el arrastre",
                    "Practica la precisión en el posicionamiento"
                ],
                parametros={
                    "tamaño_objetivo": 60,
                    "tiempo_limite": None
                }
            ),
            Ejercicio(
                id="terapia_abrir_cerradura",
                nombre="Abrir Cerradura",
                descripcion="Ejercicio de motricidad fina para mejorar la destreza en tareas de precisión como usar llaves.",
                tipo=TipoEjercicio.TERAPIA_OCUPACIONAL,
                nivel=NivelDificultad.INTERMEDIO,
                instrucciones=[
                    "Inserta la llave en la cerradura",
                    "Gira la llave en la dirección correcta",
                    "Practica la coordinación y precisión"
                ],
                parametros={
                    "tiempo_limite": None
                }
            ),
            Ejercicio(
                id="terapia_usar_cubiertos",
                nombre="Usar Cubiertos",
                descripcion="Simulación de uso de cubiertos para mejorar la coordinación y habilidades de alimentación independiente.",
                tipo=TipoEjercicio.TERAPIA_OCUPACIONAL,
                nivel=NivelDificultad.INTERMEDIO,
                instrucciones=[
                    "Simula el uso de cubiertos para comer",
                    "Practica la coordinación mano-ojo",
                    "Mejora las habilidades de alimentación"
                ],
                parametros={
                    "tiempo_limite": None
                }
            ),
            Ejercicio(
                id="terapia_rompecabezas",
                nombre="Rompecabezas",
                descripcion="Ejercicio de organización espacial y resolución de problemas para mejorar la función cognitiva y motora.",
                tipo=TipoEjercicio.TERAPIA_OCUPACIONAL,
                nivel=NivelDificultad.AVANZADO,
                instrucciones=[
                    "Arma el rompecabezas arrastrando las piezas",
                    "Observa la imagen completa",
                    "Practica la organización espacial"
                ],
                parametros={
                    "numero_piezas": 9,
                    "tiempo_limite": None
                }
            ),
            Ejercicio(
                id="terapia_clasificar_objetos",
                nombre="Clasificar Objetos",
                descripcion="Ejercicio de organización y categorización para mejorar habilidades de planificación y ejecución.",
                tipo=TipoEjercicio.TERAPIA_OCUPACIONAL,
                nivel=NivelDificultad.INTERMEDIO,
                instrucciones=[
                    "Clasifica los objetos en sus categorías correspondientes",
                    "Observa las características de cada objeto",
                    "Practica la organización y planificación"
                ],
                parametros={
                    "numero_categorias": 3,
                    "tiempo_limite": None
                }
            )
        ]
        return ejercicios
    
    def obtener_ejercicios_por_tipo(self, tipo: TipoEjercicio) -> List[Ejercicio]:
        """Obtiene ejercicios filtrados por tipo"""
        return [e for e in self._ejercicios_disponibles if e.tipo == tipo and e.activo]
    
    def obtener_ejercicios_por_nivel(self, nivel: NivelDificultad) -> List[Ejercicio]:
        """Obtiene ejercicios filtrados por nivel de dificultad"""
        return [e for e in self._ejercicios_disponibles if e.nivel == nivel and e.activo]
    
    def obtener_ejercicio_por_id(self, ejercicio_id: str) -> Optional[Ejercicio]:
        """Obtiene un ejercicio específico por ID"""
        for ejercicio in self._ejercicios_disponibles:
            if ejercicio.id == ejercicio_id and ejercicio.activo:
                return ejercicio
        return None
    
    def obtener_todos_ejercicios(self) -> List[Ejercicio]:
        """Obtiene todos los ejercicios activos"""
        return [e for e in self._ejercicios_disponibles if e.activo]
    
    def obtener_ejercicios_rehabilitacion(self) -> List[Ejercicio]:
        """Obtiene ejercicios de rehabilitación"""
        return self.obtener_ejercicios_por_tipo(TipoEjercicio.REHABILITACION)
    
    def obtener_ejercicios_terapia_ocupacional(self) -> List[Ejercicio]:
        """Obtiene ejercicios de terapia ocupacional"""
        return self.obtener_ejercicios_por_tipo(TipoEjercicio.TERAPIA_OCUPACIONAL)
    
    def registrar_resultado(self, paciente: Paciente, ejercicio_id: str, exito: bool,
                          tiempo_ejecucion: Optional[float] = None,
                          puntuacion: Optional[int] = None,
                          observaciones: Optional[str] = None,
                          precision: Optional[float] = None,
                          velocidad_promedio: Optional[float] = None,
                          rango_movimiento: Optional[float] = None,
                          tiempo_reaccion_promedio: Optional[float] = None,
                          tasa_aciertos: Optional[float] = None,
                          consistencia: Optional[float] = None,
                          combo_maximo: Optional[int] = None,
                          aciertos: Optional[int] = None,
                          fallos: Optional[int] = None,
                          nivel: Optional[int] = None):
        """Registra el resultado de un ejercicio con métricas médicas avanzadas"""
        return self.ejercicio_repo.registrar_resultado(
            paciente.id, ejercicio_id, exito, tiempo_ejecucion, puntuacion, observaciones,
            precision=precision,
            velocidad_promedio=velocidad_promedio,
            rango_movimiento=rango_movimiento,
            tiempo_reaccion_promedio=tiempo_reaccion_promedio,
            tasa_aciertos=tasa_aciertos,
            consistencia=consistencia,
            combo_maximo=combo_maximo,
            aciertos=aciertos,
            fallos=fallos,
            nivel=nivel
        )
    
    def obtener_estadisticas_ejercicio(self, paciente_id: str, ejercicio_id: str) -> Dict:
        """Obtiene estadísticas específicas de un ejercicio para un paciente"""
        historial = self.ejercicio_repo.obtener_historial(paciente_id)
        ejercicios_filtrados = [r for r in historial if r.tipo_ejercicio == ejercicio_id]
        
        if not ejercicios_filtrados:
            return {
                'total_intentos': 0,
                'exitos': 0,
                'porcentaje_exito': 0,
                'promedio_tiempo': 0,
                'mejor_tiempo': None,
                'ultima_actividad': None
            }
        
        total = len(ejercicios_filtrados)
        exitos = sum(1 for r in ejercicios_filtrados if r.exito)
        porcentaje = (exitos / total) * 100 if total > 0 else 0
        
        tiempos = [r.tiempo_ejecucion for r in ejercicios_filtrados if r.tiempo_ejecucion]
        promedio_tiempo = sum(tiempos) / len(tiempos) if tiempos else 0
        mejor_tiempo = min(tiempos) if tiempos else None
        
        ultima_actividad = max(ejercicios_filtrados, key=lambda x: x.fecha).fecha
        
        return {
            'total_intentos': total,
            'exitos': exitos,
            'porcentaje_exito': round(porcentaje, 2),
            'promedio_tiempo': round(promedio_tiempo, 2),
            'mejor_tiempo': mejor_tiempo,
            'ultima_actividad': ultima_actividad
        }
    
    def obtener_recomendacion_ejercicio(self, paciente_id: str) -> Optional[Ejercicio]:
        """Obtiene una recomendación de ejercicio basada en el historial del paciente"""
        historial = self.ejercicio_repo.obtener_historial(paciente_id)
        
        if not historial:
            # Si no hay historial, recomendar nivel principiante
            return self.obtener_ejercicio_por_id("rehabilitacion_nivel_1")
        
        # Analizar el último ejercicio realizado
        ultimo_ejercicio = max(historial, key=lambda x: x.fecha)
        
        # Si el último ejercicio fue exitoso, sugerir el siguiente nivel
        if ultimo_ejercicio.exito:
            if "nivel_1" in ultimo_ejercicio.tipo_ejercicio:
                return self.obtener_ejercicio_por_id("rehabilitacion_nivel_2")
            elif "nivel_2" in ultimo_ejercicio.tipo_ejercicio:
                return self.obtener_ejercicio_por_id("rehabilitacion_nivel_3")
        
        # Si no fue exitoso, sugerir el mismo nivel o uno anterior
        return self.obtener_ejercicio_por_id(ultimo_ejercicio.tipo_ejercicio)
