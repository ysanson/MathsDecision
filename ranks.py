import sys
from random import randint

#Matrix of ranks
RANKS= [[21,20,18,15,11,6],
        [20,19,17,14,10,5],
        [18,17,16,13,9,4],
        [15,14,13,12,8,3],
        [11,10,9,8,7,2],
        [6,5,4,3,2,1]]

#Correlation between a rank and a line of the matrix
RANKS_CORRELATION={
    "TB":0,
    "B":1,
    "AB":2,
    "P":3,
    "I":4,
    "AR":5
}

#Students in a bi-dimensional array containing the students appreciations for each other.
#This function returns a bi-dimensional array containing the rank of each student's matching.
def attributeRanks(students):
    n = len(students)
    ME = [[-1] * n for _ in range(n)]
    for i in range(n):
        for j in range(i):
            markA = students[i][j]
            markB = students[j][i]
            rank = RANKS[RANKS_CORRELATION[markA]][RANKS_CORRELATION[markB]]
            ME[i][j] = ME[j][i] = rank
    return ME

#Counts the number of specific ranks a student have.
#Returns a matrix, 21*n, containing the count of ranks.
def countRanks(ME, n):
        NR = [[0] * n for _ in range(21)]
        for i in range(n):
                for j in range(n):
                        rank = ME[i][j]
                        NR[rank][i] += 1 
        return NR



