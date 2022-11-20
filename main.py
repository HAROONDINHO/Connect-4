import random
import numpy as np
from numpy import int8
import pygame
import sys
import math
from tkinter import *
from tkinter import messagebox
import copy
import time
from treelib import Node, Tree

ROW_COUNT = 6
COL_COUNT = 7
scope_length = 4
EMPTY = 0
PLAYER = 0
PLAYER_PIECE = 1
AI = 1
AI_PIECE = 2

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SKY_BLUE = (11, 214, 214)

new_np = np.zeros((6, 7), dtype=int8)

mm_tree = Tree()
treeroot = mm_tree.create_node("Root", "root")

## operations on binary representation of the board
def bin_to_np(bin_board):
    global new_np
    new_np = np.zeros((6, 7), dtype=int8)
    for i in range(7):
        for j in range(((7<<(60-9*i))&bin_board)>>(60-9*i)):
            new_np[j, i] = (((1 << (59 - 9 * i - j) ) & (bin_board)) >> (59 - 9 * i - j))+1
    return new_np


def np_to_bin(np_board):
    new_bin = 9223372036854775808
    rows_count = [0, 0, 0, 0, 0, 0, 0]
    for i in range(7):
        x = which_ROW(np_board, i)
        if x == None:
            rows_count[i] = 6
        else:
            rows_count[i] = x
    for i in range(7):
        new_bin = new_bin|(rows_count[i]<<(60-9*i))
    cols_content = []
    for i in range(7):
        cols_content.append(list(np_board[:, i]))
    for i in range(7):
        for j in range(rows_count[i]):
            if(cols_content[i][j]==AI_PIECE):
                new_bin = new_bin|(1<<(59-9*i-j))
    return new_bin


def bin_game_done(bin_board):
    k = 0
    for i in range(COL_COUNT):
        if((((7<<(60-9*i))&bin_board)>>(60-9*i)) <= 5):
            k+=1
            break
    if (k == 0):
        return True
    else:
        return False

def bin_valid_locations(bin_board):
    valid = []
    for c in range(COL_COUNT):
        if ((((7<<(60-9*c))&bin_board)>>(60-9*c)) <= 5):
            valid.append(c)
    return valid


def bin_piece_drop(bin_board, row, col, piece):
    # update row count for the column
    new_bin_which_ROW = (((7<<(60-9*col))&bin_board)>>(60-9*col)) + 1
    temp = bin_board&(~(7<<(60-(9*col))))
    bin_board = ((bin_board>>(60-9*col)))
    bin_board = (((bin_board&8)|new_bin_which_ROW)<<(60-9*col))|temp
    # update position
    if piece==AI_PIECE:
        bin_board = bin_board|(1<<(59-(9*col)-row))
    else:
        bin_board = bin_board&~(1<<(59-(9*col)-row))
    return bin_board

#####################################################################################################################

def create_connect4():
    board = np.zeros((ROW_COUNT, COL_COUNT), dtype=int8)
    return board


## checks the last ROW if it's empty so that the move would be valid
def move_is_valid(board, COL):
    if board[ROW_COUNT - 1][COL] == 0:
        return True


