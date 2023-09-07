# This is our main driver file

import pygame as p

import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # For animations later on
IMAGES = {}


# Initialize a global dictionary of images and will be called exactly once in main

def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # We can access an image by saying IMAGES['wp']


# The main function that will handle user input and graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves_naive()
    move_made = False  # flag variable when the move is made

    load_images()
    running = True
    sq_selected = ()  # No square selected initially, keeps track of last click of the user  (row, column)
    player_clicks = []  # keeps track of player clicks (two tuples : [(7,4),(4,4)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):  # if the square is the same that was selected before
                    sq_selected = ()
                    player_clicks = []  # player click list has [(4,5),(6,7)]
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)  # append for both 1st and 2nd click
                if len(player_clicks) == 2:  # after 2nd click
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notations())
                    if move in valid_moves:  # only valid moves are made
                        gs.make_move(move)
                        move_made = True
                        if gs.white_to_move:
                            print("white's turn")
                        else:
                            print("black's turn")
                    sq_selected = ()  # reset user clicks
                    player_clicks = []
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves_naive()
            move_made = False

        clock.tick(MAX_FPS)
        p.display.flip()
        draw_game_state(screen, gs)


# Responsible for all graphics in the current state
def draw_game_state(screen, gs):
    draw_board(screen)
    draw_piece(screen, gs.board)


# Draw squares on the board
def draw_board(screen):
    colors = [p.Color("white"), p.Color("dark green")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# Draw the pieces on the board using the current game state of the board
def draw_piece(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
