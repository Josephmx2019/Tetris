from os import system
from random import randint
from keyboard import is_pressed
from time import sleep

class Pieza:
    def __init__(self, bloques):
        self.bloques = bloques

ANCHO = 10
ALTO = 20
tablero = [[' ' for _ in range(ANCHO)] for _ in range(ALTO)]
x, y = 0, 0

piezas = [
    Pieza([[0, 0], [1, 0], [0, 1], [1, 1]]),  # Cuadrado
    Pieza([[0, -1], [0, 0], [0, 1], [0, 2]]),  # Línea
    Pieza([[0, 0], [1, 0], [2, 0], [2, 1]]),  # L normal
    Pieza([[0, 0], [1, 0], [2, 0], [0, 1]]),  # L invertida
    Pieza([[0, 1], [1, 1], [1, 0], [2, 0]]),  # Z normal
    Pieza([[0, 0], [1, 0], [1, 1], [2, 1]]),  # Z invertida
    Pieza([[0, 0], [1, 0], [2, 0], [1, 1]])   # T
]

piezaActual = piezas[0]

def inicializarTablero():
    for i in range(ALTO):
        for j in range(ANCHO):
            tablero[i][j] = ' '

def imprimirTablero():
    system("cls")  # Para Windows, usa "clear" en Linux
    for i in range(ALTO):
        print("|", end="")
        for j in range(ANCHO):
            esPartePieza = any(x + piezaActual.bloques[k][0] == j and y + piezaActual.bloques[k][1] == i for k in range(4))
            print('#' if esPartePieza else tablero[i][j], end='')
        print("|")
    print("-" * (ANCHO + 2))

def generarPieza():
    global piezaActual, x, y
    piezaActual = piezas[randint(0, 6)]
    x, y = ANCHO // 2 - 1, 0

def colisiona(nuevoX, nuevoY, nuevaPieza):
    for i in range(4):
        px = nuevoX + nuevaPieza.bloques[i][0]
        py = nuevoY + nuevaPieza.bloques[i][1]
        if py >= ALTO or px < 0 or px >= ANCHO or tablero[py][px] != ' ':
            return True
    return False

def fijarPieza():
    for i in range(4):
        tablero[y + piezaActual.bloques[i][1]][x + piezaActual.bloques[i][0]] = '#'

def eliminarLineas():
    global tablero
    nuevas_filas = [fila for fila in tablero if ' ' in fila]
    for _ in range(ALTO - len(nuevas_filas)):
        nuevas_filas.insert(0, [' '] * ANCHO)
    tablero = nuevas_filas

def moverPieza(dx, dy):
    global x, y
    if not colisiona(x + dx, y + dy, piezaActual):
        x += dx
        y += dy
    elif dy == 1:  # Si la pieza choca al bajar
        fijarPieza()
        eliminarLineas()
        generarPieza()
        if colisiona(x, y, piezaActual):
            print("Game Over")
            exit()

def rotarPieza(pieza):
    return Pieza([[-y, x] for x, y in pieza.bloques])

def rotarSiPosible():
    global piezaActual
    nuevaRotacion = rotarPieza(piezaActual)
    if not colisiona(x, y, nuevaRotacion):
        piezaActual = nuevaRotacion

def jugar():
    generarPieza()
    while True:
        imprimirTablero()
        if is_pressed("a"): moverPieza(-1, 0)
        if is_pressed("d"): moverPieza(1, 0)
        if is_pressed("s"): moverPieza(0, 1)
        if is_pressed("w"): rotarSiPosible()
        sleep(0.3)
        moverPieza(0, 1)

if __name__ == "__main__":
    inicializarTablero()
    jugar()


"""from os import system
from random import randint
from keyboard import is_pressed
from time import sleep 

class Pieza():
    def __init__(self, bloques):
        self.bloques = bloques

ANCHO = 10
ALTO = 20
tablero = [[' ' for _ in range(ANCHO)] for _ in range(ALTO)]
x = 0
y = 0

piezas = [
    Pieza([[0, 0], [1, 0], [0, 1], [1, 1]]),  # Cuadrado
    Pieza([[0, -1], [0, 0], [0, 1], [0, 2]]),  # Línea
    Pieza([[0, 0], [1, 0], [2, 0], [2, 1]]),  # L normal
    Pieza([[0, 0], [1, 0], [2, 0], [0, 1]]),  # L invertida
    Pieza([[0, 1], [1, 1], [1, 0], [2, 0]]),  # Z normal
    Pieza([[0, 0], [1, 0], [1, 1], [2, 1]]),  # Z invertida
    Pieza([[0, 0], [1, 0], [2, 0], [1, 1]])   # T
]

piezaActual = piezas[0]

def inicializarTablero():
    for i in range(ALTO):
        for j in range(ANCHO):
            tablero[i][j] = ' '

def imprimirTablero():
    system("cls")
    for i in range(ALTO):
        print("|")
        for j in range(ANCHO):
            esPartePieza = 0
            for k in range(4):
                if x + piezaActual.bloques[k][0] == j and y + piezaActual.bloques[k][1] == i:
                    esPartePieza = 1
            
            print('#' if esPartePieza else tablero[i][j], end='')
        print("\n")
    print("--------------------\n")

def generarPieza():
    tipo = randint(0,6)
    piezaActual = piezas[tipo]
    x = ANCHO / 2 - 1
    y = 0

def colisiona(nuevoX, nuevoY, nuevaPieza):
    for i in range(4):
        px = nuevoX + nuevaPieza.bloques[i][0]
        py = nuevoY + nuevaPieza.bloques[i][1]

        if py >= ALTO or px < 0 or px >= ANCHO or tablero[py][px] != ' ':
            return 1
    return 0

def fijarPieza():
    for i in range(4):
        tablero[y + piezaActual.bloques[i][1]][x + piezaActual.bloques[i][0]] = '#'

def eliminarLineas():
    for fila in range(ALTO - 1, 0, -1):
        completa = 1

        for col in range(ANCHO):
            if tablero[fila][col] == ' ':
                completa = 0
                break

        if completa:
            for y in range(fila, 0, -1):
                for x in range(ANCHO):
                    tablero[y][x] = tablero[y - 1][x]
            
            for x in range(ANCHO):
                tablero[0][x] = ' '
            fila = fila + 1

def moverPieza(dx, dy):
    global x,y
    if colisiona(x + dx, y + dy, piezaActual) != 1:
        x += dx
        y += dy
    elif dy == 1:
        fijarPieza()
        eliminarLineas()
        generarPieza()

        if colisiona(x, y, piezaActual):
            print("Game Over")

def rotarPieza(pieza):
    rotada = pieza
    for i in range(4):
        tempX = pieza.bloques[i][0]
        rotada.bloques[i][0] = pieza.bloques[i][1]
        rotada.bloques[i][1] = tempX
    return rotada

def rotarSiPosible():
    nuevaRotacion = rotarPieza(piezaActual)
    if colisiona(x, y, nuevaRotacion) != 1:
        piezaActual = nuevaRotacion

def jugar():
    generarPieza()
    while 1:
        imprimirTablero()
        if is_pressed('a'):
            moverPieza(-1, 0)
        elif is_pressed('d'):
            moverPieza(1, 0)
        elif is_pressed('s'):
            moverPieza(0, 1)
        elif is_pressed('w'):
            rotarSiPosible()
        sleep(0.3)
        moverPieza(0, 1)

def main():
    inicializarTablero()
    jugar()

if __name__ == '__main__':
    main()"""
