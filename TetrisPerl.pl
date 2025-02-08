use strict;
use warnings;
use Time::HiRes qw(sleep);

# Constantes para el tamaño del tablero
my $ANCHO = 10;
my $ALTO = 20;

# Tablero de juego
my @tablero = map { [' '] x $ANCHO } 1..$ALTO;

# Definición de las piezas
my @piezas = (
    [[ [0,0], [1,0], [0,1], [1,1] ]],  # Cuadrado
    [[ [0,-1], [0,0], [0,1], [0,2] ]],  # Línea
    [[ [0,0], [1,0], [2,0], [2,1] ]],   # L normal
    [[ [0,0], [1,0], [2,0], [0,1] ]],   # L invertida
    [[ [0,1], [1,1], [1,0], [2,0] ]],   # Z normal
    [[ [0,0], [1,0], [1,1], [2,1] ]],   # Z invertida
    [[ [0,0], [1,0], [2,0], [1,1] ]]    # T
);

my $piezaActual;
my $x;
my $y;

# Inicializar el tablero
sub inicializarTablero {
    for my $i (0..$ALTO-1) {
        for my $j (0..$ANCHO-1) {
            $tablero[$i][$j] = ' ';
        }
    }
}

# Imprimir el tablero
sub imprimirTablero {
    system('clear');  # Para Linux/macOS, usa 'cls' en Windows
    for my $i (0..$ALTO-1) {
        print "|";
        for my $j (0..$ANCHO-1) {
            my $esPartePieza = 0;
            for my $k (0..3) {
                if ($x + $piezaActual->[$k][0] == $j && $y + $piezaActual->[$k][1] == $i) {
                    $esPartePieza = 1;
                    last;
                }
            }
            print $esPartePieza ? '#' : $tablero[$i][$j];
        }
        print "|\n";
    }
    print "-" x 20 . "\n";
}

# Generar una nueva pieza
sub generarPieza {
    my $tipo = int(rand(7));
    $piezaActual = $piezas[$tipo];
    $x = int($ANCHO / 2) - 1;
    $y = 0;
}

# Verificar colisión de la pieza
sub colisiona {
    my ($nuevoX, $nuevoY, $nuevaPieza) = @_;
    for my $i (0..3) {
        my $px = $nuevoX + $nuevaPieza->[$i][0];
        my $py = $nuevoY + $nuevaPieza->[$i][1];

        if ($py >= $ALTO || $px < 0 || $px >= $ANCHO || $tablero[$py][$px] ne ' ') {
            return 1;
        }
    }
    return 0;
}

# Fijar la pieza en el tablero
sub fijarPieza {
    for my $i (0..3) {
        $tablero[$y + $piezaActual->[$i][1]][$x + $piezaActual->[$i][0]] = '#';
    }
}

# Eliminar líneas completas
sub eliminarLineas {
    for my $fila (reverse 0..$ALTO-1) {
        my $completa = 1;

        for my $col (0..$ANCHO-1) {
            if ($tablero[$fila][$col] eq ' ') {
                $completa = 0;
                last;
            }
        }

        if ($completa) {
            for my $y ($fila..1) {
                for my $x (0..$ANCHO-1) {
                    $tablero[$y][$x] = $tablero[$y-1][$x];
                }
            }
            for my $x (0..$ANCHO-1) {
                $tablero[0][$x] = ' ';
            }
        }
    }
}

# Mover la pieza
sub moverPieza {
    my ($dx, $dy) = @_;
    if (!colisiona($x + $dx, $y + $dy, $piezaActual)) {
        $x += $dx;
        $y += $dy;
    } elsif ($dy == 1) {  # Cuando se mueve hacia abajo
        fijarPieza();
        eliminarLineas();
        generarPieza();

        if (colisiona($x, $y, $piezaActual)) {
            print "Game Over\n";
            exit(0);
        }
    }
}

# Rotar la pieza
sub rotarPieza {
    my ($pieza) = @_;
    my @rotada = @$pieza;
    for my $i (0..3) {
        my $tempX = $pieza->[$i][0];
        $rotada[$i][0] = -$pieza->[$i][1];
        $rotada[$i][1] = $tempX;
    }
    return \@rotada;
}

# Intentar rotar la pieza si es posible
sub rotarSiPosible {
    my $nuevaRotacion = rotarPieza($piezaActual);
    if (!colisiona($x, $y, $nuevaRotacion)) {
        $piezaActual = $nuevaRotacion;
    }
}

# Función principal de juego
sub jugar {
    generarPieza();
    while (1) {
        imprimirTablero();
        my $input = '';
        $| = 1;  # Flush output after each print
        if (defined($input = <STDIN>)) {
            chomp($input);
            if ($input eq 'a') { moverPieza(-1, 0); }
            elsif ($input eq 'd') { moverPieza(1, 0); }
            elsif ($input eq 's') { moverPieza(0, 1); }
            elsif ($input eq 'w') { rotarSiPosible(); }
        }
        sleep(0.3);
        moverPieza(0, 1);
    }
}

# Iniciar el juego
inicializarTablero();
jugar();
