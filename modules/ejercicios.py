import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox
from modules.usuarios import registrar_resultado, obtener_historial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COLOR_FONDO = "#e6f0fa"
COLOR_BOTON = "#1976d2"
COLOR_BOTON_TEXTO = "#ffffff"
FONT_TITULO = ("Arial", 18, "bold")
FONT_NORMAL = ("Arial", 12)


def menu_ejercicios_grafico(root, paciente, volver_callback):
    def lanzar_ejercicio(nivel):
        root.withdraw()
        exito = ejecutar_ejercicio(nivel, paciente)
        registrar_resultado(paciente, f"Ejercicio nivel {nivel}", exito)
        root.deiconify()
    def mostrar_historial():
        historial = obtener_historial(paciente)
        if not historial:
            messagebox.showinfo("Historial", "No hay registros de ejercicios.")
            return
        ventana = tk.Toplevel(root)
        ventana.title("Historial de ejercicios")
        ventana.configure(bg=COLOR_FONDO)
        tk.Label(ventana, text=f"Historial de {paciente['nombre']}", font=FONT_TITULO, bg=COLOR_FONDO, fg="#0d47a1").pack(pady=(15, 5))
        fig, ax = plt.subplots(figsize=(5,3))
        fechas = [h['fecha'] for h in historial]
        niveles = [h['nivel'] for h in historial]
        exitos = [1 if h['exito'] else 0 for h in historial]
        ax.plot(fechas, niveles, marker='o', label='Nivel')
        ax.bar(fechas, exitos, alpha=0.3, label='Éxito')
        ax.set_ylabel('Nivel / Éxito')
        ax.set_xlabel('Fecha')
        ax.set_title('Progreso del paciente')
        ax.legend()
        plt.xticks(rotation=45, ha='right')
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
        boton_cerrar = tk.Button(ventana, text="Cerrar", font=("Arial", 12, "bold"), bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, width=15, height=1, bd=0, relief="ridge", activebackground="#1565c0", activeforeground=COLOR_BOTON_TEXTO, command=ventana.destroy)
        boton_cerrar.pack(pady=10)
    def abrir_terapia_ocupacional():
        ventana = tk.Toplevel(root)
        ventana.title("Terapia Ocupacional")
        ventana.configure(bg=COLOR_FONDO)
        tk.Label(ventana, text="Terapia Ocupacional", font=FONT_TITULO, bg=COLOR_FONDO, fg="#0d47a1").pack(pady=(20, 10))
        tk.Button(ventana, text="Abotonar camisa", font=("Arial", 13, "bold"), bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, width=25, height=2, bd=0, relief="ridge", activebackground="#1565c0", activeforeground=COLOR_BOTON_TEXTO, command=lambda: [ventana.withdraw(), abotonar_camisa(paciente, ventana)]).pack(pady=8)
        tk.Button(ventana, text="Arrastrar y soltar objeto", font=("Arial", 13, "bold"), bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, width=25, height=2, bd=0, relief="ridge", activebackground="#1565c0", activeforeground=COLOR_BOTON_TEXTO, command=lambda: [ventana.withdraw(), arrastrar_objeto(paciente, ventana)]).pack(pady=8)
        tk.Button(ventana, text="Cerrar", font=("Arial", 13, "bold"), bg="#bdbdbd", fg="#263238", width=25, height=2, bd=0, relief="ridge", activebackground="#757575", activeforeground="#263238", command=ventana.destroy).pack(pady=12)
    frame = tk.Frame(root, bg=COLOR_FONDO)
    frame.pack(expand=True, fill="both")
    tk.Label(frame, text=f"Paciente: {paciente['nombre']}", font=FONT_NORMAL, bg=COLOR_FONDO, fg="#1976d2").pack(pady=(20, 5))
    tk.Label(frame, text="Seleccione el nivel de ejercicio:", font=FONT_TITULO, bg=COLOR_FONDO, fg="#0d47a1").pack(pady=(0, 15))
    boton1 = tk.Button(frame, text="Nivel 1 (objetivo estático)", font=("Arial", 13, "bold"), bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, width=30, height=2, bd=0, relief="ridge", activebackground="#1565c0", activeforeground=COLOR_BOTON_TEXTO, command=lambda: lanzar_ejercicio(1))
    boton1.pack(pady=6)
    boton2 = tk.Button(frame, text="Nivel 2 (objetivo se mueve lento)", font=("Arial", 13, "bold"), bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, width=30, height=2, bd=0, relief="ridge", activebackground="#1565c0", activeforeground=COLOR_BOTON_TEXTO, command=lambda: lanzar_ejercicio(2))
    boton2.pack(pady=6)
    boton3 = tk.Button(frame, text="Nivel 3 (objetivo se mueve rápido)", font=("Arial", 13, "bold"), bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, width=30, height=2, bd=0, relief="ridge", activebackground="#1565c0", activeforeground=COLOR_BOTON_TEXTO, command=lambda: lanzar_ejercicio(3))
    boton3.pack(pady=6)
    # --- Botón de Terapia Ocupacional ---
    boton_terapia = tk.Button(frame, text="Terapia Ocupacional", font=("Arial", 13, "bold"), bg="#ff9800", fg="#fff", width=30, height=2, bd=0, relief="ridge", activebackground="#fb8c00", activeforeground="#fff", command=abrir_terapia_ocupacional)
    boton_terapia.pack(pady=12)
    # ---
    boton_hist = tk.Button(frame, text="Ver historial y avance", font=("Arial", 13, "bold"), bg="#43a047", fg=COLOR_BOTON_TEXTO, width=30, height=2, bd=0, relief="ridge", activebackground="#388e3c", activeforeground=COLOR_BOTON_TEXTO, command=mostrar_historial)
    boton_hist.pack(pady=12)
    boton_volver = tk.Button(frame, text="Volver", font=("Arial", 13, "bold"), bg="#bdbdbd", fg="#263238", width=30, height=2, bd=0, relief="ridge", activebackground="#757575", activeforeground="#263238", command=lambda: [frame.destroy(), volver_callback()])
    boton_volver.pack(pady=6)

