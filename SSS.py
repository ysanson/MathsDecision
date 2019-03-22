import sys
import src.fileOperations as fileOperations
import src.groups as groups
import src.ranks as ranks
import src.globals as glo


# This function prints a matrix on screen.
def printMatrix(matrix):
    for line in matrix:
        print(line)


# This function is the main of this script.
def main():
    print("Beginning SSS")
    glo.init()
    launch_mode = "exhaustif"
    number_results_max = None
    for arg in sys.argv[1:]:
        sub_arg = arg[2:]
        if sub_arg[:3] == "arg":
            launch_mode = sub_arg[4:]
        elif sub_arg[:3] == "num":
            number_results_max = sub_arg[7:]
        elif sub_arg[:3] == "ext":
            ext = sub_arg[4:]
    if number_results_max == None:
        number_results_max = -1
    fileName = "preferences" + ext + ".csv"
    print("Launching with arguments", launch_mode, number_results_max, ext)
    names, students = fileOperations.readAppreciationsCSV(fileName)
    n = len(students)
    ME = ranks.attributeRanks(students)
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

    division = []
    for group in groupsOfThree:
        division.append(group)
    for group in groupsOfTwo:
        division.append(group)
    glo.divisions.append(division)

    if len(glo.equalsStudentsList) > 1:
        if launch_mode == "exhaustif":
            if n <= 11:
                groups.createMultipledivisions(-1)
        elif launch_mode == "reel":
            groups.createMultipledivisions((int)(number_results_max))

    fileOperations.writeCSV(glo.divisions, names)
    print("Writing complete.\nEnd of SSS.")


main()
