
from itertools import permutations
import random

def getFitness(popu, boardSize):
    fitnessList = [] # list hold fitness for all populations
    board = [[0 for x in range(boardSize)] for y in range(boardSize)]


    for tuple in popu:
        fitness = 0
        conflict = 0 # count number of attacking conflict on board
        col = 0

        placeQueensOnBoard(tuple,board) # call this function to place queens on board
        for row in tuple: # get row conflict
            print("row: ", row, "col: ",col)
            conflict += countRowConflict(row, board)
            conflict += countAttackDiagonalRight(row,col,board, boardSize)
            conflict += countAttackDiagonalLeft(row,col,board, boardSize)
            col += 1 #to keep track of column number

        print("Total conflict: ",conflict)
        fitness = boardSize*(boardSize - 1) - conflict
        fitnessList.append(fitness)

        print("fitness: ",fitness)

        for i in board:
            print(i)
        board = [[0 for x in range(boardSize)] for y in range(boardSize)]


    return fitnessList

def countRowConflict(row, board):
    numAttack = 0
    col = 0
    while(col < len(board)):
        if(board[row][col] == 1):
            numAttack += 1
        col += 1
    numAttack -= 1 #this one queen itself
    return numAttack

#----------------------------- attack in right diagonal -----------------------------
def countAttackDiagonalRight(row, col, board, boardSize):
    numAttacks = 0
    colStart = col - row
    rowStart = 0
    if(colStart < 0):
        rowStart += (-colStart)
        colStart = 0

    i = rowStart
    j = colStart
    while(i < boardSize and j < boardSize):
        if(board[i][j] == 1):
            numAttacks += 1
        i += 1
        j += 1
    numAttacks -= 1

    print('attack in right dia: ',numAttacks)
    return numAttacks

# ---------------------------- attacks in left diagonal ----------------------------
def countAttackDiagonalLeft(row, col, board,boardSize):
    numAttacks = 0

    colStart = col + row
    rowStart = 0
    if(colStart >= boardSize):
        rowStart += (colStart - boardSize + 1)
        colStart = boardSize - 1

    i = rowStart
    j = colStart
    while(i < boardSize and j >= 0):
        if(board[i][j] == 1):
            numAttacks += 1
        i += 1
        j -= 1
    numAttacks -= 1

    print('attack in Left dia: ',numAttacks)
    return numAttacks



def placeQueensOnBoard(tuple,board):
    col = 0
    for row in tuple:
        board[row][col] = 1
        col += 1

def getTotalFitness(fitnessList):
    total = 0
    for i in fitnessList:
        total += i
    return total

def getFitnessPerc(fitnessList, boardSize, totalFitness):
    fitnessPer = []

    for i in fitnessList:
        fitnessPer.append((i/totalFitness)*100)

    return fitnessPer