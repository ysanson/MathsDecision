import csv, sys
import fileOperations, groupsMulti, ranks

#This function prints a matrix on screen.
def printMatrix(matrix):
    for line in matrix:
        print(line)

#TODO: complete this function
def createRepartition(groupsOfTwo, studentsLeft, chosenStudent, nbBinomes, nbTrinomes):
    return 0

if __name__ == "__main__":
    ext = sys.argv[1][1:]
    fileName = "preferences"+ext+".csv"
    names, students = fileOperations.readAppreciationsCSV(fileName)
    n = len(students)
    ME = ranks.attributeRanks(students)
    NR = ranks.countRanks(ME, n)
    nbBinomes, nbTrinomes=0,0
    if n<36:
        if n%2==0:
            nbBinomes, nbTrinomes = (int)(n/2), 0
        else:
            nbBinomes, nbTrinomes = (int)((n-3)/2), 1 
    else:
        nbTrinomes = n-36
        nbBinomes = 18-nbTrinomes
    groupsOfTwo, studentsLeft = groupsMulti.createGroupsOfTwo(ME, NR, (nbBinomes+nbTrinomes))
    groupsOfThree=[]
    print("Groups of 2 : ")
    printMatrix(groupsOfTwo)
    print("Students left : ", studentsLeft)
    if nbTrinomes>=1:
        groupsOfTwo, groupsOfThree = groupsMulti.createGroupsOfThree(groupsOfTwo, studentsLeft, ME)
    print("Final results :")
    print("Groups of 2 : ")
    printMatrix(groupsOfTwo)
    print("Groups of 3 : ")
    printMatrix(groupsOfThree)
    print("Writing CSV...")
    fileOperations.writeCSV(groupsOfTwo, groupsOfThree, names)
    print("Writing complete.\nEnd of the script.")