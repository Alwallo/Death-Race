from tkinter import *
import winsound
import threading
import csv
import json
from juego import *


class VentanaPrincipal():
    # Definimos el constructor de la clase principal
    def __init__(self):
        pass

    # Definimos la funcion que se encarga de crear la ventana
    def Crear(self):
        self.name = "player"
        self.isClosed = False
        self.main = Tk()  # Iniciamos la ventana con la variable "main"
        self.main.config(width=900, height=600, bg="black")  # Damos las dimensiones de la misma
        self.main.overrideredirect(True)  # Le quitamos los bordes y la barra superior
        self.main.wm_state("zoomed")

        # Centrar la ventana en la pantalla
        self.CentrarPantalla(self.main)

        # Creamos un contenedor de widgets
        inicio = PhotoImage(file="Imagenes/imagenPrincipal.png")
        self.canvasFondo = Canvas(self.main, width = 1400, height = 1000, bg = "black")
        self.canvasFondo.pack()
        self.canvasFondo.create_image((690, 350), image = inicio)

        # Inicio de creacion de botones, etiquetas

        exit = PhotoImage(file="Imagenes/exit.png")
        btn_exit = (Button(self.canvasFondo, image = exit, width = 40, height = 40,
                          cursor="hand2", relief=FLAT, command=lambda: CerrarV()))
        btn_exit.place(x = 10, y = 7)

        startG = PhotoImage(file="Imagenes/play.png")
        btn_start = (Button(self.canvasFondo, image=startG, width=250, height=70,
                            cursor="hand2", relief=FLAT, command=lambda: CrearUsuario()))
        btn_start.place(x = 1050, y = 640)

        estad = PhotoImage(file="Imagenes/estad.png")
        btn_estadisticas = (Button(self.canvasFondo, width=40, height=35, cursor="hand2",
                                   image=estad, relief=FLAT, command=lambda: Estadisticas()))
        btn_estadisticas.place(x=10, y=60)

        # Reproducimos el sonido de inicio siempre que la ventana principal este activa
        def ReproducirSonido():
            while (not self.isClosed):
                winsound.PlaySound("sonidos/musicaFondo.wav", winsound.SND_FILENAME)

        repro = threading.Thread(target=ReproducirSonido)  # Ponemos en segundo plano el sonido
        repro.start()  # Iniciamos el hilo

        # Destruimos la ventana principal al presionar "btn_exit"
        def CerrarV():
            self.isClosed = True  # Con esto paramos el bucle del hilo
            self.main.destroy()

        def Estadisticas():
            self.CrearVentanaEstadisticas()

        def CrearUsuario():
            self.Usuario()

        self.main.mainloop()

    # Crea la ventana de estadisticas
    def CrearVentanaEstadisticas(self):
        self.states = Toplevel()
        self.states.overrideredirect(True)
        self.frameState = Frame(self.states)
        self.frameState.pack(expand=1)
        self.frameState.config(width=600, height=500, bg="gray")
        self.states.config(width=600, height=500, bg="gray")

        # Centrar la ventana en la pantalla
        self.CentrarPantalla(self.states)

        self.home = PhotoImage(file="Imagenes/Home.png")
        btn_home = Button(self.states, image=self.home, width=45, height=45,
                          bg="gray", command=lambda: self.states.state("withdraw"))
        btn_home.place(x=10, y=10)

        # Creamos etiquetas para jugador y puntuacion
        Label(self.frameState, font=("Space Invaders", 16), bg="black", text="Jugador",
              width=15, height=1, fg="blue").place(x=60, y=90)
        Label(self.frameState, font=("Space Invaders", 16), bg="black", text="Puntuacion",
              width=15, height=1, fg="blue").place(x=300, y=90)

        # Creamos las listboxs para escribir los jugadores y su puntuacion
        self.leaderboard = (Listbox(self.frameState, font=("Space Invaders", 16), bg="black",
                                    width=15, height=10, fg="white"))
        self.leaderboard.place(x=60, y=130)
        self.leaderboard2 = (Listbox(self.frameState, font=("Space Invaders", 16), bg="black",
                                     width=15, height=10, fg="white"))
        self.leaderboard2.place(x=300, y=130)

        # Creamos la lista de diccionarios
        datos = {}
        datos["lider"] = []
        lista = []
        # Abrimos el archivo csv para escribir cada columna de la puntuacion alta en una lista
        with open("statsPlayer.csv", newline='') as File:
            reader = csv.reader(File)
            for row in reader:
                if len(row) > 0 and row[0] != "":
                    lista += [(int(row[1]))]
        # Ordenamos esa lista de nemor a mayor y la invertimos para obtener la puntuacion mas alta
        lista.sort()
        lista.reverse()

        # Abrimos el archivo, leemos el jugador y la puntuacion  y lo ingresamos en una lista
        puntos = []
        with open("statsPlayer.csv", newline='') as File:
            reader = csv.reader(File)
            for row in reader:
                if len(row) > 0:
                    if row[0] != "":
                        puntos.append([row[0], row[1]])

        # Recorremos la lista ordenada y la lista desordenada para guardar en una lista de diccionarios la puntuacion mas alta
        for lis in lista:
            for row in puntos:
                if len(row) > 0:
                    if int(row[1]) == lis:
                        datos["lider"].append({"Jugador": row[0], "Puntuacion": row[1]})

        # Abrimos el archivo con JSON y escribimos el diccionario
        with open("leader", 'w') as file:
            json.dump(datos["lider"], file)

        # Escribimos en las listbox los primeros 5 jugadores con puntuacion alta
        with open("leader") as lider:
            high = json.load(lider)
            contador = 0
            for h in high:
                if contador < 5:
                    self.leaderboard.insert(END, h["Jugador"])
                    self.leaderboard2.insert(END, h["Puntuacion"])
                contador = contador + 1


    # Creamos la ventana para ingresar un usuario
    def Usuario(self):
        self.user = Toplevel()
        self.user.overrideredirect(True)
        self.user.config(width=300, height=100, bg="gray")
        self.frameUser = Frame(self.user)
        self.frameUser.pack(expand=1)
        self.frameUser.config(width=300, height=100, bg="gray")

        # Centrar la ventana en la pantalla
        self.CentrarPantalla(self.user)

        lbl_nombre = (Label(self.frameUser, bg="gray", fg="black", font=("Space Invaders", 12),
                            text="Introduce tu nombre: ", width=200, height=20)).pack()
        self.text_nombre = (Entry(self.frameUser, bg="white", fg="blue", font=("Space Invaders", 12),
                                  width=22))
        self.text_nombre.place(x=15, y=60)
        self.text_nombre.bind("<Return>", self.keyboard)


    # Si se presiona "Enter" en la ventana usuario, se realiza este evento
    def keyboard(self, event):
        self.name = self.text_nombre.get()
        self.puntos = 0
        self.puntosAltos = 0
        self.Nuevo = True
        self.indice = 0
        # Abrimos un archivo csv de lectura y si el usuario es nuevo le ponemos de puntuacion 0
        with open("statsPlayer.csv", newline='') as File:
            reader = csv.reader(File)
            for row in reader:
                if len(row) > 0:
                    if self.name == row[0]:
                        self.Nuevo = False
                        self.indice = row[1]
            if (self.Nuevo):
                with open("statsPlayer.csv", "a") as archivocsv:
                    userpoint = [self.name, self.puntosAltos, self.puntos]
                    usernam = csv.writer(archivocsv, delimiter=",", lineterminator="\n")
                    usernam.writerow(userpoint)
            else:
                self.puntos = self.indice
        self.user.state("withdraw")
        self.CrearVentanaJuego(self.name)

    def CrearVentanaJuego(self, name):
        self.main.destroy()
        self.isClosed = True
        # Creamos la instancia de la superclase "Nuevo Juego"
        n = NuevoJuego(2, 1, 5, name, 1)
        n.CrearVentana()


    # Funcion para centrar las ventanas en la pantalla
    def CentrarPantalla(self, root):
        root.update_idletasks()
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = (h / 2 - size[1] / 2) - 10
        root.geometry("%dx%d+%d+%d" % (size + (x, y)))


if __name__ == "__main__":
    # Creamos la instancia de la clase principal
    nuevo = VentanaPrincipal()
    nuevo.Crear()
