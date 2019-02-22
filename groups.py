from random import randint

#This function creates groups of 2, based on the appreciations given, and the groups we have to form.
#Returns an array containing the groups, and another array containing the students left.
#TODO: change this whole algorithm
def createGroupsOfTwo(studentRanks, n):
    groupsOfTwo = []
    studentsLeft = []
    stu = randint(0, n)
    while len(studentsLeft) > n: #TODO: change this statement
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

#Chooses a student based on his number of maxRank
#Returns a number, corresponding to a student in the matrix.
def chosenStudent(matrix, maxRank):
    studentsChosen = []
    if maxRank ==1:
        return None
    for i in  range(len(matrix)):
        if matrix[i][maxRank] == 1:
            studentsChosen.append(i)
    if len(studentsChosen) >1:
        #TODO: modifier
        return distinguishStudents(studentsChosen, matrix, maxRank-1)
    elif len(studentsChosen)==0:
        return chosenStudent(matrix, maxRank-1)
    return studentsChosen[0]

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
    elif len(studentsChosen==0):
        return distinguishStudents(studentList, matrix, maxRank-1)
    return studentsChosen[0]

def maximumRank(matrix):
    maxR = 0
    for i in range(22,0,-1):
        if matrix[0][i] != -1 and i>=maxR:
            maxR=i
    return maxR
