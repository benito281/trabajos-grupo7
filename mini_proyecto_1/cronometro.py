import tkinter as tk
import time

class Cronometro:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.counter = 0
        self.start_time = 0

        # Label para mostrar el tiempo
        self.label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
        self.label.pack()

        # Botones del cronómetro
        self.start_button = tk.Button(root, text="Iniciar Cronómetro", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(root, text="Parar Cronómetro", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(root, text="Reiniciar Cronómetro", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.lap_button = tk.Button(root, text="Tiempo Parcial", command=self.lap)
        self.lap_button.pack(side=tk.LEFT, padx=10)

        self.lap_times = tk.Text(root, height=10, width=30)
        self.lap_times.pack(side=tk.BOTTOM, pady=10)

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.counter
            self.update_time()
            self.running = True

    def stop(self):
        if self.running:
            self.root.after_cancel(self.update)
            self.running = False

    def reset(self):
        if not self.running:
            self.counter = 0
            self.label.config(text="00:00:00")
            self.lap_times.delete(1.0, tk.END)

    def lap(self):
        if self.running:
            lap_time = time.strftime('%H:%M:%S', time.gmtime(self.counter))
            self.lap_times.insert(tk.END, f"Tiempo Parcial: {lap_time}\n")

    def update_time(self):
        self.counter = time.time() - self.start_time
        formatted_time = time.strftime('%H:%M:%S', time.gmtime(self.counter))
        self.label.config(text=formatted_time)
        self.update = self.root.after(1000, self.update_time)

class Temporizador:
    def __init__(self, root):
        self.root = root
        self.timer_running = False
        self.timer_counter = 0

        # Label para mostrar el tiempo
        self.label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
        self.label.pack()

        # Cuadro de entrada para el temporizador
        self.timer_label = tk.Label(root, text="Configurar Temporizador (HH:MM:SS):")
        self.timer_label.pack(pady=10)

        self.timer_entry = tk.Entry(root)
        self.timer_entry.pack()

        # Botones del temporizador
        self.set_timer_button = tk.Button(root, text="Establecer Temporizador", command=self.set_timer)
        self.set_timer_button.pack(side=tk.LEFT, padx=10)

        self.start_timer_button = tk.Button(root, text="Iniciar Temporizador", command=self.start)
        self.start_timer_button.pack(side=tk.LEFT, padx=10)

        self.stop_timer_button = tk.Button(root, text="Parar Temporizador", command=self.stop)
        self.stop_timer_button.pack(side=tk.LEFT, padx=10)

    def set_timer(self):
        timer_input = self.timer_entry.get()
        try:
            h, m, s = map(int, timer_input.split(":"))
            self.timer_counter = h * 3600 + m * 60 + s
            formatted_time = time.strftime('%H:%M:%S', time.gmtime(self.timer_counter))
            self.label.config(text=formatted_time)
        except ValueError:
            self.label.config(text="Formato Inválido")

    def start(self):
        if not self.timer_running and self.timer_counter > 0:
            self.timer_running = True
            self.update_timer()

    def stop(self):
        if self.timer_running:
            self.root.after_cancel(self.update_timer_id)
            self.timer_running = False

    def update_timer(self):
        if self.timer_counter > 0:
            self.timer_counter -= 1
            formatted_time = time.strftime('%H:%M:%S', time.gmtime(self.timer_counter))
            self.label.config(text=formatted_time)
            self.update_timer_id = self.root.after(1000, self.update_timer)
        else:
            self.label.config(text="¡Tiempo terminado!")
            self.timer_running = False

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Cronómetro y Temporizador")

        # Menú principal
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # Menú de selección de funcionalidad
        self.func_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Seleccionar", menu=self.func_menu)
        self.func_menu.add_command(label="Cronómetro", command=self.mostrar_cronometro)
        self.func_menu.add_command(label="Temporizador", command=self.mostrar_temporizador)

        # Inicializa con el cronómetro
        self.mostrar_cronometro()

    def mostrar_cronometro(self):
        self.limpiar_pantalla()
        Cronometro(self.root)

    def mostrar_temporizador(self):
        self.limpiar_pantalla()
        Temporizador(self.root)

    def limpiar_pantalla(self):
        # Eliminar todos los widgets de la pantalla, pero conservar el menú
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Menu):
                continue
            widget.destroy()

# Configuración de la ventana principal
root = tk.Tk()
app = Aplicacion(root)
root.mainloop()
