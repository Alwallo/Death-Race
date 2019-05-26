import pygame, sys
from pygame.locals import *
import os
import random
import csv
from cliente import *

pygame.init()


# clase principal del juego
class NuevoJuego(object):
    # parametros que recibe la clase NuevoJueo
    def __init__(self, velEnemy, rangoDisparo, velocidadDisparo, username, nivel, aceleracion):
        self.rangoDisparo = rangoDisparo
        self.velocidadDisparo = velocidadDisparo
        self.velEnemy = velEnemy
        self.puntos = 0
        self.puntuacionAlta = 0
        self.username = username
        self.nivel = nivel
        self.aceleracion = aceleracion

    # funcion para guardar las puntuaciones de los jugadores
    def SaveScores(self, sc, hs, user):
        self.user = user
        self.sc = sc
        self.hs = hs
        self.lista = []
        with open("statsPlayer.csv", newline='') as File:
            reader = csv.reader(File)
            self.lista.append([self.user, self.hs, self.sc])
            for row in reader:
                if len(row) > 0:
                    if self.user != row[0]:
                        self.lista.append(row)
        writer = csv.writer(open('statsPlayer.csv', 'w'), delimiter=",")
        writer.writerows(self.lista)

    # funcion para cargar los puntajes más altos de los jugadores
    def LoadScores(self, user):
        self.user = user
        with open("statsPlayer.csv", newline='') as File:
            reader = csv.reader(File)
            for row in reader:
                if len(row) > 0:
                    if self.user == row[0]:
                        self.puntuacionAlta = int(row[1])
                        self.puntos = int(row[2])
                        if self.nivel == 1:
                            self.puntos = 0
                        else:
                            self.puntos = int(row[2])
                            # clase para la nave defensora

    class playerCar(pygame.sprite.Sprite):
        def __init__(self, x, y, ruta):
            pygame.sprite.Sprite.__init__(self)
            # se carga la imagen de la nave
            self.ruta = ruta
            self.imagenCar = pygame.image.load("Imagenes/buggie1.png")
            # se obtiene el rectanulo de la nave y su centro
            self.rectCar = self.imagenCar.get_rect()
            self.rectCar.centerx = x
            self.rectCar.centery = y
            # velocidad a la que se mueve la nave
            self.velocidad = 5
            # lista para controlar los disparos de la nave
            self.listaDisparo = []
            # se valida la vida de la nave
            self.vida = True
            # se carga el sonido para cada disparo de la nave
            self.sonidoOn = pygame.mixer.Sound("sonidos/aceleracionCont1.wav")
            self.sonidoAcel = pygame.mixer.Sound("sonidos/aceleracion_1.wav")
            self.sonidoDisparo = pygame.mixer.Sound("sonidos/disparo.wav")
            self.sonidoFrenado = pygame.mixer.Sound("sonidos/frenado.wav")
            self.posicionx = x
            self.posiciony = y
            self.vida = 100

        def setRuta(self, ruta):
            self.ruta = ruta
            if ruta == 0:
                self.imagenCar = pygame.image.load("Imagenes/buggie1.png")
            elif ruta == 1:
                self.imagenCar = pygame.image.load("Imagenes/buggie1.1.png")
            else:
                self.imagenCar = pygame.image.load("Imagenes/buggie1.2.png")
        # -------------------------------------------------------------------------------------------------------

    class FondoPant(pygame.sprite.Sprite):
        def __init__(self):
            self.imgFondo = pygame.image.load("Imagenes/desierto fondo.jpg").convert_alpha()
            self.rectFondo = self.imgFondo.get_rect()

        # def dibujar(self, superficie):--------------------------------
        def update(self, ventana, velocidadx, velocidady):
            self.rectFondo.move_ip(-velocidadx, +velocidady)
            ventana.blit(self.imgFondo, self.rectFondo)

            # ------------------------------------------------------------------------------------------------------

    # función para los disparos de la nave y los aliens
    class proyectil(pygame.sprite.Sprite):
        def __init__(self, posx, posy, ruta, velocidadDisparo):
            pygame.sprite.Sprite.__init__(self)
            # se carga la imagen del proyectil
            self.imagenProyectil = pygame.image.load(ruta)
            self.ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            # se obtiene el rectangulo de la imagen del proyectil
            self.rect = self.imagenProyectil.get_rect()
            # definicion de variable para velocidad de disparo
            self.velocidadDisparo = velocidadDisparo
            # se obtienen las posiciones en (x,y) de la imagen del proyectil
            self.rect.top = posy
            self.rect.left = posx
            # superficie donde se dibuja la imagen del proyectil
            self.superficie = self.ventana

        # funcion define la trayectoria de los proyectiles de la nave y enemigos
        def trayectoria(self):
            # si es True, el disparo es de la nave espacial, de lo contrario es de un enemigo
            self.rect.top = self.rect.top - self.velocidadDisparo

        # funcion dibuja el disparo o proyectil en la ventana
        def dibujarDisparo(self, superficie):
            self.superficie.blit(self.imagenProyectil, self.rect)
            # clase para los enemigos

    class obstaculos(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            # cargar imagenes de diferentes obstaculos
            self.obstaculo1 = pygame.image.load("Imagenes/arbol1.png")
            self.rectObs1 = self.obstaculo1.get_rect()
            self.obstaculo2 = pygame.image.load("Imagenes/arboles.png")
            self.rectObs2 = self.obstaculo2.get_rect()
            self.obstaculo3 = pygame.image.load("Imagenes/arboles (1).png")
            self.rectObs3 = self.obstaculo3.get_rect()
            self.obstaculo4 = pygame.image.load("Imagenes/arboles (2).png")
            self.rectObs4 = self.obstaculo4.get_rect()
            self.obstaculo5 = pygame.image.load("Imagenes/arboles (3).png")
            self.rectObs5 = self.obstaculo5.get_rect()
            self.obstaculo6 = pygame.image.load("Imagenes/arboles (4).png")
            self.rectObs6 = self.obstaculo6.get_rect()
            self.obstaculo7 = pygame.image.load("Imagenes/roca2.png")
            self.rectObs7 = self.obstaculo7.get_rect()
            self.obstaculo8 = pygame.image.load("Imagenes/mina.png")
            self.rectObs8 = self.obstaculo8.get_rect()
            self.obstaculo9 = pygame.image.load("Imagenes/corazonVida.png")
            self.rectObs9 = self.obstaculo9.get_rect()
            self.obstaculo10 = pygame.image.load("Imagenes/banderaSalida.jpg")
            self.rectObs10 = self.obstaculo10.get_rect()

            self.listaObjetos = []
            self.posObjx = 0
            self.posObjy = 0
            self.listaDeObjetos()

        # funcion para controlar la lista de los enemigos.
        def listaDeObjetos(self):
            for numObj in range(100):
                self.posObjx = random.randint(-4000, 4000)
                self.posObjy = random.randint(-5000, 5000)
                self.rectObs1.left = self.posObjx
                self.rectObs1.top = self.posObjy
                self.rectObs1 = self.obstaculo1.get_rect()
                self.pos1 = [self.obstaculo1, self.rectObs1, self.posObjx, self.posObjy, True]
                self.listaObjetos.append(self.pos1)

            for numObj in range(100):
                self.posObjx = random.randint(-4000, 4000)
                self.posObjy = random.randint(-5000, 5000)
                self.rectObs2.left = self.posObjx
                self.rectObs2.top = self.posObjy
                self.rectObs2 = self.obstaculo2.get_rect()
                self.pos2 = [self.obstaculo2, self.rectObs2, self.posObjx, self.posObjy, True]
                self.listaObjetos.append(self.pos2)

            for numObj in range(100):
                self.posObjx = random.randint(-4000, 4000)
                self.posObjy = random.randint(-5000, 5000)
                self.rectObs3.left = self.posObjx
                self.rectObs3.top = self.posObjy
                self.rectObs3 = self.obstaculo3.get_rect()
                self.pos3 = [self.obstaculo3, self.rectObs3, self.posObjx, self.posObjy, True]
                self.listaObjetos.append(self.pos3)

            for numObj in range(100):
                self.posObjx = random.randint(-4000, 4000)
                self.posObjy = random.randint(-5000, 5000)
                self.rectObs4.left = self.posObjx
                self.rectObs4.top = self.posObjy
                self.rectObs4 = self.obstaculo4.get_rect()
                self.pos4 = [self.obstaculo4, self.rectObs4, self.posObjx, self.posObjy, True]
                self.listaObjetos.append(self.pos4)

            for numObj in range(100):
                self.posObjx = random.randint(-4000, 4000)
                self.posObjy = random.randint(-5000, 5000)
                self.rectObs5.left = self.posObjx
                self.rectObs5.top = self.posObjy
                self.rectObs5 = self.obstaculo5.get_rect()
                self.pos5 = [self.obstaculo5, self.rectObs5, self.posObjx, self.posObjy, True]
                self.listaObjetos.append(self.pos5)

            for numObj in range(100):
                self.posObjx = random.randint(-4000, 4000)
                self.posObjy = random.randint(-5000, 5000)
                self.rectObs6.left = self.posObjx
                self.rectObs6.top = self.posObjy
                self.rectObs6 = self.obstaculo6.get_rect()
                self.pos6 = [self.obstaculo6, self.rectObs6, self.posObjx, self.posObjy, True]
                self.listaObjetos.append(self.pos6)

            for numObj in range(100):
                self.posObjx = random.randint(-4000, 4000)
                self.posObjy = random.randint(-5000, 5000)
                self.rectObs7.left = self.posObjx
                self.rectObs7.top = self.posObjy
                self.rectObs7 = self.obstaculo7.get_rect()
                self.pos7 = [self.obstaculo7, self.rectObs7, self.posObjx, self.posObjy, True]
                self.listaObjetos.append(self.pos7)

            for numObj in range(100):
                self.posObjx = random.randint(-4000, 4000)
                self.posObjy = random.randint(-5000, 5000)
                self.rectObs8.left = self.posObjx
                self.rectObs8.top = self.posObjy
                self.rectObs8 = self.obstaculo8.get_rect()
                self.pos8 = [self.obstaculo8, self.rectObs8, self.posObjx, self.posObjy, True]
                self.listaObjetos.append(self.pos8)

            for numObj in range(10):
                self.posObjx = random.randint(-4000, 4000)
                self.posObjy = random.randint(-5000, 5000)
                self.rectObs9.left = self.posObjx
                self.rectObs9.top = self.posObjy
                self.rectObs9 = self.obstaculo9.get_rect()
                self.pos9 = [self.obstaculo9, self.rectObs9, self.posObjx, self.posObjy, True]
                self.listaObjetos.append(self.pos9)


        # funcion para dibujar enemigos en la ventana. controlado por matriz
        def dibujar(self, superficie):
            for i in range(810):
                if self.listaObjetos[i][4]:
                    self.listaObjetos[i][1].left = self.listaObjetos[i][2]
                    self.listaObjetos[i][1].top = self.listaObjetos[i][3]
                    superficie.blit(self.listaObjetos[i][0], self.listaObjetos[i][1])

    class enemigo(pygame.sprite.Sprite):
        def __init__(self, rangoDisparo):
            pygame.sprite.Sprite.__init__(self)
            # cargar imagenes de los enemigos y sus explosiones
            self.CarEnemy = pygame.image.load("Imagenes/buggie2.png")
            self.RectEnemigo = self.CarEnemy.get_rect()

            # variables para los enemigos
            self.listaDisparo = []
            self.listaEnemigo = []
            self.listaExplosion = []
            self.listaDeEnemigos()

        def listaDeEnemigos(self):
            for i in range(10):
                self.EnemigoX = random.randint(-1250, 1250)
                self.EnemigoY = random.randint(0, 1000)
                self.RectEnemigo.left = self.EnemigoX
                self.RectEnemigo.top = self.EnemigoY
                self.RectEnemigo = self.CarEnemy.get_rect()
                self.Enemigos = [self.CarEnemy, self.RectEnemigo, self.EnemigoX, self.EnemigoY, True, 100]
                self.listaEnemigo.append(self.Enemigos)

        # funcion para dibujar enemigos en la ventana. controlado por matriz
        def dibujar(self, superficie):
            for i in range(10):
                self.invasor = self.listaEnemigo[i][0]
                self.invasorRect = self.listaEnemigo[i][1]
                self.invasorX = self.listaEnemigo[i][2]
                self.invasorY = self.listaEnemigo[i][3]
                self.listaEnemigo[i][1].top = self.invasorY
                self.listaEnemigo[i][1].left = self.invasorX
                # condicion para controlar si se eliminan o no los enemigos
                if self.listaEnemigo[i][4]:
                    superficie.blit(self.invasor, (self.invasorX, self.invasorY))

    # funcion para el disparo de los enemigos
    def disparoEnemy(self, Enemigo):
        for i in range(10):
            if Enemigo.listaEnemigo[i][4]:
                # se usan numeros aleatorios para que los enemigos no disparen al mismo tiempo, sino tratar de que sea uno por uno
                if (random.randint(0, 100) < self.rangoDisparo):
                    h, k = Enemigo.listaEnemigo[i][1].center
                    # dibujar proyectil enemigo
                    proyectilEnemigo = self.proyectil(h, k, "Imagenes/proyectil.png", self.velocidadDisparo)
                    Enemigo.listaDisparo.append(proyectilEnemigo)

    # funcion para el mensaje de felicitación al completar el juego
    def congrats(self):
        # se carga imagen del mensaje
        ventFel = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        fondoFel = pygame.image.load("Imagenes/EndScreen.jpg")
        # se dibuja en ventana
        while True:
            ventFel.blit(fondoFel, (0, 0))

    # funcion principal de ejecucion del juego
    def CrearVentana(self):
        # se crea la ventana del juego (dimensiones)
        ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.mixer.music.load("sonidos/explosion.wav")

        # tipo de fuente para el juego y mensajes a imprimir
        font = pygame.font.match_font("Fabian ")
        score = pygame.font.Font.render((pygame.font.Font(font, 30)), "SCORE:", 0, (0, 0, 0))
        hscore = pygame.font.Font.render((pygame.font.Font(font, 30)), "HI-SCORE:", 0, (0, 0, 0))
        Nombre_Jugador = pygame.font.Font.render((pygame.font.Font(font, 20)), str.upper(self.username), 0, (139, 0, 0))
        nivel = pygame.font.Font.render((pygame.font.Font(font, 30)), "LEVEL:", 0, (0, 0, 0))
        life = pygame.font.Font.render((pygame.font.Font(font, 30)), "LIFE:", 0, (0, 0, 0))

        bandSalida = pygame.image.load("Imagenes/meta.png")
        rectSalida = bandSalida.get_rect()
        rectSalida.left = random.randint(0, 800)
        rectSalida.top = -4000
        # llamada a la funcion LoadScores para cargar puntajes de jugadores
        self.LoadScores(self.username)

        # variables para la ejecucion del juego
        net = Network()
        jugador = self.playerCar(696, 452, 0)
        jugador2 = self.playerCar(550, 452, 0)
        Enemigo = self.enemigo(self.rangoDisparo)
        detener = True
        enJuego = True
        movimientoEnemigo = True

        Fondo1 = self.FondoPant()
        velx = 0
        vely = 0
        posiciones = []
        obstacle = self.obstaculos()
        segundos = 0
        minutos = 0
        posObjeto = []
        posEnemigo = []
        # ciclo de ejecución
        while True:
            Fondo1.update(ventana, velx, vely)
            ventana.blit(bandSalida, (rectSalida.left, rectSalida.top))
            obstacle.dibujar(ventana)
            Enemigo.dibujar(ventana)
            for t in range(810):
                obstaculox = obstacle.listaObjetos[t][2]
                obstaculoy = obstacle.listaObjetos[t][3]
                obstaculoVisible = obstacle.listaObjetos[t][4]
                posObjeto.append([obstaculox,obstaculoy,obstaculoVisible])
            for u in range(10):
                Enemigox = Enemigo.listaEnemigo[u][2]
                Enemigoy = Enemigo.listaEnemigo[u][3]
                EnemigoVisible = Enemigo.listaEnemigo[u][4]
                posEnemigo.append([Enemigox, Enemigoy, EnemigoVisible])

            posiciones = [jugador.posicionx, jugador.posiciony,jugador2.rectCar.left, jugador2.rectCar.top, posObjeto, posEnemigo]

            tiempo = pygame.time.get_ticks() // 1000
            if segundos > 59:
                segundos = 0
                minutos = tiempo // 60
            else:
                segundos = tiempo - (minutos * 60)

            if segundos < 10:
                contar = pygame.font.Font.render((pygame.font.Font(font, 30)),
                                                 "TIEMPO :  " + str(minutos) + ":0" + str(segundos), 0, (0, 0, 0))
            else:
                contar = pygame.font.Font.render((pygame.font.Font(font, 30)),
                                                 "TIEMPO :  " + str(minutos) + ":" + str(segundos), 0, (0, 0, 0))
            numeroNivel = pygame.font.Font.render((pygame.font.Font(font, 30)), str(self.nivel), 0, (0, 0, 139))

            # se imprime el texto en la ventana#######################################
            ventana.blit(score, (20, 0))
            ventana.blit(hscore, (1000, 0))
            ventana.blit(nivel, (550, 0))
            ventana.blit(numeroNivel, (650, 0))
            ventana.blit(contar, (20, 50))
            ventana.blit(Nombre_Jugador, (jugador.rectCar.left - 8, jugador.rectCar.top - 20))
            scor = pygame.font.Font.render((pygame.font.Font(font, 30)), str(self.puntos), 0, (0, 0, 139))
            ventana.blit(scor, (110, 0))
            ventana.blit(life, (1000, 50))

            if self.puntos >= self.puntuacionAlta:
                hscor = pygame.font.Font.render((pygame.font.Font(font, 30)), str(self.puntos), 0, (0, 0, 139))
                self.SaveScores(self.puntos, self.puntos, self.username)
            else:
                hscor = pygame.font.Font.render((pygame.font.Font(font, 30)), str(self.puntuacionAlta), 0,  (0, 0, 139))
                self.SaveScores(self.puntos, self.puntuacionAlta, self.username)
            # imprimir puntaje mas alto
            ventana.blit(hscor,(1200, 0))

            otroJugador = net.send([jugador.posicionx, jugador.posiciony, jugador.ruta, jugador.vida])
            jugador2.setRuta(otroJugador[2])
            jugador2.rectCar.left = otroJugador[1]
            jugador2.rectCar.top = otroJugador[0]
            jugador2.vida = otroJugador[3]
            if jugador2.vida > 0:
                ventana.blit(jugador2.imagenCar, jugador2.rectCar)

            # ciclo para cerrar los modulos de pygame al salir del juego
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Movimiento del carrito
            if enJuego == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_s:
                        pygame.quit()
                        sys.exit()

                    elif event.key == K_g:

                        with open("savegame", "wb") as f:
                            pickle.dump(posiciones, f)

                    elif event.key == K_r:
                        with open("savegame", "rb") as f:
                            posiciones = pickle.load(f)
                            posiciones[0] = jugador.posicionx
                            posiciones[1] = jugador.posiciony
                            posiciones[2] = jugador2.rectCar.left
                            posiciones[3] = jugador2.rectCar.top
                            posiciones[4] = posObjeto
                            posiciones[5] = posEnemigo
                            for t in range(810):
                                obstacle.listaObjetos[t][2] = posObjeto[t][0]
                                obstacle.listaObjetos[t][3] = posObjeto[t][1]
                                obstacle.listaObjetos[t][4] = posObjeto[t][2]
                            for u in range(10):
                                Enemigo.listaEnemigo[u][2] = posEnemigo[u][0]
                                Enemigo.listaEnemigo[u][3] = posEnemigo[u][1]
                                Enemigo.listaEnemigo[u][4] = posEnemigo[u][2]

                    elif event.key == K_LEFT:
                        jugador.sonidoFrenado.stop()
                        jugador.posiciony -= velx
                        rectSalida.left -= velx
                        if jugador.rectCar.colliderect(jugador2.rectCar):
                            velx = 0
                            vely = 0
                            jugador2.rectCar.right -= 200
                        else:
                            velx = self.aceleracion * -5
                            vely = 0
                            self.aceleracion += 0.01
                            for lista in range(810):
                                obstacle.listaObjetos[lista][2] -= velx
                            for enem in range(10):
                                Enemigo.listaEnemigo[enem][2] -= velx
                        #Empujar Enemigos
                        for i in range(10):
                            if jugador.rectCar.colliderect(Enemigo.listaEnemigo[i][1]):
                                Enemigo.listaEnemigo[i][2] -= 50

                        jugador.setRuta(2)
                        ventana.blit(jugador.imagenCar, jugador.rectCar)
                        jugador.sonidoOn.stop()
                        jugador.sonidoAcel.play(1000)
                        if Fondo1.rectFondo.left > 0:
                            Fondo1.rectFondo.left = -2600
                    elif event.key == K_RIGHT:
                        jugador.sonidoFrenado.stop()
                        jugador.posiciony += velx
                        rectSalida.left -= velx
                        if jugador.rectCar.colliderect(jugador2.rectCar):
                            velx = 0
                            vely = 0
                            jugador2.rectCar.left += 200
                        else:
                            velx = self.aceleracion * 5
                            vely = 0
                            self.aceleracion += 0.01
                            for lista in range(810):
                                obstacle.listaObjetos[lista][2] -= velx
                            for enem in range(10):
                                Enemigo.listaEnemigo[enem][2] -= velx
                        #Empujar Enemigos
                            for i in range(10):
                                if jugador.rectCar.colliderect(Enemigo.listaEnemigo[i][1]):
                                    Enemigo.listaEnemigo[i][2] += 50
                        jugador.setRuta(1)
                        ventana.blit(jugador.imagenCar, jugador.rectCar)
                        jugador.sonidoOn.stop()
                        jugador.sonidoAcel.play(1000)
                        if Fondo1.rectFondo.right < 2600:
                            Fondo1.rectFondo.right = 4000
                    elif event.key == K_UP:
                        jugador.sonidoFrenado.stop()
                        jugador.posicionx -= velx
                        rectSalida.top += vely
                        if jugador.rectCar.colliderect(jugador2.rectCar):
                            velx = 0
                            vely = 0
                            jugador2.rectCar.bottom -= 200
                        else:
                            velx = 0
                            vely = self.aceleracion * 5
                            self.aceleracion += 0.01
                            for lista in range(810):
                                obstacle.listaObjetos[lista][3] += vely
                            for enem in range(10):
                                Enemigo.listaEnemigo[enem][3] += 5
                            jugador2.rectCar.top += 5
                        # Empujar Enemigos
                            for i in range(10):
                                if jugador.rectCar.colliderect(Enemigo.listaEnemigo[i][1]):
                                    Enemigo.listaEnemigo[i][3] -= 50
                        jugador.setRuta(0)
                        ventana.blit(jugador.imagenCar, jugador.rectCar)
                        jugador.sonidoOn.stop()
                        jugador.sonidoAcel.play(1000)
                        if Fondo1.rectFondo.top > 10:
                            Fondo1.rectFondo.top = -2000
                    elif event.key == K_DOWN:
                        jugador.sonidoOn.play()
                        jugador.posicionx += velx
                        rectSalida.top += velx
                        if jugador.rectCar.colliderect(jugador2.rectCar):
                            velx = 0
                            vely = 0
                            jugador2.rectCar.top += 200
                        else:
                            velx = 0
                            vely = -5
                            for lista in range(810):
                                obstacle.listaObjetos[lista][3] -= 5
                            for enem in range(10):
                                Enemigo.listaEnemigo[enem][3] -= 5
                            jugador2.rectCar.bottom -= 5
                        jugador.setRuta(0)
                        ventana.blit(jugador.imagenCar, jugador.rectCar)
                        jugador.sonidoOn.play()
                        if Fondo1.rectFondo.bottom < 1000:
                            Fondo1.rectFondo.bottom = 4000

                    # definicion de tecla para disparos del jugador
                    elif event.key == K_SPACE:
                        x = jugador.rectCar.centerx - 10
                        y = jugador.rectCar.centery - 50
                        miProyectil = self.proyectil(x, y, "Imagenes/proyectil.png", 5)
                        jugador.listaDisparo.append(miProyectil)
                        # reproducir efecto de sonido para el disparo del jugador
                        jugador.sonidoDisparo.play()

                    else:
                        jugador.setRuta(0)
                        ventana.blit(jugador.imagenCar, jugador.rectCar)


                elif event.type == pygame.KEYUP:
                    ventana.blit(jugador.imagenCar, jugador.rectCar)
                    velx = 0
                    vely = 0
                    if event.key == K_UP:
                        jugador.sonidoFrenado.play(1)
                        vely = self.aceleracion + 2
                        jugador.sonidoAcel.stop()
                        self.aceleracion = 0.5
                        if jugador.rectCar.colliderect(jugador2.rectCar):
                            velx = 0
                            vely = 0
                            jugador2.rectCar.bottom -= 200
                        else:
                            for lista in range(810):
                                obstacle.listaObjetos[lista][3] += vely
                            for enem in range(10):
                                Enemigo.listaEnemigo[enem][3] += vely
                            jugador2.rectCar.top += 5
                            rectSalida.top += vely
                        jugador.setRuta(0)
                        ventana.blit(jugador.imagenCar, jugador.rectCar)
                        if Fondo1.rectFondo.top > 10:
                            Fondo1.rectFondo.top = -2000
                    elif event.key == K_DOWN:
                        jugador.sonidoAcel.stop()
                    elif event.key == K_LEFT:
                        jugador.sonidoFrenado.play(1)
                        velx = self.aceleracion - 3
                        jugador.sonidoAcel.stop()
                        self.aceleracion = 0.5
                        if jugador.rectCar.colliderect(jugador2.rectCar):
                            velx = 0
                            vely = 0
                            jugador2.rectCar.right -= 200
                        else:
                            for lista in range(810):
                                obstacle.listaObjetos[lista][2] -= velx
                            for enem in range(10):
                                Enemigo.listaEnemigo[enem][2] -= velx
                            rectSalida.left -= velx
                        jugador.setRuta(2)
                        ventana.blit(jugador.imagenCar, jugador.rectCar)
                        if Fondo1.rectFondo.left > 0:
                            Fondo1.rectFondo.left = -2600
                    elif event.key == K_RIGHT:
                        jugador.sonidoFrenado.play(1)
                        velx = self.aceleracion + 3
                        jugador.sonidoAcel.stop()
                        self.aceleracion = 0.5
                        if jugador.rectCar.colliderect(jugador2.rectCar):
                            velx = 0
                            vely = 0
                            jugador2.rectCar.left += 200
                        else:
                            for lista in range(810):
                                obstacle.listaObjetos[lista][2] -= velx
                            for enem in range(10):
                                Enemigo.listaEnemigo[enem][2] -= velx
                            rectSalida.left -= velx
                        jugador.setRuta(1)
                        ventana.blit(jugador.imagenCar, jugador.rectCar)
                        if Fondo1.rectFondo.right < 2600:
                            Fondo1.rectFondo.right = 4000

                else:
                    velx = 0
                    vely = 0
                    ventana.blit(jugador.imagenCar, jugador.rectCar)

            for obstaculo in range(810):
                for enem in range(10):
                    if jugador.rectCar.colliderect(obstacle.listaObjetos[obstaculo][1]):
                        if obstacle.listaObjetos[obstaculo][4]:
                            if obstaculo >= 800:
                                obstacle.listaObjetos[obstaculo][4] = False
                                jugador.vida += 40
                            else:
                                jugador.vida -= 33
                                obstacle.listaObjetos[obstaculo][4] = False
                                pygame.mixer.music.play(1)
                    elif Enemigo.listaEnemigo[enem][1].colliderect(obstacle.listaObjetos[obstaculo][1]):
                        if Enemigo.listaEnemigo[enem][4]:
                            if obstacle.listaObjetos[obstaculo][4]:
                                if obstaculo >= 800:
                                    Enemigo.listaEnemigo[enem][5] += 40
                                    obstacle.listaObjetos[obstaculo][4] = False
                                else:
                                    Enemigo.listaEnemigo[enem][5] -= 33
                                    obstacle.listaObjetos[obstaculo][4] = False
                                    pygame.mixer.music.play(1)
                            if Enemigo.listaEnemigo[enem][5] <= 0:
                                Enemigo.listaEnemigo[enem][4] = False

            if jugador.vida > 69:
                ventana.blit(pygame.image.load("Imagenes/vida3.png"), (1090, 50))
            elif 68 > jugador.vida > 35:
                ventana.blit(pygame.image.load("Imagenes/vida2.png"), (1090, 50))
            elif 35 > jugador.vida > 5:
                ventana.blit(pygame.image.load("Imagenes/vida1.png"), (1090, 50))
            else:
                ventana.blit(pygame.image.load("Imagenes/vida0.png"), (1090, 50))
                pygame.quit()
                sys.exit()

            # definicion del movimiento de los enemigos
            for i in range(10):
                if 3 < segundos < 5:
                    Enemigo.listaEnemigo[i][0] = pygame.image.load("Imagenes/buggie2.1.png")
                    Enemigo.listaEnemigo[i][2] -= 2
                elif 13 < segundos < 15:
                    Enemigo.listaEnemigo[i][0] = pygame.image.load("Imagenes/buggie2.2.png")
                    Enemigo.listaEnemigo[i][2] += 2
                else:
                    Enemigo.listaEnemigo[i][0] = pygame.image.load("Imagenes/buggie2.png")
                    Enemigo.listaEnemigo[i][3] -= 2

            if (random.randint(0, 100)<self.rangoDisparo):
                if detener:
                    self.disparoEnemy(Enemigo)

            # condición para dibujar los disparos del jugador
            if len(jugador.listaDisparo) > 0:
                for disparoCarro in jugador.listaDisparo:
                    disparoCarro.dibujarDisparo(ventana)
                    disparoCarro.trayectoria()
                    # condicion para validar si un enemigo es eliminado por el disparo del jugador
                    if len(Enemigo.listaEnemigo) > 0:
                        for i in range(10):
                            if disparoCarro.rect.colliderect(Enemigo.listaEnemigo[i][1]):
                                if Enemigo.listaEnemigo[i][4]:
                                    self.puntos = self.puntos + 10
                                    # sonidoExplosion.play()
                                    Enemigo.listaEnemigo[i][5] -= 10
                                    jugador.listaDisparo.remove(disparoCarro)
                    if len(obstacle.listaObjetos) > 0:
                        for j in range(810):
                            if disparoCarro.rect.colliderect(obstacle.listaObjetos[j][1]):
                                if obstacle.listaObjetos[j][4]:
                                    obstacle.listaObjetos[j][4] = False
                                    jugador.listaDisparo.remove(disparoCarro)
                    if jugador2.vida > 0:
                        if disparoCarro.rect.colliderect(jugador2.rectCar):
                            jugador.listaDisparo.remove(disparoCarro)
                            jugador2.vida -= 10
                            self.puntos = self.puntos + 10

            #Condiciones para las bajas
            for i in range(10):
                if Enemigo.listaEnemigo[i][5] <= 0:
                    Enemigo.listaEnemigo[i][4] = False

            # condicion para el disparo de los enemigos
            if len(Enemigo.listaDisparo) > 0:
                for disparoEnemigo in Enemigo.listaDisparo:
                    disparoEnemigo.dibujarDisparo(ventana)
                    disparoEnemigo.trayectoria()
                    # valida si el enemigo dispara al jugador
                    if disparoEnemigo.rect.colliderect(jugador.rectCar):
                        jugador.vida -= 10
                    # valida si el disparo de la nave colisiona con el de un enemigo, entonces que se eliminen ambos
                    for disparo in jugador.listaDisparo:
                        if disparo.rect.colliderect(disparoEnemigo.rect):
                            Enemigo.listaDisparo.remove(disparoEnemigo)
                            jugador.listaDisparo.remove(disparo)

            # validacion para pasar al siguente nivel
            if minutos == 2:
                self.nivel += 1
                # niveles de dificultad
                if self.nivel == 2:
                    self.sigNivel = NuevoJuego(3, 2.5, 5, self.username, self.nivel, 0.5)
                    self.sigNivel.CrearVentana()
                elif self.nivel == 3:
                    self.otroNivel = NuevoJuego(5, 3.5, 5, self.username, self.nivel, 0.5)
                    self.otroNivel.CrearVentana()
                # valida si el jugador a completado el juego con exito, si es así se imprime ´pantalla de felicitación
                else:
                    print("FIN")


            # se actualiza la pantalla
            pygame.display.update()

    # si el jugador pierde entonces vuelve al nivel 1
    '''def gameOver(self):
        self.nivel = 1
        self.sigNivel = NuevoJuego(1, 1.5, self.user, 5, 0.5, self.nivel)
        self.sigNivel.CrearVentana()'''

