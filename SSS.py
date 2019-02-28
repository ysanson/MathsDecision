import sys
import src.fileOperations as fileOperations
import src.groups as groups
import src.ranks as ranks


# This function prints a matrix on screen.
def printMatrix(matrix):
    for line in matrix:
        print(line)


# This function is the main of this script.
def main():
    ext = sys.argv[1][1:]
    fileName = "preferences" + ext + ".csv"
    names, students = fileOperations.readAppreciationsCSV(fileName)
    n = len(students)
    ME = ranks.attributeRanks(students)
    printMatrix(ME)
    NR = ranks.countRanks(ME, n)
    nbBinomes, nbTrinomes = 0, 0
    if n < 36:
        if n % 2 == 0:
            nbBinomes, nbTrinomes = (int)(n / 2), 0
        else:
            nbBinomes, nbTrinomes = (int)((n - 3) / 2), 1
    else:
        nbTrinomes = n - 36
        nbBinomes = 18 - nbTrinomes
    groupsOfTwo, studentsLeft = groups.createGroupsOfTwo(ME, NR, (nbBinomes + nbTrinomes))
    groupsOfThree = []
    if nbTrinomes >= 1:
        groupsOfTwo, groupsOfThree = groups.createGroupsOfThree(groupsOfTwo, studentsLeft, ME)
    print("Final results :")
    print("Groups of 2 : ")
    printMatrix(groupsOfTwo)
    print("Groups of 3 : ")
    printMatrix(groupsOfThree)
    print("Writing CSV...")
    repartitions = []
    repartition = []
    for group in groupsOfThree:
        repartition.append(group)
    for group in groupsOfTwo:
        repartition.append(group)
    repartitions.append(repartition)
    fileOperations.writeCSV(repartitions, names)
    print("Writing complete.\nEnd of the script.")


main()
