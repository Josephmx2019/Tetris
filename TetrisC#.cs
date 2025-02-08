using System;
using System.Threading;

class Program {
  const int ANCHO = 10;
  const int ALTO = 20;
  public static char[,] tablero = new char[ALTO, ANCHO];
  public static Random rand = new Random();

  public struct Pieza
  {
      public int[,] bloques;
  }

  static Pieza[] piezas = new Pieza[7]
  {
      new Pieza { bloques = new int[,] { { 0, 0 }, { 1, 0 }, { 0, 1 }, { 1, 1 } } }, // Cuadrado
      new Pieza { bloques = new int[,] { { 0, -1 }, { 0, 0 }, { 0, 1 }, { 0, 2 } } }, // Línea
      new Pieza { bloques = new int[,] { { 0, 0 }, { 1, 0 }, { 2, 0 }, { 2, 1 } } }, // L normal
      new Pieza { bloques = new int[,] { { 0, 0 }, { 1, 0 }, { 2, 0 }, { 0, 1 } } }, // L invertida
      new Pieza { bloques = new int[,] { { 0, 1 }, { 1, 1 }, { 1, 0 }, { 2, 0 } } }, // Z normal
      new Pieza { bloques = new int[,] { { 0, 0 }, { 1, 0 }, { 1, 1 }, { 2, 1 } } }, // Z invertida
      new Pieza { bloques = new int[,] { { 0, 0 }, { 1, 0 }, { 2, 0 }, { 1, 1 } } }  // T
  };

  static Pieza piezaActual;
  public static int x, y;
  
  public static void inicializarTablero()
  {
    for (int i = 0; i < ALTO; i++)
    {
      for (int j = 0; j < ANCHO; j++)
      {
        tablero[i,j] = ' ';
      }
    }
  }

  public static void imprimirTablero(){
    Console.Clear();
    for (int i = 0; i < ALTO; i++)
    {
      Console.Write("|");
      for (int j = 0; j < ANCHO; j++)
      {
        int esPartePieza = 0;
        for (int k = 0; k < 4; k++)
        {
          if (x + piezaActual.bloques[k,0] == j && y + piezaActual.bloques[k,1] == i)
          {
            esPartePieza = 1;
          }
        }
        if (esPartePieza != 0)
        {
            Console.Write('#');
        }
        else
        {
            Console.Write(tablero[i, j]);
        }
      }
      Console.WriteLine("|");
    }
    Console.WriteLine("--------------------");
  }

  public static void generarPieza()
  {
    int tipo = rand.Next(0, 7); // Genera un número aleatorio entre 0 y 6
    piezaActual = piezas[tipo];
    x = ANCHO / 2 - 1;
    y = 0;
  }

  public static int colisiona(int nuevoX, int nuevoY, Pieza nuevaPieza)
  {
    for (int i = 0; i < 4; i++) {
        int px = nuevoX + nuevaPieza.bloques[i,0];
        int py = nuevoY + nuevaPieza.bloques[i,1];

        if (py >= ALTO || px < 0 || px >= ANCHO || tablero[py,px] != ' ')
            return 1;
    }
    return 0;
  }

  public static void fijarPieza()
  {
    for (int i = 0; i < 4; i++)
    {
      tablero[y + piezaActual.bloques[i,1],x + piezaActual.bloques[i,0]] = '#';
    }
  }

  public static void eliminarLineas() {
      for (int fila = ALTO - 1; fila >= 0; fila--) {
          int completa = 1;

          for (int col = 0; col < ANCHO; col++) {
              if (tablero[fila,col] == ' ') {
                  completa = 0;
                  break;
              }
          }

          if (completa != 0) {
              for (int y = fila; y > 0; y--)
                  for (int x = 0; x < ANCHO; x++)
                      tablero[y,x] = tablero[y - 1,x];

              for (int x = 0; x < ANCHO; x++)
                  tablero[0,x] = ' ';

              fila++; 
          }
      }
  }

  public static void moverPieza(int dx, int dy) 
  {
    if (colisiona(x + dx, y + dy, piezaActual) != 1) 
    {
        x += dx;
        y += dy;
    } else if (dy == 1) 
    { 
      fijarPieza();
      eliminarLineas();
      generarPieza();

      if (colisiona(x, y, piezaActual) != 0) 
      {
        Console.WriteLine("Game Over");
        Console.ReadLine();
      }
    }
  }

  public static Pieza rotarPieza(Pieza pieza)
  {
    Pieza rotada = pieza;
    for (int i = 0; i < 4; i++) {
        int tempX = pieza.bloques[i,0];
        rotada.bloques[i,0] = -pieza.bloques[i,1];
        rotada.bloques[i,1] = tempX;
    }
    return rotada;
  }

  public static void rotarSiPosible() {
      Pieza nuevaRotacion = rotarPieza(piezaActual);
      if (colisiona(x, y, nuevaRotacion) != 1)
    {
      piezaActual = nuevaRotacion;
    }
  }

  public static void jugar()
  {
    generarPieza();

    while (true)
    {
      imprimirTablero();
      if (Console.KeyAvailable) // Verifica si una tecla ha sido presionada
      {
          ConsoleKey tecla = Console.ReadKey(intercept: true).Key; // Lee la tecla presionada
          switch (tecla)
          {
          case ConsoleKey.A: moverPieza(-1, 0); break;
          case ConsoleKey.D: moverPieza(1, 0); break;
          case ConsoleKey.S: moverPieza(0, 1); break;
          case ConsoleKey.W: rotarSiPosible(); break;
          }
      }

      Thread.Sleep(300);
      moverPieza(0, 1); 
    }
    Console.WriteLine("Presiona una tecla para salir");
    Console.ReadKey();
  }
  
  public static void Main (string[] args) {
    inicializarTablero();
    jugar();
  }
}