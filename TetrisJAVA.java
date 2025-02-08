import java.util.Random;
import java.util.Scanner;

public class TetrisJAVA{
    static final int ANCHO = 10;
    static final int ALTO = 20;
    static char[][] tablero = new char[ALTO][ANCHO];
    static Random rand = new Random();
    static Pieza piezaActual;
    static int x, y;

    static class Pieza {
        int[][] bloques;

        Pieza(int[][] bloques) {
            this.bloques = bloques;
        }
    }

    static Pieza[] piezas = {
            new Pieza(new int[][]{{0,0}, {1,0}, {0,1}, {1,1}}),  // Cuadrado
            new Pieza(new int[][]{{0,-1}, {0,0}, {0,1}, {0,2}}), // Línea
            new Pieza(new int[][]{{0,0}, {1,0}, {2,0}, {2,1}}),  // L normal
            new Pieza(new int[][]{{0,0}, {1,0}, {2,0}, {0,1}}),  // L invertida
            new Pieza(new int[][]{{0,1}, {1,1}, {1,0}, {2,0}}),  // Z normal
            new Pieza(new int[][]{{0,0}, {1,0}, {1,1}, {2,1}}),  // Z invertida
            new Pieza(new int[][]{{0,0}, {1,0}, {2,0}, {1,1}})   // T
    };

    public static void Clear() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }

    public static void inicializarTablero(){
        for (int i = 0; i < ALTO; i++){
            for (int j = 0; j < ANCHO; j++){
                tablero[i][j] = ' ';
            }
        }
    }

    static void imprimirTablero() {
        System.out.print("\033[H\033[2J"); // Limpia la consola
        System.out.flush();

        for (int i = 0; i < ALTO; i++) {
            System.out.print("|");
            for (int j = 0; j < ANCHO; j++) {
                boolean esPartePieza = false;
                for (int k = 0; k < 4; k++) {
                    if (x + piezaActual.bloques[k][0] == j && y + piezaActual.bloques[k][1] == i) {
                        esPartePieza = true;
                        break;
                    }
                }
                System.out.print(esPartePieza ? '#' : tablero[i][j]);
            }
            System.out.println("|");
        }
        System.out.println("--------------------");
    }


    public static void generarPieza(){
        Random rand = new Random();
        int tipo = rand.nextInt(7);
        piezaActual = piezas[tipo];
        x = ANCHO / 2 - 1;
        y = 0;
    }

    public static int colisiona(int nuevoX, int nuevoY, Pieza nuevPieza){
        for (int i = 0; i < 4; i++){
            int px = nuevoX + nuevPieza.bloques[i][0];
            int py = nuevoY + nuevPieza.bloques[i][1];

            if (py >= ALTO || px < 0 || px >= ANCHO || tablero[py][px] != ' '){
                return 1;
            }
        }
        return 0;
    }

    public static void fijarPieza(){
        for (int i = 0; i < 4; i++){
            tablero[y + piezaActual.bloques[i][1]][x + piezaActual.bloques[i][0]] = '#';
        }
    }

    public static void eliminarLineas(){
        for (int fila = ALTO - 1; fila >= 0; fila--) {
            int completa = 1;

            for (int col = 0; col < ANCHO; col++) {
                if (tablero[fila][col] == ' ') {
                    completa = 0;
                    break;
                }
            }

            if (completa == 1) {
                for (int Y = fila; y > 0; y--){
                    for (int X = 0; x < ANCHO; x++){
                        tablero[Y][X] = tablero[Y - 1][X];
                    }
                }

                for (int X = 0; x < ANCHO; x++){
                    tablero[0][X] = ' ';
                }
                    
                fila++; 
            }
        }
    }

    public static void moverPieza(int dx, int dy){
        if (colisiona(x + dx, y + dy, piezaActual) == 0) {
            x += dx;
            y += dy;
        } else if (dy == 1) { 
            fijarPieza();
            eliminarLineas();
            generarPieza();

            if (colisiona(x, y, piezaActual) == 1) {
                System.out.println("Game Over");
            }
        }
    }

    public static Pieza rotarPieza(Pieza pieza){
        Pieza rotada = pieza;
        for (int i = 0; i < 4; i++){
            int temX = pieza.bloques[i][0];
            rotada.bloques[i][0] = pieza.bloques[i][1];
            rotada.bloques[i][1] = temX;
        }

        return rotada;
    }

    public static void rotarSiPosible(){
        Pieza nuevaRotacion = rotarPieza(piezaActual);
        if (colisiona(x, y, nuevaRotacion) == 1){
            piezaActual = nuevaRotacion;
        }
    }

    public static void jugar() {
        generarPieza();
        Scanner scanner = new Scanner(System.in);

        Thread inputThread = new Thread(() -> {
            while (true) {
                String input = scanner.nextLine();  // Lee una línea de entrada
                if (input.length() > 0) {
                    char tecla = input.charAt(0);  // Toma el primer carácter
                    switch (tecla) {
                        case 'a': moverPieza(-1, 0); break;
                        case 'd': moverPieza(1, 0); break;
                        case 's': moverPieza(0, 1); break;
                        case 'w': rotarSiPosible(); break;
                    }
                }
            }
        });
        inputThread.start();

        while (true) {
            imprimirTablero();
            try {
                Thread.sleep(300); // Control de caída de la pieza
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            moverPieza(0, 1);
        }
    }

    public static void main(String[] args) {
        inicializarTablero();
        jugar();
    }
}