## check if the ROW is empty so that we know where the player can play
def which_ROW(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r


def piece_drop(board, row, col, piece):
    board[row][col] = piece


def game_done(board):
    k = 0
    for i in range(COL_COUNT):
        if (board[5][i] == 0):
            k += 1
    if (k == 0):
        return True
    else:
        return False


def score_scope(scope, piece):
    score_sum = 0
    if piece == AI_PIECE:
        opp_piece = PLAYER_PIECE
    else:
        opp_piece = AI_PIECE

    if scope.count(piece) == 4:
        score_sum += 100
    elif scope.count(piece) == 3 and scope.count(EMPTY) == 1:
        score_sum += 55
    elif scope.count(piece) == 2 and scope.count(EMPTY) == 2:
        score_sum += 2

    if scope.count(opp_piece) == 4:
        score_sum -= 200
    elif scope.count(opp_piece) == 3 and scope.count(EMPTY) == 1:
        score_sum -= 100
    return score_sum



def score(board, piece):
    score_sum = 0
    #center dom
    center = [int(i) for i in list(board[:, COL_COUNT//2])]
    center_count = center.count(piece)
    score_sum += center_count*10
    #horizontal scores
    for r in range(ROW_COUNT):
        row = [int(i) for i in list(board[r,:])]
        for c in range(COL_COUNT-3):
            scope = row[c:c+scope_length]
            score_sum += score_scope(scope, piece)
    #vertical_scores
    for c in range(COL_COUNT):
        col = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            scope = col[r:r+scope_length]
            score_sum += score_scope(scope, piece)
    #+ve diagonal scores
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            scope = [board[r+i][c+i] for i in range(scope_length)]
            score_sum += score_scope(scope, piece)
    #-ve diagonal scores
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            scope = [board[r+3-i][c+i] for i in range(scope_length)]
            score_sum += score_scope(scope, piece)

    return score_sum



def final_score(board):
    sum1 = 0 #player score
    sum2 = 0 #ai score
    piece1 = PLAYER_PIECE

    #vertical check
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == board[r][c + 1] and board[r][c] == board[r][c + 2] and board[r][c] == board[r][c + 3]:
                if board[r][c] == piece1:
                    sum1 += 1
                else:
                    sum2 += 1
    #horizontal check
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == board[r + 1][c] and board[r][c] == board[r + 2][c] and board[r][c] == board[r + 3][c]:
                if board[r][c] == piece1:
                    sum1 += 1
                else:
                    sum2 += 1
    #+ve diagonal check
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == board[r + 1][c + 1] and board[r][c] == board[r + 2][c + 2] and board[r][c] ==
                    board[r + 3][c + 3]):
                if board[r][c] == piece1:
                    sum1 += 1
                else:
                    sum2 += 1
    # -ve diagonal check
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (board[r][c] == board[r - 1][c + 1] and board[r][c] == board[r - 2][c + 2] and board[r][c] == board[r - 3][c + 3]):
                if board[r][c] == piece1:
                    sum1 += 1
                else:
                    sum2 += 1

    return sum1, sum2

node_count = 0

def minimax(board, depth, maxplayer, root):
    global mm_tree
    global node_count
    if depth == 0 or bin_game_done(board):
        if bin_game_done(board):
            temp = bin_to_np(board)
            s1, s2 = final_score(temp)
            if s2 > s1:
                return (None, 10000000000)
            elif s1 > s2:
                return (None, -10000000000)
            else:
                return (None, 0)
        else: #depth is 0
            return (None, score(bin_to_np(board), AI_PIECE))
    locations = bin_valid_locations(board)
    if maxplayer: #maxplayer
        value = -math.inf
        column = random.choice(locations)
        for col in locations:
            row = (((7<<(60-9*col))&board)>>(60-9*col))
            parent_id = root.identifier
            parent = mm_tree.create_node(col, node_count, parent=root)
            node_count+=1
            temp = bin_piece_drop(board, row, col, AI_PIECE)
            new_value = minimax(temp, depth-1, False, parent)[1]
            parent = mm_tree.get_node(nid=parent_id)
            if new_value > value:
                value = new_value
                column = col
        return column, value

    else: #minplayer
        value = math.inf
        column = random.choice(locations)
        for col in locations:
            row = ((7<<(60-9*col))&board)>>(60-9*col)
            parent_id = root.identifier
            parent = mm_tree.create_node(col, node_count, parent=root)
            node_count += 1
            temp = bin_piece_drop(board, row, col, PLAYER_PIECE)
            new_value = minimax(temp, depth - 1, True, parent)[1]
            parent = mm_tree.get_node(nid=parent_id)
            if new_value < value:
                value = new_value
                column = col
        return column, value


def minimax_pruning(board, depth, alpha, beta, maxplayer, root):
    global mm_tree
    global node_count
    if depth == 0 or bin_game_done(board):
        if bin_game_done(board):
            s1, s2 = final_score(bin_to_np(board))
            if s2 > s1:
                return (None, 10000000000)
            elif s1 > s2:
                return (None, -10000000000)
            else:
                return (None, 0)
        else: #depth is 0
            return (None, score(bin_to_np(board), AI_PIECE))
    locations = bin_valid_locations(board)
    if maxplayer: #maxplayer
        value = -math.inf
        column = locations[len(locations)//2]
        for col in locations:
            row = (((7<<(60-9*col))&(board))>>(60-9*col))
            parent_id = root.identifier
            parent = mm_tree.create_node(col, node_count, parent=root)
            node_count += 1
            temp = bin_piece_drop(board, row, col, AI_PIECE)
            new_value = minimax_pruning(temp, depth-1, alpha, beta, False, parent)[1]
            parent = mm_tree.get_node(nid=parent_id)
            if new_value > value:
                value = new_value
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: #minplayer
        value = math.inf
        column = locations[len(locations)//2]
        for col in locations:
            row = (((7<<(60-9*col))&board)>>(60-9*col))
            parent_id = root.identifier
            parent = mm_tree.create_node(col, node_count, parent=root)
            node_count += 1
            temp = bin_piece_drop(board, row, col, PLAYER_PIECE)
            new_value = minimax_pruning(temp, depth - 1, alpha, beta,True, parent)[1]
            parent = mm_tree.get_node(nid=parent_id)
            if new_value < value:
                value = new_value
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value




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


########################################################################################################################################################################################################################################################

board = create_connect4()

root = Tk()
root.title('On/Off Prunning!')
root.geometry("500x300")
is_on = True

my_label = Label(root,
                 text="The prunning Is On!",
                 fg="green",
                 font=("Helvetica", 32))

my_label.pack(pady=20)

def switch():
    global is_on
    if is_on:
        on_button.config(image=off)
        my_label.config(text="The prunning is Off!",fg="grey")
        is_on = False
    else:

        on_button.config(image=on)
        my_label.config(text="The prunning is On!", fg="green")
        is_on = True

on = PhotoImage(file="on.png")
off = PhotoImage(file="off.png")
on_button = Button(root, image=on, bd=0,
                   command=switch)
on_button.pack(pady=50)
root.mainloop()


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

while not game_done(board):
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

                    if game_done(board):
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

                    draw_board(board)
                    turn = AI
                    if game_done(board):
                        pygame.time.wait(5000)

                else:
                    label = myfont.render("please choose a valid location", 1, RED)
                    screen.blit(label, (10, 10))
                    continue

    bin_board = np_to_bin(board)
    if turn == AI and not bin_game_done(bin_board):

        time0 = time.time()
        if is_on:
            col, minimax_score = minimax_pruning(bin_board, 4, -math.inf, math.inf, True, treeroot)
        else:
            col, minimax_score = minimax(bin_board, 5, True, treeroot)
        mm_tree.show()
        print(f"\n{time.time()-time0}\n")


        if move_is_valid(board, col):
            row = which_ROW(board, col)
            piece_drop(board, row, col, AI_PIECE)

            if game_done(board):
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

            draw_board(board)
            turn = PLAYER
            if game_done(board):
                pygame.time.wait(5000)
        else:
            continue



