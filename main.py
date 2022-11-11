import numpy as np
from numpy import int8

ROW_COUNT=6
COL_COUNT=7

def create_connect4():
 board = np.zeros((ROW_COUNT, COL_COUNT), dtype=int8)
 return board

## checks the last ROW if it's empty so that the move would be valid
def move_is_valid(board,COL):
    if board[ROW_COUNT - 1][col] == 0 :
        return True
    else:
        print("please choose a valid location")


## check if the ROW is empty so that we know where the player can play
def which_ROW(board,col):
    for r in range (ROW_COUNT):
        if board[r][col] == 0:
            return r

def piece_drop(board,row,col,piece):
    board[row][col] =piece

def flip_board(board):
    board=np.flipud(board)
    print(board)

def game_done():
    k=0
    for i in range (COL_COUNT):
        if (board[5][i]==0):
            k+=1
    if (k==0):
        return True
    else:
        return False



def final_score(board):
    sum1=0
    sum2=0
    piece1=1
    piece2=2

    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
           if (board[r][c] == board[r][c + 1] and board[r][c] ==  board[r][c +2]  and board[r][c] ==  board[r][c +3]):
               if (board[r][c]==piece1):
                   sum1+=1
               else:
                   sum2+=1
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == board[r + 1][c] and board[r][c]== board[r + 2][c] and board[r][c]  ==board[r + 3][c]  ) :
                if (board[r][c] == piece1):
                    sum1 += 1
                else:
                    sum2 += 1

    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] ==  board[r + 1][c + 1]  and board[r][c]== board[r + 2][c + 2]  and board[r][c]== board[r + 3][c + 3]):
                if (board[r][c] == piece1):
                    sum1 += 1
                else:
                    sum2 += 1
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (board[r][c] == board[r - 1][c + 1]  and board[r][c]==board[r - 2][c + 2] and board[r][c]== board[r - 3][c + 3] ):
                if (board[r][c] == piece1):
                    sum1 += 1
                else:
                    sum2 += 1

    return sum1,sum2



 ########################################################################################################################################################################################################################################################
turn=0
board=create_connect4()
flip_board(board)
while not (game_done()):

 if turn == 0:
    col=int(input("player 1 move: "))
    if (col>6 or col<0):
        print("invalid location")
        continue
    if move_is_valid(board,col):
         row=which_ROW(board, col)
         piece_drop(board,row,col,1)
    else:
        continue
    turn += 1
    flip_board(board)



 else:
    col= int(input("player 2 move: "))
    if (col>6 or col<0):
        print("invalid location")
        continue
    if  move_is_valid(board,col):
        row=which_ROW(board, col)
        piece_drop(board,row,col,2)
    else:
        continue

    turn=0
    flip_board(board)


s1,s2= final_score(board)
print(s1,s2)
if (s1>s2):
    print(f"player 1 wins score = {s1-s2}")
elif (s1<s2):
    print(f"player 2 wins score = {s2-s1}")
else:
    print(f"draw {s1}--{s2}")









