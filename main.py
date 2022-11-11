import numpy as np

ROW=6
COL=7

def create_connect4():
 board = np.zeros((6, 7))
 return board

## checks the last ROW if it's empty so that the move would be valid
def move_is_valid(board,COL):
    if board[ROW-1][col] == 0 :
        return True
    else:
        return print("invalid move")

## check if the ROW is empty so that we know where the player can play
def which_ROW(board,col):
    for r in range (ROW):
        if board[r][col] == 0:
            return r

def piece_drop(board,row,col,piece):
    board[row][col] =piece

def flip_board(board):
    board=np.flipud(board)
    print(board)
 ########################################################################################################################################################################################################################################################
turn=0
board=create_connect4()
flip_board(board)

game_done= False
while not game_done:


 if turn == 0:
    col=int(input("player 1 move between (0-6):"))
    if move_is_valid(board,col):
         row=which_ROW(board, col)
         piece_drop(board,row,col,1)
    turn += 1
    flip_board(board)

 else:
        col= int(input("player 2 move between (0-6):"))
        if move_is_valid(board,col):
            row=which_ROW(board, col)
            piece_drop(board,row,col,2)
        turn=0
        flip_board(board)






