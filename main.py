import ranks, groups, fileOperations

#This function returns a matrix containing the student's appreciation for each other.
def createStudentsAppreciations():
    return fileOperations.readAppreciationsCSV() 

#This function prints a matrix on screen.
def printMatrix(matrix):
    for line in matrix:
        print(line)

names, students = createStudentsAppreciations()
n = len(students)
ME = ranks.attributeRanks(students)
printMatrix(ME)
NR = ranks.countRanks(ME, n)
nbBinomes, nbTrinomes=0,0
if n<36:
    if n%2==0:
        nbBinomes, nbTrinomes = n/2, 0
    else:
        nbBinomes, nbTrinomes = (n-3)/2, 1 
else:
    nbTrinomes = n-36
    nbBinomes = 18-nbTrinomes

printMatrix(NR)
groupsOfTwo, studentsLeft = groups.createGroupsOfTwo(ME, NR, (nbBinomes+nbTrinomes))
print("groups of 2")
printMatrix(groupsOfTwo)
print("Students left:", studentsLeft)
