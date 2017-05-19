from itertools import permutations
import random
from GA import*

boardSize = 4 #Number of Queens
numPopulation = 10 # number of total population
population = [] # list of population
maxGen = 1000 # maximum genaration
permList = [] # list for permutation
fitnessList = []
totalFitness = 0
fitnessPercent = []


permList = list(permutations(range(0, boardSize)))
random.shuffle(permList)

# taking population
i = 0
while(i < numPopulation):
    population.append(permList[i])
    i += 1

# for i in population:
#     print(i)
testPop = [[0,1,2,3],[1,2,0,3],[3,2,0,1],[2, 1,0,3]]
# for i in testPop:
#     print(i)

print("=======================")



# print(testPop)
fitnessList = getFitness(population, boardSize)
totalFitness = getTotalFitness(fitnessList)
fitnessPercent = getFitnessPerc(fitnessList, boardSize, totalFitness)


print("====================== fitness list: ",fitnessList)
print("Total fitness: ", totalFitness)
print("fitness percent: ", fitnessPercent)

