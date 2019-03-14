import sys

import copy
import math
import random
import time

#These are the initial variables we have to set
#For best performance pop_size = 100 mutation rate = 0.1
board_size = 50
population_size = 100
generations = 100000
mutation_rate = .1


#DO NOT MODIFY THESE VARIABLES
goal = board_size * (board_size-1) /2 #Goal fitness
count = 0 #Counter for how many generations we have
populations = [] #List to store all our boards
totalFitness = 0 #Total Fitness of Population(For Roulette Selection)
nextPopulation = [] #List that hold children


class Board:
	def __init__(self):
		self.board_size = board_size
		self.goal = goal
		self.fitness = self.goal
		self.mutation_rate = mutation_rate
		#This will generate a list containing (0,1,2,3,4,5,6,7,..n)
		self.queens = list(range(board_size))
		random.shuffle(self.queens)

		#We've initialized a board, that has placed all the queens randomly at some place
	def setQueens(self,queenList):
		self.queens = queenList
	
	#A mutation will take place according to the mutation rate
	#A mutation is just the switching of two queen positions.
	def mutate(self):
		if random.randrange(1/self.mutation_rate) == 1: #This is just a way to express the probability of mutation
			j = random.randrange(self.board_size)
			k = random.randrange(self.board_size)
			temp = self.queens[j]
			self.queens[j] = self.queens[k]
			self.queens[k] = temp
			

	
	#Fitness is computed through a very simple function
	#This function I got through an online article
	#If the below mathematical statement is true, then the fitness is lowered because
	#there is a conflict
	def compute_fitness(self):
		for i in range(self.board_size):
			for j in range(i+1,self.board_size):
				if math.fabs(self.queens[i] - self.queens[j]) == math.fabs(j -i):
					self.fitness -= 1

	#Simple function to print the board
	#This was copied from stackoverflow
	def print_board(self):
		for row in range(self.board_size):
			print("",end="|")
			queen = self.queens.index(row)
			for col in range(self.board_size):
				if col == queen:
					print("Q",end="|")
				else:
					print("_",end="|")
			print ("")
		





def create_board():
	for i in range(population_size):
		populations.append(Board())

def printPopulation(populations):
	for boards in populations:
		print(boards.fitness,boards.queens)

def getFitness(totalFitness):
	for boards in populations:
		boards.compute_fitness()
		totalFitness += boards.fitness
		
def sortBoards():
	#This is an easy method to sort a list of objects by a key attribute, in this case fitness
	populations.sort(key=lambda x: x.fitness, reverse=True)

def makeCrossover(populations):
	population1 = populations[int(0):int(population_size/2)]
	population2 = populations[::-1]
	population2 = population2[0:int(population_size/2)]
	i = 0
	for i in range(len(population1)):
		nextPopulation.append(crossover(population1[i].queens,population2[i].queens))
		

def crossover(board1, board2):
	pos = random.randrange(board_size)
	
	firstSlice = board1[:pos]
	secondSlice = board2[pos:]
	#firstSlice.extend(secondSlice)
	#print(firstSlice)
	newChild = firstSlice + secondSlice
	
	#Here we check if each item in this list is unique
	#If it is not unique we will have the change it
	newChild = changeListToUnique(newChild)
	
	newBoard = Board()
	newBoard.setQueens(newChild)
	return newBoard
	


#I got this from somebody at stackoverflow
def changeListToUnique(l):
	for num in l:
		if l.count(num) > 1:
			ix = l.index(num)
			missing = [n for n in range(len(l)) if n not in set(l)]
			try:
				l[ix] = missing.pop(0)
			except IndexError:
				break
	return l

def rouletteSelection(population):
        max     = sum([c.fitness for c in population])
        pick    = random.uniform(0, max)
        current = 0
        for chromosome in population:
            current += chromosome.fitness
            if current > pick:
                return chromosome

#Next generation selection, select half of the population for next parents
#Initialize the board


start_time = time.time()
create_board()
while(count < generations):
	
	#After 1000 generations, start over
	#++++++++++++++++++++++++++++++++++++++++
	#This code is if you want to start fresh after 1000 generations
	#if count % 1000 == 0:
	# 	create_board()
	#++++++++++++++++++++++++++++++++++++++++
	
	
	#Calculate fitness for all populations
	getFitness(totalFitness)
	#Sort boards by fitness
	sortBoards()
	
	#Every 10 print our current board + fitness
	if count % 10 == 0:
		print(populations[0].fitness,populations[0].queens)
	
	if (populations[0].fitness == goal):
		print ("Final Board is")
		populations[0].print_board()
		print ("Completed in ",count," generations")
		print ("Board Size: ", board_size)
		print ("Population Size: ", population_size)
		print ("Mutation Rate: ", mutation_rate)
		break
	
	
	#This is just regular selection of the best half of the population
	#split the list so we get the best population_size/2 boards
	parentPopulation = populations[:int(population_size/2)]
	
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# This code is for roulette selection, however I do not recommend it
	#parentPopulation = []
	#for i in range(int(population_size/2)):
	#	parentPopulation.append(rouletteSelection(populations))
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	
	#Make Crossovers and put them into nextPopulation
	makeCrossover(parentPopulation)
	
	populations = []
	populations.extend(parentPopulation)
	#Our nextgeneration is now ready
	populations.extend(nextPopulation)
	#Mutate Our boards
	for board in populations:
		board.mutate()
	
	nextPopulation = []
	parentPopulation = []
	count+=1
	
print("Solution Took %s seconds ---" % (time.time() - start_time))
