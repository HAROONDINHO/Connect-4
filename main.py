import random

import numpy as np
from numpy import int8
import pygame
import sys
import math
from tkinter import *
from tkinter import messagebox

ROW_COUNT = 6
COL_COUNT = 7
PLAYER = 0
PLAYER_PIECE = 1
AI = 1
AI_PIECE = 2

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SKY_BLUE = (11, 214, 214)


def create_connect4():
    board = np.zeros((ROW_COUNT, COL_COUNT), dtype=int8)
    return board


## checks the last ROW if it's empty so that the move would be valid
def move_is_valid(board, COL):
    if board[ROW_COUNT - 1][col] == 0:
        return True


## check if the ROW is empty so that we know where the player can play
def which_ROW(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def piece_drop(board, row, col, piece):
    board[row][col] = piece


def flip_board(board):
    board = np.flipud(board)


def game_done():
    k = 0
    for i in range(COL_COUNT):
        if (board[5][i] == 0):
            k += 1
    if (k == 0):
        return True
    else:
        return False


def score(board):
    pass


def final_score(board):
    sum1 = 0
    sum2 = 0
    piece1 = PLAYER_PIECE

    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == board[r][c + 1] and board[r][c] == board[r][c + 2] and board[r][c] == board[r][c + 3]:
                if board[r][c] == piece1:
                    sum1 += 1
                else:
                    sum2 += 1
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == board[r + 1][c] and board[r][c] == board[r + 2][c] and board[r][c] == board[r + 3][c]:
                if board[r][c] == piece1:
                    sum1 += 1
                else:
                    sum2 += 1

    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == board[r + 1][c + 1] and board[r][c] == board[r + 2][c + 2] and board[r][c] ==
                    board[r + 3][c + 3]):
                if board[r][c] == piece1:
                    sum1 += 1
                else:
                    sum2 += 1
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (board[r][c] == board[r - 1][c + 1] and board[r][c] == board[r - 2][c + 2] and board[r][c] ==
                    board[r - 3][c + 3]):
                if board[r][c] == piece1:
                    sum1 += 1
                else:
                    sum2 += 1

    return sum1, sum2


def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


# #######################################################################################################################################################################################################################################################
board = create_connect4()
flip_board(board)

# root = Tk()
#
# root.title('On/Off Prunning!')
#
#
# root.geometry("500x300")
# is_on = True
# my_label = Label(root,
#                  text="The prunning Is On!",
#                  fg="green",
#                  font=("Helvetica", 32))
#
# my_label.pack(pady=20)
#
# def switch():
#     global is_on
#     if is_on:
#         on_button.config(image=off)
#         my_label.config(text="The prunning is Off!",
#                         fg="grey")
#         is_on = False
#     else:
#
#         on_button.config(image=on)
#         my_label.config(text="The prunning is On!", fg="green")
#         is_on = True
#
# on = PhotoImage(file="on.png")
# off = PhotoImage(file="off.png")
# on_button = Button(root, image=on, bd=0,
#                    command=switch)
# on_button.pack(pady=50)
# root.mainloop()

pygame.init()
SQUARESIZE = 125
width = COL_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)
screen = pygame.display.set_mode(size)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 40)
turn = random.randint(PLAYER, AI)

while not game_done():

    draw_board(board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if move_is_valid(board, col):
                    row = which_ROW(board, col)
                    piece_drop(board, row, col, PLAYER_PIECE)

                    if game_done():
                        s1, s2 = final_score(board)
                        if s1 > s2:
                            label = myfont.render(f"HUMAN wins!! {s1} - {s2}", 1, RED)
                            screen.blit(label, (40, 10))

                        elif s1 < s2:
                            label = myfont.render(f"AI wins!! {s2} - {s1}", 1, YELLOW)
                            screen.blit(label, (40, 10))

                        else:
                            label = myfont.render(f"TIE {s1} - {s2}", 1, SKY_BLUE)
                            screen.blit(label, (40, 10))

                    flip_board(board)
                    draw_board(board)
                    turn = AI
                    if game_done():
                        pygame.time.wait(5000)

                else:
                    label = myfont.render("please choose a valid location", 1, RED)
                    screen.blit(label, (10, 10))
                    continue

    if turn == AI and not game_done():

        col = random.randint(0, COL_COUNT-1)

        if move_is_valid(board, col):
            row = which_ROW(board, col)
            piece_drop(board, row, col, AI_PIECE)

            if game_done():
                s1, s2 = final_score(board)
                if s1 > s2:
                    label = myfont.render(f"HUMAN wins!! {s1} - {s2}", 1, RED)
                    screen.blit(label, (40, 10))

                elif s1 < s2:
                    label = myfont.render(f"AI wins!! {s2} - {s1}", 1, YELLOW)
                    screen.blit(label, (40, 10))

                else:
                    label = myfont.render(f"TIE {s1} - {s2}", 1, SKY_BLUE)
                    screen.blit(label, (40, 10))

            flip_board(board)
            draw_board(board)
            turn = PLAYER
            if game_done():
                pygame.time.wait(5000)
        else:
            continue