def ejecutar_ejercicio(nivel, paciente):
    """Ejecuta un ejercicio de rehabilitación motora mejorado con pygame"""
    import time
    import math
    
    pygame.init()
    pygame.mixer.init()
    
    # Configuración de pantalla
    ancho, alto = 1000, 700
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption(f"Rehabilitación Motora - Nivel {nivel} | Paciente: {paciente.get('nombre', 'Usuario')}")
    reloj = pygame.time.Clock()
    
    # Colores mejorados
    BLANCO = (255, 255, 255)
    AZUL_PRIMARIO = (25, 118, 210)
    AZUL_SECUNDARIO = (66, 165, 245)
    ROJO_PRIMARIO = (244, 67, 54)
    VERDE_EXITO = (76, 175, 80)
    VERDE_CLARO = (129, 199, 132)
    GRIS_FONDO = (245, 247, 250)
    GRIS_OSCURO = (97, 97, 97)
    AMARILLO = (255, 193, 7)
    NARANJA = (255, 152, 0)
    
    # Fuentes
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_grande = pygame.font.Font(None, 36)
    fuente_mediana = pygame.font.Font(None, 24)
    fuente_pequena = pygame.font.Font(None, 18)
    
    # Estado del juego
    tiempo_inicio = time.time()
    tiempo_limite = 60  # 60 segundos
    puntuacion = 0
    aciertos = 0
    fallos = 0
    combo = 0
    max_combo = 0
    ultimo_acierto_tiempo = 0
    
    # Métricas médicas
    metricas = {
        'tiempos_reaccion': [],
        'distancias_movimiento': [],
        'posiciones_mano': [],
        'posiciones_objetivo': [],
        'min_x': float('inf'),
        'max_x': float('-inf'),
        'min_y': float('inf'),
        'max_y': float('-inf')
    }
    
    # Mano virtual mejorada
    mano_size = 45
    mano_x, mano_y = ancho // 2, alto // 2
    velocidad_base = 8
    velocidad = velocidad_base
    mano_color = AZUL_PRIMARIO
    mano_pulso = 0
    
    # Objetivo mejorado
    objetivo_size = nivel == 1 and 50 or nivel == 2 and 45 or 40
    objetivo_x = random.randint(objetivo_size, ancho - objetivo_size)
    objetivo_y = random.randint(objetivo_size, alto - objetivo_size)
    objetivo_vx, objetivo_vy = 0, 0
    
    if nivel == 2:
        objetivo_vx = random.choice([-2, 2])
        objetivo_vy = random.choice([-2, 2])
    elif nivel == 3:
        objetivo_vx = random.choice([-5, 5])
        objetivo_vy = random.choice([-5, 5])
    
    objetivo_color = ROJO_PRIMARIO
    objetivo_pulso = 0
    objetivo_brillo = 0
    
    # Partículas para efectos visuales
    particulas = []
    
    # Estado del juego
    juego_activo = True
    pausado = False
    objetivo_tocado = False
    
    # Bucle principal del juego
    while juego_activo:
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicio
        tiempo_restante = max(0, tiempo_limite - tiempo_transcurrido)
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                juego_activo = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    juego_activo = False
                elif event.key == pygame.K_SPACE:
                    pausado = not pausado
                elif event.key == pygame.K_r and not juego_activo:
                    # Reiniciar juego
                    return ejecutar_ejercicio(nivel, paciente)
        
        if pausado:
            # Mostrar pantalla de pausa
            pantalla.fill(GRIS_FONDO)
            texto_pausa = fuente_grande.render("PAUSADO - Presiona ESPACIO para continuar", True, GRIS_OSCURO)
            pantalla.blit(texto_pausa, (ancho//2 - texto_pausa.get_width()//2, alto//2))
            pygame.display.flip()
            reloj.tick(60)
            continue
        
        if tiempo_restante <= 0:
            juego_activo = False
            continue
        
        # Control de movimiento mejorado
        teclas = pygame.key.get_pressed()
        movimiento_x = 0
        movimiento_y = 0
        
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            movimiento_x = -velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            movimiento_x = velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            movimiento_y = -velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            movimiento_y = velocidad
        
        # Movimiento diagonal suave
        if movimiento_x != 0 and movimiento_y != 0:
            movimiento_x *= 0.707  # Normalización para movimiento diagonal
            movimiento_y *= 0.707
        
        mano_x += movimiento_x
        mano_y += movimiento_y
        
        # Limitar movimiento dentro de la pantalla
        mano_x = max(mano_size//2, min(ancho - mano_size//2, mano_x))
        mano_y = max(mano_size//2, min(alto - mano_size//2, mano_y))
        
        # Registrar posición para métricas
        metricas['posiciones_mano'].append((mano_x, mano_y))
        if len(metricas['posiciones_mano']) > 100:
            metricas['posiciones_mano'].pop(0)
        
        metricas['min_x'] = min(metricas['min_x'], mano_x)
        metricas['max_x'] = max(metricas['max_x'], mano_x)
        metricas['min_y'] = min(metricas['min_y'], mano_y)
        metricas['max_y'] = max(metricas['max_y'], mano_y)
        
        # Calcular distancia recorrida
        if len(metricas['posiciones_mano']) > 1:
            dist = math.sqrt(
                (metricas['posiciones_mano'][-1][0] - metricas['posiciones_mano'][-2][0])**2 +
                (metricas['posiciones_mano'][-1][1] - metricas['posiciones_mano'][-2][1])**2
            )
            metricas['distancias_movimiento'].append(dist)
        
        # Movimiento del objetivo mejorado
        if nivel > 1:
            objetivo_pulso += 0.1
            objetivo_brillo = abs(math.sin(objetivo_pulso)) * 50
            
            objetivo_x += objetivo_vx
            objetivo_y += objetivo_vy
            
            # Rebote mejorado con amortiguación
            bounce_damping = 0.95 if nivel == 2 else 0.9
            
            if objetivo_x <= objetivo_size or objetivo_x >= ancho - objetivo_size:
                objetivo_vx *= -bounce_damping
                objetivo_x = max(objetivo_size, min(ancho - objetivo_size, objetivo_x))
                if nivel == 3:
                    objetivo_vy += random.choice([-2, 2])
            
            if objetivo_y <= objetivo_size or objetivo_y >= alto - objetivo_size:
                objetivo_vy *= -bounce_damping
                objetivo_y = max(objetivo_size, min(alto - objetivo_size, objetivo_y))
                if nivel == 3:
                    objetivo_vx += random.choice([-2, 2])
            
            # Para nivel 3, agregar cambios de dirección aleatorios
            if nivel == 3 and random.random() < 0.02:
                objetivo_vx += random.choice([-3, 3])
                objetivo_vy += random.choice([-3, 3])
            
            # Limitar velocidad máxima
            velocidad_max = 8 if nivel == 2 else 12
            velocidad_actual = math.sqrt(objetivo_vx**2 + objetivo_vy**2)
            if velocidad_actual > velocidad_max:
                factor = velocidad_max / velocidad_actual
                objetivo_vx *= factor
                objetivo_vy *= factor
            
            metricas['posiciones_objetivo'].append((objetivo_x, objetivo_y))
            if len(metricas['posiciones_objetivo']) > 100:
                metricas['posiciones_objetivo'].pop(0)
        
        # Detección de colisión mejorada
        distancia = math.sqrt((mano_x - objetivo_x)**2 + (mano_y - objetivo_y)**2)
        objetivo_anterior_tocado = objetivo_tocado
        
        if distancia <= (mano_size//2 + objetivo_size//2):
            if not objetivo_tocado:
                objetivo_tocado = True
                aciertos += 1
                combo += 1
                max_combo = max(max_combo, combo)
                
                # Calcular tiempo de reacción
                if ultimo_acierto_tiempo > 0:
                    tiempo_reaccion = tiempo_actual - ultimo_acierto_tiempo
                    metricas['tiempos_reaccion'].append(tiempo_reaccion)
                ultimo_acierto_tiempo = tiempo_actual
                
                # Calcular puntuación con multiplicador de combo
                puntos_base = nivel * 10
                multiplicador_combo = 1 + (combo * 0.1)
                puntos_obtenidos = int(puntos_base * multiplicador_combo)
                puntuacion += puntos_obtenidos
                
                # Crear partículas de éxito
                for _ in range(20):
                    particulas.append({
                        'x': objetivo_x,
                        'y': objetivo_y,
                        'vx': random.uniform(-5, 5),
                        'vy': random.uniform(-5, 5),
                        'life': 1.0,
                        'color': VERDE_EXITO,
                        'size': random.randint(3, 8)
                    })
                
                # Reposicionar objetivo
                objetivo_x = random.randint(objetivo_size, ancho - objetivo_size)
                objetivo_y = random.randint(objetivo_size, alto - objetivo_size)
                
                if nivel == 2:
                    objetivo_vx = random.choice([-2, 2])
                    objetivo_vy = random.choice([-2, 2])
                elif nivel == 3:
                    objetivo_vx = random.choice([-5, 5])
                    objetivo_vy = random.choice([-5, 5])
        else:
            if objetivo_anterior_tocado:
                objetivo_tocado = False
            combo = 0
        
        # Actualizar partículas
        for particula in particulas[:]:
            particula['x'] += particula['vx']
            particula['y'] += particula['vy']
            particula['life'] -= 0.02
            particula['vx'] *= 0.98
            particula['vy'] *= 0.98
            
            if particula['life'] <= 0:
                particulas.remove(particula)
        
        # Efectos visuales
        mano_pulso += 0.15
        pulso_mano = math.sin(mano_pulso) * 3
        
        # Dibujar fondo con gradiente
        pantalla.fill(GRIS_FONDO)
        
        # Dibujar cuadrícula de fondo
        for x in range(0, ancho, 50):
            pygame.draw.line(pantalla, (230, 230, 235), (x, 0), (x, alto), 1)
        for y in range(0, alto, 50):
            pygame.draw.line(pantalla, (230, 230, 235), (0, y), (ancho, y), 1)
        
        # Dibujar objetivo con efectos
        objetivo_pulso_visual = math.sin(objetivo_pulso) * 5
        objetivo_size_visual = objetivo_size + objetivo_pulso_visual
        
        # Brillo del objetivo
        if nivel > 1:
            brillo_color = (
                min(255, ROJO_PRIMARIO[0] + int(objetivo_brillo)),
                min(255, ROJO_PRIMARIO[1] + int(objetivo_brillo)),
                min(255, ROJO_PRIMARIO[2] + int(objetivo_brillo))
            )
        else:
            brillo_color = ROJO_PRIMARIO
        
        # Círculo exterior del objetivo
        pygame.draw.circle(pantalla, brillo_color, (int(objetivo_x), int(objetivo_y)), int(objetivo_size_visual + 10), 3)
        # Círculo principal del objetivo
        pygame.draw.circle(pantalla, brillo_color, (int(objetivo_x), int(objetivo_y)), int(objetivo_size_visual))
        # Círculo interior
        pygame.draw.circle(pantalla, BLANCO, (int(objetivo_x), int(objetivo_y)), int(objetivo_size_visual * 0.6), 2)
        # Centro del objetivo
        pygame.draw.circle(pantalla, BLANCO, (int(objetivo_x), int(objetivo_y)), 5)
        
        # Dibujar mano virtual mejorada
        mano_size_visual = mano_size + pulso_mano
        
        # Sombra de la mano
        pygame.draw.circle(pantalla, (0, 0, 0, 50), (int(mano_x + 3), int(mano_y + 3)), int(mano_size_visual//2), 0)
        
        # Mano con gradiente simulado
        pygame.draw.circle(pantalla, AZUL_SECUNDARIO, (int(mano_x), int(mano_y)), int(mano_size_visual//2))
        pygame.draw.circle(pantalla, AZUL_PRIMARIO, (int(mano_x), int(mano_y)), int(mano_size_visual//2 * 0.8))
        pygame.draw.circle(pantalla, BLANCO, (int(mano_x), int(mano_y)), int(mano_size_visual//2 * 0.5))
        
        # Dibujar partículas
        for particula in particulas:
            alpha = int(255 * particula['life'])
            color_con_alpha = (*particula['color'][:3], alpha)
            pygame.draw.circle(
                pantalla,
                particula['color'],
                (int(particula['x']), int(particula['y'])),
                particula['size']
            )
        
        # Dibujar UI mejorada
        # Panel superior
        pygame.draw.rect(pantalla, (255, 255, 255, 200), (10, 10, ancho - 20, 80))
        pygame.draw.rect(pantalla, AZUL_PRIMARIO, (10, 10, ancho - 20, 80), 3)
        
        # Tiempo restante
        tiempo_texto = fuente_mediana.render(f"Tiempo: {int(tiempo_restante)}s", True, GRIS_OSCURO)
        pantalla.blit(tiempo_texto, (30, 25))
        
        # Puntuación
        puntuacion_texto = fuente_mediana.render(f"Puntos: {puntuacion}", True, VERDE_EXITO)
        pantalla.blit(puntuacion_texto, (250, 25))
        
        # Aciertos
        aciertos_texto = fuente_mediana.render(f"Aciertos: {aciertos}", True, AZUL_PRIMARIO)
        pantalla.blit(aciertos_texto, (450, 25))
        
        # Precisión
        total_intentos_actual = aciertos + fallos
        precision_actual = (aciertos / total_intentos_actual * 100) if total_intentos_actual > 0 else 0
        precision_texto = fuente_mediana.render(f"Precisión: {precision_actual:.1f}%", True, NARANJA)
        pantalla.blit(precision_texto, (650, 25))
        
        # Combo
        if combo > 1:
            combo_texto = fuente_grande.render(f"COMBO x{combo}!", True, AMARILLO)
            pantalla.blit(combo_texto, (850, 20))
        
        # Panel de métricas (lateral derecho)
        panel_ancho = 200
        pygame.draw.rect(pantalla, (255, 255, 255, 200), (ancho - panel_ancho - 10, 100, panel_ancho, alto - 110))
        pygame.draw.rect(pantalla, AZUL_PRIMARIO, (ancho - panel_ancho - 10, 100, panel_ancho, alto - 110), 3)
        
        titulo_metricas = fuente_pequena.render("MÉTRICAS", True, AZUL_PRIMARIO)
        pantalla.blit(titulo_metricas, (ancho - panel_ancho + 10, 110))
        
        y_offset = 140
        # Velocidad promedio
        if len(metricas['distancias_movimiento']) > 0:
            velocidad_promedio = sum(metricas['distancias_movimiento'][-30:]) / min(30, len(metricas['distancias_movimiento'])) * 60
            vel_texto = fuente_pequena.render(f"Velocidad: {velocidad_promedio:.1f} px/s", True, GRIS_OSCURO)
            pantalla.blit(vel_texto, (ancho - panel_ancho + 10, y_offset))
            y_offset += 25
        
        # Rango de movimiento
        rango_x = metricas['max_x'] - metricas['min_x'] if metricas['max_x'] != float('-inf') else 0
        rango_y = metricas['max_y'] - metricas['min_y'] if metricas['max_y'] != float('-inf') else 0
        rango_texto = fuente_pequena.render(f"Rango: {max(rango_x, rango_y):.0f} px", True, GRIS_OSCURO)
        pantalla.blit(rango_texto, (ancho - panel_ancho + 10, y_offset))
        y_offset += 25
        
        # Tiempo de reacción promedio
        if len(metricas['tiempos_reaccion']) > 0:
            tiempo_reaccion_prom = sum(metricas['tiempos_reaccion']) / len(metricas['tiempos_reaccion']) * 1000
            react_texto = fuente_pequena.render(f"Reacción: {tiempo_reaccion_prom:.0f} ms", True, GRIS_OSCURO)
            pantalla.blit(react_texto, (ancho - panel_ancho + 10, y_offset))
            y_offset += 25
        
        # Combo máximo
        combo_max_texto = fuente_pequena.render(f"Combo Max: {max_combo}", True, GRIS_OSCURO)
        pantalla.blit(combo_max_texto, (ancho - panel_ancho + 10, y_offset))
        
        # Instrucciones
        instrucciones = [
            "Flechas o WASD: Mover",
            "ESPACIO: Pausar",
            "ESC: Salir"
        ]
        y_inst = alto - 100
        for instruccion in instrucciones:
            inst_texto = fuente_pequena.render(instruccion, True, GRIS_OSCURO)
            pantalla.blit(inst_texto, (30, y_inst))
            y_inst += 20
        
        pygame.display.flip()
        reloj.tick(60)  # 60 FPS para animaciones suaves
    
    # Calcular métricas finales
    tiempo_total = tiempo_limite - tiempo_restante
    total_intentos = aciertos + fallos
    precision_final = (aciertos / total_intentos * 100) if total_intentos > 0 else 0
    
    # Determinar éxito basado en criterios médicos
    criterio_precision = nivel == 1 and 60 or nivel == 2 and 50 or 40
    criterio_aciertos = nivel * 3
    exito = precision_final >= criterio_precision and aciertos >= criterio_aciertos
    
    # Preparar métricas para registro
    metricas_finales = {
        'precision': round(precision_final, 2),
        'puntuacion': puntuacion,
        'aciertos': aciertos,
        'fallos': fallos,
        'tiempo_total': round(tiempo_total, 2),
        'combo_maximo': max_combo,
        'velocidad_promedio': round(sum(metricas['distancias_movimiento'][-30:]) / min(30, len(metricas['distancias_movimiento'])) * 60, 2) if metricas['distancias_movimiento'] else 0,
        'rango_movimiento': round(max(rango_x, rango_y), 2),
        'tiempo_reaccion_promedio': round(sum(metricas['tiempos_reaccion']) / len(metricas['tiempos_reaccion']) * 1000, 2) if metricas['tiempos_reaccion'] else 0
    }
    
    # Mostrar pantalla de resultados
    mostrar_resultados_pygame(pantalla, ancho, alto, exito, puntuacion, aciertos, precision_final, max_combo, metricas_finales, fuente_grande, fuente_mediana)
    
    pygame.quit()
    
    # Registrar resultado con métricas
    registrar_resultado(paciente, f"Ejercicio nivel {nivel}", exito)
    
    return exito

def mostrar_resultados_pygame(pantalla, ancho, alto, exito, puntuacion, aciertos, precision, combo_max, metricas, fuente_grande, fuente_mediana):
    """Muestra pantalla de resultados mejorada"""
    import time
    
    BLANCO = (255, 255, 255)
    VERDE_EXITO = (76, 175, 80)
    NARANJA = (255, 152, 0)
    GRIS_FONDO = (245, 247, 250)
    AZUL_PRIMARIO = (25, 118, 210)
    GRIS_OSCURO = (97, 97, 97)
    
    pantalla.fill(GRIS_FONDO)
    
    # Título
    if exito:
        titulo = fuente_grande.render("¡EXCELENTE TRABAJO!", True, VERDE_EXITO)
    else:
        titulo = fuente_grande.render("Continúa Practicando", True, NARANJA)
    
    pantalla.blit(titulo, (ancho//2 - titulo.get_width()//2, 100))
    
    # Estadísticas
    y_pos = 200
    estadisticas = [
        f"Puntuación: {puntuacion}",
        f"Aciertos: {aciertos}",
        f"Precisión: {precision:.1f}%",
        f"Combo Máximo: {combo_max}",
        f"Velocidad Promedio: {metricas['velocidad_promedio']:.1f} px/s",
        f"Rango de Movimiento: {metricas['rango_movimiento']:.0f} px",
        f"Tiempo de Reacción: {metricas['tiempo_reaccion_promedio']:.0f} ms"
    ]
    
    for estadistica in estadisticas:
        texto = fuente_mediana.render(estadistica, True, GRIS_OSCURO)
        pantalla.blit(texto, (ancho//2 - texto.get_width()//2, y_pos))
        y_pos += 40
    
    # Instrucciones
    instruccion = fuente_mediana.render("Presiona cualquier tecla para continuar...", True, AZUL_PRIMARIO)
    pantalla.blit(instruccion, (ancho//2 - instruccion.get_width()//2, alto - 100))
    
    pygame.display.flip()
    
    # Esperar input del usuario
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esperando = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                esperando = False
        time.sleep(0.1)

def mostrar_ventana_exito():
    ventana = tk.Toplevel()
    ventana.title("¡Ejercicio completado!")
    ventana.configure(bg="#e6f0fa")
    ventana.geometry("400x220")
    ventana.resizable(False, False)
    # Ícono grande de éxito
    icono = tk.Label(ventana, text="✅", font=("Arial", 60), bg="#e6f0fa", fg="#43a047")
    icono.pack(pady=(25, 5))
    # Mensaje destacado
    mensaje = tk.Label(ventana, text="¡Ejercicio completado con éxito!", font=("Arial", 18, "bold"), bg="#e6f0fa", fg="#1976d2")
    mensaje.pack(pady=(0, 10))
    # Botón cerrar
    boton = tk.Button(ventana, text="Aceptar", font=("Arial", 13, "bold"), bg="#43a047", fg="#fff", width=15, height=1, bd=0, relief="ridge", activebackground="#388e3c", activeforeground="#fff", command=ventana.destroy)
    boton.pack(pady=10)
    ventana.grab_set()

# --- Actividad: Abotonar camisa ---
def abotonar_camisa(paciente, ventana_padre):
    ventana = tk.Toplevel()
    ventana.title("Abotonar camisa")
    ventana.geometry("400x400")
    ventana.configure(bg=COLOR_FONDO)
    tk.Label(ventana, text="Simulación: Abotonar camisa", font=FONT_TITULO, bg=COLOR_FONDO, fg="#0d47a1").pack(pady=(20, 10))
    instrucciones = tk.Label(ventana, text="Haz clic en los botones en orden para abotonar la camisa.", font=FONT_NORMAL, bg=COLOR_FONDO)
    instrucciones.pack(pady=(0, 15))
    botones = []
    estado = {"actual": 0}
    def click_boton(idx):
        if idx == estado["actual"]:
            botones[idx]["bg"] = "#43a047"
            estado["actual"] += 1
            if estado["actual"] == 5:
                messagebox.showinfo("¡Éxito!", "¡Has abotonado la camisa!")
                registrar_resultado(paciente, "Abotonar camisa", True)
                ventana.destroy()
                ventana_padre.deiconify()
        else:
            messagebox.showwarning("Orden incorrecto", "Debes abotonar en orden de arriba a abajo.")
    for i in range(5):
        b = tk.Button(ventana, text=f"Botón {i+1}", font=("Arial", 14), width=15, height=2, bg="#bdbdbd", command=lambda idx=i: click_boton(idx))
        b.pack(pady=8)
        botones.append(b)
    ventana.protocol("WM_DELETE_WINDOW", lambda: [ventana.destroy(), ventana_padre.deiconify()])
    ventana.grab_set()

# --- Actividad: Arrastrar y soltar objeto ---
def arrastrar_objeto(paciente, ventana_padre):
    ventana = tk.Toplevel()
    ventana.title("Arrastrar y soltar objeto")
    ventana.geometry("500x400")
    ventana.configure(bg=COLOR_FONDO)
    tk.Label(ventana, text="Simulación: Arrastrar y soltar objeto", font=FONT_TITULO, bg=COLOR_FONDO, fg="#0d47a1").pack(pady=(20, 10))
    instrucciones = tk.Label(ventana, text="Arrastra la cuchara al círculo verde.", font=FONT_NORMAL, bg=COLOR_FONDO)
    instrucciones.pack(pady=(0, 10))
    canvas = tk.Canvas(ventana, width=400, height=250, bg="#fff", highlightthickness=0)
    canvas.pack(pady=10)
    # Zona objetivo
    objetivo = canvas.create_oval(320, 180, 380, 240, fill="#43a047", outline="")
    # Cuchara (rectángulo)
    cuchara = canvas.create_rectangle(30, 100, 110, 140, fill="#bdbdbd", outline="#757575")
    arrastrando = {"activo": False}
    def iniciar_arrastre(event):
        if canvas.find_withtag(tk.CURRENT)[0] == cuchara:
            arrastrando["activo"] = True
            arrastrando["x"] = event.x
            arrastrando["y"] = event.y
    def mover(event):
        if arrastrando["activo"]:
            dx = event.x - arrastrando["x"]
            dy = event.y - arrastrando["y"]
            canvas.move(cuchara, dx, dy)
            arrastrando["x"] = event.x
            arrastrando["y"] = event.y
    def soltar(event):
        arrastrando["activo"] = False
        # Verificar si la cuchara está dentro del objetivo
        coords_cuchara = canvas.coords(cuchara)
        coords_objetivo = canvas.coords(objetivo)
        centro_cuchara = ((coords_cuchara[0]+coords_cuchara[2])/2, (coords_cuchara[1]+coords_cuchara[3])/2)
        if (coords_objetivo[0] < centro_cuchara[0] < coords_objetivo[2]) and (coords_objetivo[1] < centro_cuchara[1] < coords_objetivo[3]):
            messagebox.showinfo("¡Éxito!", "¡Has colocado la cuchara correctamente!")
            registrar_resultado(paciente, "Arrastrar y soltar objeto", True)
            ventana.destroy()
            ventana_padre.deiconify()
    canvas.tag_bind(cuchara, "<ButtonPress-1>", iniciar_arrastre)
    canvas.tag_bind(cuchara, "<B1-Motion>", mover)
    canvas.tag_bind(cuchara, "<ButtonRelease-1>", soltar)
    ventana.protocol("WM_DELETE_WINDOW", lambda: [ventana.destroy(), ventana_padre.deiconify()])
    ventana.grab_set() 