import rangs, groups

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
NG3, NG2 = 0,0
if n%3 == 1:
    NG3 = (int)(n-4)/2
    NG2 = 2
elif n%3 == 2:
    NG3 = (int)(n-2)/3
    NG2 = 1
else:
    NG3 = n/3

print("NG3: ", NG3)
print("n-NG3", n-NG3)
students = createStudentsAppreciations()
studentRanks = rangs.attributeRanks(students)
printMatrix(studentRanks)
groupsOfTwo, studentsLeft = groups.createGroupsOfTwo(studentRanks, NG3, NG2, n)
print("groups of 2")
printMatrix(groupsOfTwo)
print("Students left:", studentsLeft)
#printMatrix(attributeRanks(createStudentsAppreciations()))