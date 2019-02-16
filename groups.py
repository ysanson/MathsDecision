from random import randint

#This function creates groups of 2, based on the appreciations given, and the groups we have to form.
#Returns an array containing the groups, and another array containing the students left.
def createGroupsOfTwo(studentRanks, NG3, NG2, n):
    groupsOfTwo = []
    studentWeight = []
    for i in range(n):
        studentWeight.append(sum(studentRanks[i]))
    studentsLeft = []
    for i in range(n):
        studentsLeft.append(i)
    stu = randint(0, n)
    while len(studentsLeft) > NG3:
        maxRank = -1
        studentToPick = -1
        while stu not in studentsLeft:
            stu = randint(0, n)
        for i in range(n):
            if i in studentsLeft and i != stu:
                if studentRanks[stu][i] == 21:
                    groupsOfTwo.append([stu, i])
                    studentsLeft.remove(stu)
                    studentsLeft.remove(i)
                elif maxRank < studentRanks[stu][i]:
                    maxRank = studentRanks[stu][i]
                    studentToPick = i
        groupsOfTwo.append([stu, studentToPick])
        studentsLeft.remove(stu)
        studentsLeft.remove(studentToPick)
    return groupsOfTwo, studentsLeft
