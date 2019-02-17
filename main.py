import ranks, groups, fileOperations


#This function returns a matrix containing the student's appreciation for each other.
def createStudentsAppreciations():
    #fileOperations.readAppreciationsCSV()
    students = [[-1,"B","TB","TB","B"],
                ["TB", -1, "B", "B", "P"],
                ["AB", "B", -1, "AB", "B"],
                ["P", "P", "B", -1, "B"],
                ["B", "I", "TB", "B", -1]]
    return students

#This function prints a matrix on screen.
def printMatrix(matrix):
    for line in matrix:
        print(line)


students = createStudentsAppreciations()
n = len(students)
ME = ranks.attributeRanks(students)
printMatrix(ME)
NR = ranks.countRanks(ME, n)
nbBinomes, nbTrinomes=0,0
if n/2>18:
    nbTrinomes = n-36
    nbBinomes = 18-nbTrinomes
else:
    nbBinomes, nbTrinomes = n/2, 0 
printMatrix(NR)
groupsOfTwo, studentsLeft = groups.createGroupsOfTwo(ME, n)
print("groups of 2")
printMatrix(groupsOfTwo)
print("Students left:", studentsLeft)