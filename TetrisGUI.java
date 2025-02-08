import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.Random;
import javax.swing.*;

public class TetrisGUI extends JPanel implements KeyListener {
    static final int ANCHO = 10;
    static final int ALTO = 20;
    static final int TAMANO_CELDA = 30; 
    static char[][] tablero = new char[ALTO][ANCHO];
    static Pieza piezaActual;
    static int x, y;
    static Random rand = new Random();

    static class Pieza {
        int[][] bloques;
        Pieza(int[][] bloques) { this.bloques = bloques; }
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

    public TetrisGUI() {
        setPreferredSize(new Dimension(ANCHO * TAMANO_CELDA, ALTO * TAMANO_CELDA));
        setBackground(Color.BLACK);
        addKeyListener(this);
        setFocusable(true);
        inicializarTablero();
        generarPieza();
        iniciarJuego();
    }

    public static void inicializarTablero() {
        for (int i = 0; i < ALTO; i++) {
            for (int j = 0; j < ANCHO; j++) {
                tablero[i][j] = ' ';
            }
        }
    }

    public static void generarPieza() {
        piezaActual = piezas[rand.nextInt(piezas.length)];
        x = ANCHO / 2 - 1;
        y = 0;
    }

    public static boolean colisiona(int nuevoX, int nuevoY) {
        for (int i = 0; i < 4; i++) {
            int px = nuevoX + piezaActual.bloques[i][0];
            int py = nuevoY + piezaActual.bloques[i][1];

            if (py >= ALTO || px < 0 || px >= ANCHO || tablero[py][px] != ' ') {
                return true;
            }
        }
        return false;
    }

    public static void fijarPieza() {
        for (int i = 0; i < 4; i++) {
            int px = x + piezaActual.bloques[i][0];
            int py = y + piezaActual.bloques[i][1];
            tablero[py][px] = '#';
        }
    }

    public static void eliminarLineas() {
        for (int fila = ALTO - 1; fila >= 0; fila--) {
            boolean completa = true;
            for (int col = 0; col < ANCHO; col++) {
                if (tablero[fila][col] == ' ') {
                    completa = false;
                    break;
                }
            }
            if (completa) {
                for (int i = fila; i > 0; i--) {
                    System.arraycopy(tablero[i - 1], 0, tablero[i], 0, ANCHO);
                }
                for (int col = 0; col < ANCHO; col++) {
                    tablero[0][col] = ' ';
                }
                fila++; // Revisar de nuevo la misma fila
            }
        }
    }

    public void moverPieza(int dx, int dy) {
        if (!colisiona(x + dx, y + dy)) {
            x += dx;
            y += dy;
        } else if (dy == 1) {
            fijarPieza();
            eliminarLineas();
            generarPieza();
            if (colisiona(x, y)) {
                JOptionPane.showMessageDialog(this, "Game Over");
                System.exit(0);
            }
        }
        repaint();
    }

    public static Pieza rotarPieza(Pieza pieza) {
        int[][] nuevosBloques = new int[4][2];
        for (int i = 0; i < 4; i++) {
            nuevosBloques[i][0] = -pieza.bloques[i][1];
            nuevosBloques[i][1] = pieza.bloques[i][0];
        }
        return new Pieza(nuevosBloques);
    }

    public void rotarSiPosible() {
        Pieza nuevaRotacion = rotarPieza(piezaActual);
        if (!colisiona(x, y)) {
            piezaActual = nuevaRotacion;
        }
        repaint();
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        for (int i = 0; i < ALTO; i++) {
            for (int j = 0; j < ANCHO; j++) {
                if (tablero[i][j] == '#') {
                    g.setColor(Color.BLUE);
                    g.fillRect(j * TAMANO_CELDA, i * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA);
                }
                g.setColor(Color.WHITE);
                g.drawRect(j * TAMANO_CELDA, i * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA);
            }
        }
        g.setColor(Color.RED);
        for (int i = 0; i < 4; i++) {
            int px = x + piezaActual.bloques[i][0];
            int py = y + piezaActual.bloques[i][1];
            g.fillRect(px * TAMANO_CELDA, py * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA);
        }
    }

    @Override
    public void keyPressed(KeyEvent e) {
        switch (e.getKeyCode()) {
            case KeyEvent.VK_A: moverPieza(-1, 0); break;
            case KeyEvent.VK_D: moverPieza(1, 0); break;
            case KeyEvent.VK_S: moverPieza(0, 1); break;
            case KeyEvent.VK_W: rotarSiPosible(); break;
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {}

    @Override
    public void keyTyped(KeyEvent e) {}

    public void iniciarJuego() {
        Timer timer = new Timer(500, e -> {
            moverPieza(0, 1);
        });
        timer.start();
    }

    public static void main(String[] args) {
        JFrame ventana = new JFrame("Tetris en Java");
        TetrisGUI juego = new TetrisGUI();
        ventana.add(juego);
        ventana.pack();
        ventana.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        ventana.setVisible(true);
    }
}
