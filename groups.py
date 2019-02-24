from random import randint
import time
#This function creates groups of 2, based on the appreciations given, and the groups we have to form.
#Returns an array containing the groups, and another array containing the students left.
#TODO: change this whole algorithm
def createGroupsOfTwo(studentRanks, numberOfGroups):
    groupsOfTwo = []
    studentsLeft = []
    maxRank = 21
    for i in range(len(studentRanks)):
        studentsLeft.append(i)
    for i in range(numberOfGroups):
        isDisable, studentRanks = disableRank(studentsLeft, studentRanks, maxRank)
        if isDisable:
            maxRank = maximumRank(studentRanks)
        student = chooseStudent(studentRanks, maxRank)
        otherStudent = findOtherStudent(studentRanks, student)
        group = [student, otherStudent]
        print(group)
        groupsOfTwo.append(group)
        studentsLeft.remove(student)
        studentsLeft.remove(otherStudent)
        studentRanks = setStudentsPicked(group, studentRanks)
    return groupsOfTwo, studentsLeft

#Chooses a student based on his number of maxRank
#Returns a number, corresponding to a student in the matrix.
def chooseStudent(matrix, maxRank):
    studentsChosen = []
    print(maxRank)
    if maxRank == 1:
        return None
    for i in  range(len(matrix)):
        if matrix[i][maxRank] == 1:
            studentsChosen.append(i)
    if len(studentsChosen) >1:
        return distinguishStudents(studentsChosen, matrix, maxRank-1)
    elif len(studentsChosen)==0:
        return chooseStudent(matrix, maxRank-1)
    return studentsChosen[0]

#This function is used to separate students that have the same maxRank.
#Returns a number representing a student, distinguished from the others.
def distinguishStudents(studentList, matrix, maxRank):
    count = matrix[studentList[0]][maxRank]
    studentsChosen = []
    for i in studentList:
        if matrix[i][maxRank]>0:
            #If rank number is less than found before
            if matrix[i][maxRank] < count:
                studentsChosen = []
                studentsChosen.append(i)
                count = matrix[i][maxRank]
            #If rank number is equal to those already found
            elif matrix[i][maxRank] == count:
                studentsChosen.append(i)
    if len(studentsChosen) >1:
        return distinguishStudents(studentsChosen, matrix, maxRank-1)
    elif len(studentsChosen) == 0:
        return distinguishStudents(studentList, matrix, maxRank-1)
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
def findOtherStudent(studentRanks, stu):
    bestPicks = []
    rank = 0
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
        return distinguishStudents(bestPicks, studentRanks, rank-1)

def setStudentsPicked(students, studentRanks):
    for student in students:
        for i in range(len(studentRanks)):
            studentRanks[student][i] = -1
    return studentRanks