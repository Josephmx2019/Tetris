import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO = 10
ALTO = 20
TAM_CELDA = 30  # Tamaño de cada celda en el tablero
FPS = 10  # Control de velocidad del juego

# Colores
COLOR_FONDO = (0, 0, 0)
COLOR_BLOQUE = (255, 0, 0)
COLOR_LINEA = (128, 128, 128)

# Tamaño de la pantalla
ANCHO_VENTANA = ANCHO * TAM_CELDA
ALTO_VENTANA = ALTO * TAM_CELDA

# Definir la pantalla
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tetris")

# Definir los bloques de las piezas
class Pieza():
    def __init__(self, bloques):
        self.bloques = bloques

# Definir las piezas (con sus coordenadas relativas)
piezas = [
    Pieza([[0, 0], [1, 0], [0, 1], [1, 1]]),  # Cuadrado
    Pieza([[0, -1], [0, 0], [0, 1], [0, 2]]),  # Línea
    Pieza([[0, 0], [1, 0], [2, 0], [2, 1]]),  # L normal
    Pieza([[0, 0], [1, 0], [2, 0], [0, 1]]),  # L invertida
    Pieza([[0, 1], [1, 1], [1, 0], [2, 0]]),  # Z normal
    Pieza([[0, 0], [1, 0], [1, 1], [2, 1]]),  # Z invertida
    Pieza([[0, 0], [1, 0], [2, 0], [1, 1]])   # T
]

# Tablero y variables del juego
tablero = [[' ' for _ in range(ANCHO)] for _ in range(ALTO)]
x, y = ANCHO // 2 - 1, 0
piezaActual = piezas[0]

def inicializarTablero():
    for i in range(ALTO):
        for j in range(ANCHO):
            tablero[i][j] = ' '

def dibujarTablero():
    pantalla.fill(COLOR_FONDO)  # Llenar el fondo con color
    for i in range(ALTO):
        for j in range(ANCHO):
            if tablero[i][j] != ' ':
                pygame.draw.rect(pantalla, COLOR_BLOQUE,
                                 (j * TAM_CELDA, i * TAM_CELDA, TAM_CELDA, TAM_CELDA))
            pygame.draw.rect(pantalla, COLOR_LINEA,
                             (j * TAM_CELDA, i * TAM_CELDA, TAM_CELDA, TAM_CELDA), 1)  # Dibujar líneas de la cuadrícula
    pygame.display.update()

def generarPieza():
    global piezaActual, x, y
    tipo = random.randint(0, 6)
    piezaActual = piezas[tipo]
    x = ANCHO // 2 - 1
    y = 0

def colisiona(nuevoX, nuevoY, nuevaPieza):
    for i in range(4):
        px = nuevoX + nuevaPieza.bloques[i][0]
        py = nuevoY + nuevaPieza.bloques[i][1]
        if py >= ALTO or px < 0 or px >= ANCHO or tablero[py][px] != ' ':
            return True
    return False

def fijarPieza():
    global x, y
    for i in range(4):
        tablero[y + piezaActual.bloques[i][1]][x + piezaActual.bloques[i][0]] = '#'

def eliminarLineas():
    for fila in range(ALTO - 1, -1, -1):
        if all(tablero[fila][col] != ' ' for col in range(ANCHO)):
            for y in range(fila, 0, -1):
                for x in range(ANCHO):
                    tablero[y][x] = tablero[y - 1][x]
            for x in range(ANCHO):
                tablero[0][x] = ' '

def moverPieza(dx, dy):
    global x, y
    if not colisiona(x + dx, y + dy, piezaActual):
        x += dx
        y += dy
    elif dy == 1:
        fijarPieza()
        eliminarLineas()
        generarPieza()
        if colisiona(x, y, piezaActual):
            print("Game Over")
            pygame.quit()
            sys.exit()

def rotarPieza(pieza):
    rotada = Pieza([[0, 0] for _ in range(4)])
    for i in range(4):
        rotada.bloques[i][0] = -pieza.bloques[i][1]
        rotada.bloques[i][1] = pieza.bloques[i][0]
    return rotada

def rotarSiPosible():
    global piezaActual
    nuevaRotacion = rotarPieza(piezaActual)
    if not colisiona(x, y, nuevaRotacion):
        piezaActual = nuevaRotacion

def dibujarPieza(x, y, pieza):
    for i in range(4):
        px = x + pieza.bloques[i][0]
        py = y + pieza.bloques[i][1]
        if 0 <= px < ANCHO and 0 <= py < ALTO:
            pygame.draw.rect(pantalla, COLOR_BLOQUE,
                             (px * TAM_CELDA, py * TAM_CELDA, TAM_CELDA, TAM_CELDA))

def dibujarTablero():
    pantalla.fill(COLOR_FONDO)  # Llenar el fondo con color
    # Dibujar el tablero
    for i in range(ALTO):
        for j in range(ANCHO):
            if tablero[i][j] != ' ':
                pygame.draw.rect(pantalla, COLOR_BLOQUE,
                                 (j * TAM_CELDA, i * TAM_CELDA, TAM_CELDA, TAM_CELDA))
            pygame.draw.rect(pantalla, COLOR_LINEA,
                             (j * TAM_CELDA, i * TAM_CELDA, TAM_CELDA, TAM_CELDA), 1)  # Dibujar líneas de la cuadrícula

    # Dibujar la pieza actual en su posición
    dibujarPieza(x, y, piezaActual)
    
    pygame.display.update()

def moverPieza(dx, dy):
    global x, y
    if not colisiona(x + dx, y + dy, piezaActual):
        x += dx
        y += dy
    elif dy == 1:
        fijarPieza()
        eliminarLineas()
        generarPieza()
        if colisiona(x, y, piezaActual):
            print("Game Over")
            pygame.quit()
            sys.exit()

def jugar():
    global piezaActual
    generarPieza()
    clock = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.key.get_pressed()[pygame.K_a]:
            moverPieza(-1, 0)
        elif pygame.key.get_pressed()[pygame.K_d]:
            moverPieza(1, 0)
        elif pygame.key.get_pressed()[pygame.K_s]:
            moverPieza(0, 1)
        elif pygame.key.get_pressed()[pygame.K_w]:
            rotarSiPosible()

        moverPieza(0, 1)  # Mover la pieza hacia abajo
        dibujarTablero()  # Dibujar todo el tablero con la pieza en movimiento
        clock.tick(FPS)

# Iniciar el juego
if __name__ == "__main__":
    inicializarTablero()
    jugar()
