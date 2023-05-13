import tkinter as tk
import serial

class App(tk.Tk):
    def __init__(self, com_port):
        super().__init__()

        self.led_max_distance = 0

        self.serial_connection = serial.Serial(
            port=com_port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE
        )



        self.label = tk.Label(self, font=("Arial", 20), fg="blue")
        self.title("App Proj Elec")

        # Empêcher le redimensionnement de la fenêtre
        self.resizable(False, False)

        # Taille de la fenêtre
        self.geometry("350x125")

        # Texte dessus
        self.label_distance = tk.Label(self, text="Indiquez la distance voulue", font=("Arial", 13))
        self.label_distance.place(x=10, y=10, width=200, height=30)

        # Entry nombre
        self.entry = tk.Entry(self, font=("Arial", 13))
        self.valider_entree_cmd = self.register(self.valider_entree)
        self.entry.config(validate="key", validatecommand=(self.valider_entree_cmd, '%d', '%S'))
        self.entry.place(x=10, y=42.5, width=150, height=30)

        # Bouton
        self.button = tk.Button(self, text="Envoyer", font=("Arial", 13))
        self.button.place(x=170, y=40, width=80, height=30)
        self.button.config(command=self.send)

        # Texte du dessous
        self.distance_label = tk.Label(self, text="Vous êtes à une distance inconnue", font=("Arial", 13))
        self.distance_label.place(x=8, y=70, width=275, height=30)

        # Cercle rouge
        self.canvas = tk.Canvas(self)
        self.red_circle = self.canvas.create_oval(10, 10, 50, 50, fill="#FFC0CB")
        self.canvas.place(x=290, y=65, width=60, height=60)

        # Cercle vert
        self.canvas2 = tk.Canvas(self)
        self.green_circle = self.canvas2.create_oval(10, 10, 50, 50, fill="#BDFCC9")
        self.canvas2.place(x=290, y=10, width=60, height=60)

        #self.after(0, self.update_display)
        self.mainloop()

    def valider_entree(self, action, valeur_entree):
        # Vérifier si le texte entré est un nombre
        if action == "1":  # Inserer du texte
            if not valeur_entree.isdigit():
                return False
        return True

    def send(self, **kwargs):
        self.led_max_distance = int(self.entry.get())
        self.serial_connection.write(str.encode(str(self.led_max_distance) + "\r\n"))

    def read_serial(self):
        data = self.serial_connection.readline()
        try:
            return int(data.strip())
        except ValueError:
            return 0

    def update_display(self):
        data = self.read_serial()
        self.distance_label.config(text="Vous êtes à une distance de "+str(data)+" cm")
        self.update_led_display(data)
        self.after(100, self.update_display)

    def update_led_display(self, distance):
        if distance > self.led_max_distance:
            self.canvas.itemconfig(self.green_circle, fill="#BDFCC9")
            self.canvas.itemconfig(self.red_circle, fill="red")
        else:
            self.canvas.itemconfig(self.green_circle, fill="green")
            self.canvas.itemconfig(self.red_circle, fill="#FFC0CB")


if __name__ == "__main__":
    app = App('COM10')
    app.mainloop()
