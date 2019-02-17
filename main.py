import rangs, groups, fileOperations


#This function returns a matrix containing the student's appreciation for each other.
def createStudentsAppreciations():
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
ME = rangs.attributeRanks(students)
printMatrix(ME)
NR = rangs.countRanks(ME, n)
printMatrix(NR)
groupsOfTwo, studentsLeft = groups.createGroupsOfTwo(ME, n)
print("groups of 2")
printMatrix(groupsOfTwo)
print("Students left:", studentsLeft)