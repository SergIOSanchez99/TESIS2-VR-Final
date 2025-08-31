import tkinter as tk
from tkinter import messagebox
from modules.usuarios import cargar_pacientes, guardar_pacientes
from modules.ejercicios import menu_ejercicios_grafico

COLOR_FONDO = "#e6f0fa"
COLOR_BOTON = "#1976d2"
COLOR_BOTON_TEXTO = "#ffffff"
FONT_TITULO = ("Arial", 22, "bold")
FONT_LOGO = ("Arial", 16, "italic")
FONT_NORMAL = ("Arial", 12)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Rehabilitación Motora")
        self.paciente = None
        self.root.configure(bg=COLOR_FONDO)
        self.menu_inicio()

    def menu_inicio(self):
        self.limpiar()
        logo = tk.Label(self.root, text="🦾 RehaVR", font=FONT_LOGO, bg=COLOR_FONDO, fg="#1976d2")
        logo.pack(pady=(20, 5))
        titulo = tk.Label(self.root, text="Sistema de Rehabilitación Motora", font=FONT_TITULO, bg=COLOR_FONDO, fg="#0d47a1")
        titulo.pack(pady=(0, 10))
        bienvenida = tk.Label(self.root, text="Bienvenido/a. Por favor, regístrese o inicie sesión para comenzar.", font=FONT_NORMAL, bg=COLOR_FONDO)
        bienvenida.pack(pady=(0, 20))
        self.boton_grande("Registrarse", self.registro).pack(pady=8)
        self.boton_grande("Iniciar sesión", self.login).pack(pady=8)
        self.boton_grande("Salir", self.root.quit).pack(pady=8)

    def registro(self):
        self.limpiar()
        tk.Label(self.root, text="Registro de Paciente", font=FONT_TITULO, bg=COLOR_FONDO, fg="#0d47a1").pack(pady=(30, 10))
        tk.Label(self.root, text="Nombre:", font=FONT_NORMAL, bg=COLOR_FONDO).pack()
        nombre = tk.Entry(self.root, font=FONT_NORMAL)
        nombre.pack(pady=3)
        tk.Label(self.root, text="Edad:", font=FONT_NORMAL, bg=COLOR_FONDO).pack()
        edad = tk.Entry(self.root, font=FONT_NORMAL)
        edad.pack(pady=3)
        def registrar():
            n = nombre.get().strip()
            e = edad.get().strip()
            if not n or not e:
                messagebox.showerror("Error", "Completa todos los campos.")
                return
            pacientes = cargar_pacientes()
            for p in pacientes:
                if p["nombre"].lower() == n.lower() and p["edad"] == e:
                    messagebox.showerror("Error", "Ya existe un paciente con ese nombre y edad.")
                    return
            paciente = {"nombre": n, "edad": e}
            pacientes.append(paciente)
            guardar_pacientes(pacientes)
            self.paciente = paciente
            messagebox.showinfo("Éxito", "Registro exitoso.")
            self.menu_ejercicios()
        self.boton_grande("Registrar", registrar).pack(pady=12)
        self.boton_grande("Volver", self.menu_inicio).pack(pady=3)

    def login(self):
        self.limpiar()
        tk.Label(self.root, text="Inicio de Sesión", font=FONT_TITULO, bg=COLOR_FONDO, fg="#0d47a1").pack(pady=(30, 10))
        tk.Label(self.root, text="Nombre:", font=FONT_NORMAL, bg=COLOR_FONDO).pack()
        nombre = tk.Entry(self.root, font=FONT_NORMAL)
        nombre.pack(pady=3)
        tk.Label(self.root, text="Edad:", font=FONT_NORMAL, bg=COLOR_FONDO).pack()
        edad = tk.Entry(self.root, font=FONT_NORMAL)
        edad.pack(pady=3)
        def iniciar():
            n = nombre.get().strip()
            e = edad.get().strip()
            pacientes = cargar_pacientes()
            for p in pacientes:
                if p["nombre"].lower() == n.lower() and p["edad"] == e:
                    self.paciente = p
                    messagebox.showinfo("Éxito", f"Bienvenido/a, {n}!")
                    self.menu_ejercicios()
                    return
            messagebox.showerror("Error", "Paciente no encontrado.")
        self.boton_grande("Iniciar sesión", iniciar).pack(pady=12)
        self.boton_grande("Volver", self.menu_inicio).pack(pady=3)

    def menu_ejercicios(self):
        self.limpiar()
        menu_ejercicios_grafico(self.root, self.paciente, self.menu_inicio)

    def limpiar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def boton_grande(self, texto, comando):
        return tk.Button(self.root, text=texto, font=("Arial", 14, "bold"), bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, width=20, height=2, bd=0, relief="ridge", activebackground="#1565c0", activeforeground=COLOR_BOTON_TEXTO, command=comando)

def main():
    root = tk.Tk()
    root.geometry("500x500")
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main() 