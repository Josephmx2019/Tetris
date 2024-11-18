import pygame
import random

# Inicializa Pygame
pygame.init()

# Define algunos colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Configuración de la pantalla
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Define las formas de los tetrominos
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 0], [1, 1, 1]]   # T
]

SHAPE_COLORS = [CYAN, YELLOW, GREEN, RED, BLUE, ORANGE, MAGENTA]

# Función para generar un nuevo tetromino
def get_new_piece():
    shape = random.choice(SHAPES)
    color = SHAPE_COLORS[SHAPES.index(shape)]
    return {'shape': shape, 'color': color, 'x': SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2, 'y': 0}

# Función para dibujar una pieza
def draw_piece(piece):
    shape = piece['shape']
    color = piece['color']
    for i, row in enumerate(shape):
        for j, val in enumerate(row):
            if val:
                pygame.draw.rect(SCREEN, color, (piece['x'] * BLOCK_SIZE + j * BLOCK_SIZE, piece['y'] * BLOCK_SIZE + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Función para mover la pieza
def move_piece(piece, dx, dy):
    piece['x'] += dx
    piece['y'] += dy

# Función para verificar si la pieza colisiona
def check_collision(board, piece):
    shape = piece['shape']
    for i, row in enumerate(shape):
        for j, val in enumerate(row):
            if val:
                x = piece['x'] + j
                y = piece['y'] + i
                if x < 0 or x >= SCREEN_WIDTH // BLOCK_SIZE or y >= SCREEN_HEIGHT // BLOCK_SIZE:
                    return True
                if board[y][x]:
                    return True
    return False

# Función para agregar la pieza al tablero
def add_piece_to_board(board, piece):
    shape = piece['shape']
    for i, row in enumerate(shape):
        for j, val in enumerate(row):
            if val:
                board[piece['y'] + i][piece['x'] + j] = piece['color']

# Función para eliminar filas completas
def clear_lines(board):
    global score
    lines_to_clear = [i for i, row in enumerate(board) if all(cell for cell in row)]
    for i in lines_to_clear:
        board.pop(i)
        board.insert(0, [None] * (SCREEN_WIDTH // BLOCK_SIZE))
        score += 100

# Función para dibujar el tablero
def draw_board(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(SCREEN, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Función para mostrar el puntaje
def show_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    SCREEN.blit(text, (10, 10))

# Configuración inicial
board = [[None] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
clock = pygame.time.Clock()
game_over = False
score = 0

# Juego principal
while not game_over:
    piece = get_new_piece()
    piece_dropped = False

    # Movimiento del tetromino
    while not game_over and not piece_dropped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_piece(piece, -1, 0)
                    if check_collision(board, piece):
                        move_piece(piece, 1, 0)
                if event.key == pygame.K_RIGHT:
                    move_piece(piece, 1, 0)
                    if check_collision(board, piece):
                        move_piece(piece, -1, 0)
                if event.key == pygame.K_DOWN:
                    move_piece(piece, 0, 1)
                    if check_collision(board, piece):
                        move_piece(piece, 0, -1)
                        add_piece_to_board(board, piece)
                        clear_lines(board)
                        piece_dropped = True
                if event.key == pygame.K_UP:
                    # Rotación de la pieza
                    piece['shape'] = [list(x) for x in zip(*piece['shape'][::-1])]
                    if check_collision(board, piece):
                        piece['shape'] = [list(x) for x in zip(*piece['shape'])[::-1]]

        # Bajar la pieza automáticamente
        move_piece(piece, 0, 1)
        if check_collision(board, piece):
            move_piece(piece, 0, -1)  # Vuelve a la posición anterior
            add_piece_to_board(board, piece)  # Fija la pieza al tablero
            clear_lines(board)  # Elimina líneas completas
            piece_dropped = True  # Indica que la pieza ha caído

        # Dibuja la pantalla
        SCREEN.fill(BLACK)
        draw_board(board)
        draw_piece(piece)
        show_score(score)
        pygame.display.flip()
        clock.tick(3)  # Control de velocidad del juego

pygame.quit()
