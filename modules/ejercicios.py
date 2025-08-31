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
    pygame.init()
    ancho, alto = 800, 600
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption(f"Ejercicio de Rehabilitación - Nivel {nivel}")
    reloj = pygame.time.Clock()

    # Colores
    BLANCO = (255, 255, 255)
    AZUL = (0, 0, 255)
    ROJO = (255, 0, 0)
    VERDE = (0, 200, 0)

    # Mano virtual
    mano_size = 50
    mano_x, mano_y = ancho // 2, alto // 2
    velocidad = 10

    # Objetivo
    objetivo_size = 60
    objetivo_x = random.randint(0, ancho - objetivo_size)
    objetivo_y = random.randint(0, alto - objetivo_size)
    objetivo_dx, objetivo_dy = 0, 0
    if nivel == 2:
        objetivo_dx = 3
        objetivo_dy = 2
    elif nivel == 3:
        objetivo_dx = 7
        objetivo_dy = 5

    tocado = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            mano_x -= velocidad
        if teclas[pygame.K_RIGHT]:
            mano_x += velocidad
        if teclas[pygame.K_UP]:
            mano_y -= velocidad
        if teclas[pygame.K_DOWN]:
            mano_y += velocidad
        # Limitar a la pantalla
        mano_x = max(0, min(ancho - mano_size, mano_x))
        mano_y = max(0, min(alto - mano_size, mano_y))
        # Mover objetivo si corresponde
        if nivel > 1:
            objetivo_x += objetivo_dx
            objetivo_y += objetivo_dy
            if objetivo_x <= 0 or objetivo_x >= ancho - objetivo_size:
                objetivo_dx *= -1
            if objetivo_y <= 0 or objetivo_y >= alto - objetivo_size:
                objetivo_dy *= -1
        # Detección de colisión
        mano_rect = pygame.Rect(mano_x, mano_y, mano_size, mano_size)
        objetivo_rect = pygame.Rect(objetivo_x, objetivo_y, objetivo_size, objetivo_size)
        if mano_rect.colliderect(objetivo_rect):
            tocado = True
        # Dibujar
        pantalla.fill(BLANCO)
        pygame.draw.rect(pantalla, AZUL, mano_rect)
        pygame.draw.ellipse(pantalla, ROJO, objetivo_rect)
        if tocado:
            font = pygame.font.SysFont(None, 60)
            texto = font.render("¡Objetivo alcanzado!", True, VERDE)
            pantalla.blit(texto, (ancho//2 - 200, alto//2 - 30))
            pygame.display.flip()
            pygame.time.wait(2000)
            break
        pygame.display.flip()
        reloj.tick(30)
    pygame.quit()
    mostrar_ventana_exito()
    return True

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