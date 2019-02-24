from random import randint

#This function creates groups of 2, based on the appreciations given, and the groups we have to form.
#Returns an array containing the groups, and another array containing the students left.
#TODO: change this whole algorithm
def createGroupsOfTwo(studentRanks, ranksCount, numberOfGroups):
    groupsOfTwo = []
    studentsLeft = []
    maxRank = 21
    for i in range(len(studentRanks)):
        studentsLeft.append(i)
    for i in range(numberOfGroups):
        isDisable, studentRanks = disableRank(studentsLeft, studentRanks, maxRank)
        if isDisable:
            maxRank = maximumRank(studentRanks)
        student = chooseStudent(studentRanks, ranksCount, maxRank)
        print("Student : ", student)
        otherStudent = findOtherStudent(studentRanks, ranksCount, student)
        group = [student, otherStudent]
        print(group)
        groupsOfTwo.append(group)
        studentsLeft.remove(student)
        studentsLeft.remove(otherStudent)
        studentRanks = setStudentsPicked(group, studentRanks)
    return groupsOfTwo, studentsLeft

#Chooses a student based on his number of maxRank
#Returns a number, corresponding to a student in the matrix.
def chooseStudent(studentRanks, ranksCount, maxRank):
    studentsChosen = []
    print(maxRank)
    if maxRank == 1:
        return None
    for i in range(len(ranksCount)):
        if studentRanks[i][1] == -1:
            for j in range(22):
                ranksCount[i][j] =0
        if ranksCount[i][maxRank] == 1 and studentRanks[i][1] != -1:
            studentsChosen.append(i)
    print(studentsChosen)
    if len(studentsChosen) >1:
        student = distinguishStudents(studentsChosen, ranksCount, maxRank-1)
        if studentRanks[student][1] != -1:
            return student
        else:
            for i in range(22):
                ranksCount[student][i] = -1
            return chooseStudent(studentRanks, ranksCount, maxRank)
    elif len(studentsChosen)==0:
        return chooseStudent(studentRanks, ranksCount, maxRank-1)
    return studentsChosen[0]

#This function is used to separate students that have the same maxRank.
#Returns a number representing a student, distinguished from the others.
def distinguishStudents(studentList, ranksCount, maxRank):
    print("studentList[0] : ", studentList[0])
    print("maxRank : ", maxRank)
    count = ranksCount[studentList[0]][maxRank]
    studentsChosen = []
    for i in studentList:
        if ranksCount[i][maxRank]>0:
            #If rank number is less than found before
            if ranksCount[i][maxRank] < count and ranksCount[i][maxRank] != -1:
                studentsChosen = []
                studentsChosen.append(i)
                count = ranksCount[i][maxRank]
            #If rank number is equal to those already found
            elif ranksCount[i][maxRank] == count and ranksCount[i][maxRank] != -1:
                studentsChosen.append(i)
    if len(studentsChosen) >1:
        return distinguishStudents(studentsChosen, ranksCount, maxRank-1)
    elif len(studentsChosen) == 0:
        return distinguishStudents(studentList, ranksCount, maxRank-1)
    return studentsChosen[0]

#This function returns the maximum rank of the matrix.
def maximumRank(matrix):
    maxR = 0
    for i in range(22,0,-1):
        if matrix[0][i] != -1 and i>=maxR:
            maxR=i
    return maxR

#This function puts -1 to a rank if the students left doesn't have that rank.
def disableRank(studentsLeft, matrix, maxRank):
    isDisable = True
    for i in studentsLeft:
        if matrix[i][maxRank] != 0:
            isDisable = False
    if isDisable:
        for i in len(matrix):
            matrix[i][maxRank] = -1
    return isDisable, matrix

#This function searches the best student to form a group with the one in parameter.
#Returns a number, corresponding to the picked student.
def findOtherStudent(studentRanks, ranksCount, stu):
    bestPicks = []
    rank = 0
    print("stu : ", stu)
    for i in range(len(studentRanks)):
        if studentRanks[i][stu]>rank: #If we find a superior rank, we clear the picks and update the rank
            bestPicks=[]
            rank = studentRanks[i][stu]
            bestPicks.append(i)
        elif studentRanks[i][stu] == rank: #If we find someone with the same rank, we add him to the list
            bestPicks.append(i)
    if len(bestPicks) == 1:
        return bestPicks[0]
    elif len(bestPicks) > 1:
        return distinguishStudents(bestPicks, ranksCount, rank-1)

def setStudentsPicked(students, studentRanks):
    for student in students:
        for i in range(len(studentRanks)):
            studentRanks[student][i] = -1
    return studentRanks