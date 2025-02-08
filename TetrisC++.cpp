#include <iostream>
#include <stdlib.h>
#include <conio.h>
#include <ctime>
#include <string>
#include <windows.h>

using namespace std;

const int ANCHO = 10;
const int ALTO = 20;
#define clear "cls"

char tablero[ALTO][ANCHO];

typedef struct {
    int bloques[4][2];
} Pieza;

Pieza piezas[7] = {
    {{ {0,0}, {1,0}, {0,1}, {1,1} }},  // Cuadrado
    {{ {0,-1}, {0,0}, {0,1}, {0,2} }}, // Línea
    {{ {0,0}, {1,0}, {2,0}, {2,1} }},  // L normal
    {{ {0,0}, {1,0}, {2,0}, {0,1} }},  // L invertida
    {{ {0,1}, {1,1}, {1,0}, {2,0} }},  // Z normal
    {{ {0,0}, {1,0}, {1,1}, {2,1} }},  // Z invertida
    {{ {0,0}, {1,0}, {2,0}, {1,1} }}   // T
};

Pieza piezaActual;
int x, y;

void inicializarTablero() {
    for (int i = 0; i < ALTO; i++)
        for (int j = 0; j < ANCHO; j++)
            tablero[i][j] = ' ';
}

void imprimirTablero() {
    system(clear);
    for (int i = 0; i < ALTO; i++) {
    	cout << "|";
        for (int j = 0; j < ANCHO; j++) {
            int esPartePieza = 0;
            for (int k = 0; k < 4; k++)
                if (x + piezaActual.bloques[k][0] == j && y + piezaActual.bloques[k][1] == i)
                    esPartePieza = 1;
			
			cout << (esPartePieza ? '#' : tablero[i][j]);
        }
        cout << "|" << endl;
    }
    cout << "--------------------" << endl;
}
 
void generarPieza() {
    int tipo = rand() % 7;
    piezaActual = piezas[tipo];
    x = ANCHO / 2 - 1;
    y = 0;
}

int colisiona(int nuevoX, int nuevoY, Pieza nuevaPieza) {
    for (int i = 0; i < 4; i++) {
        int px = nuevoX + nuevaPieza.bloques[i][0];
        int py = nuevoY + nuevaPieza.bloques[i][1];

        if (py >= ALTO || px < 0 || px >= ANCHO || tablero[py][px] != ' ')
            return 1;
    }
    return 0;
}

void fijarPieza() {
    for (int i = 0; i < 4; i++)
        tablero[y + piezaActual.bloques[i][1]][x + piezaActual.bloques[i][0]] = '#';
}

void eliminarLineas() {
    for (int fila = ALTO - 1; fila >= 0; fila--) {
        int completa = 1;

        for (int col = 0; col < ANCHO; col++) {
            if (tablero[fila][col] == ' ') {
                completa = 0;
                break;
            }
        }

        if (completa) {
            for (int y = fila; y > 0; y--)
                for (int x = 0; x < ANCHO; x++)
                    tablero[y][x] = tablero[y - 1][x];

            for (int x = 0; x < ANCHO; x++)
                tablero[0][x] = ' ';

            fila++; 
        }
    }
}

void moverPieza(int dx, int dy) {
    if (!colisiona(x + dx, y + dy, piezaActual)) {
        x += dx;
        y += dy;
    } else if (dy == 1) { 
        fijarPieza();
        eliminarLineas();
        generarPieza();

        if (colisiona(x, y, piezaActual)) {
            printf("Game Over\n");
            exit(0);
        }
    }
}

Pieza rotarPieza(Pieza pieza) {
    Pieza rotada = pieza;
    for (int i = 0; i < 4; i++) {
        int tempX = pieza.bloques[i][0];
        rotada.bloques[i][0] = -pieza.bloques[i][1];
        rotada.bloques[i][1] = tempX;
    }
    return rotada;
}

void rotarSiPosible() {
    Pieza nuevaRotacion = rotarPieza(piezaActual);
    if (!colisiona(x, y, nuevaRotacion))
        piezaActual = nuevaRotacion;
}

void jugar() {
    generarPieza();
    while (1) {
        imprimirTablero();
        if (_kbhit()) {
            char tecla = _getch();
            switch (tecla) {
                case 'a': moverPieza(-1, 0); break;
                case 'd': moverPieza(1, 0); break;
                case 's': moverPieza(0, 1); break;
                case 'w': rotarSiPosible(); break;
            }
        }
        Sleep(300);
        moverPieza(0, 1);
    }
}

int main() {
    srand(time(NULL));
    inicializarTablero();
    jugar();
    return 0;
}   
    
