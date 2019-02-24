from random import randint

#This function creates groups of 2, based on the appreciations given, and the groups we have to form.
#Returns an array containing the groups, and another array containing the students left.
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
        otherStudent = findOtherStudent(studentRanks, ranksCount, student)
        group = [student, otherStudent]
        groupsOfTwo.append(group)
        studentsLeft.remove(student)
        studentsLeft.remove(otherStudent)
        studentRanks = setStudentsPicked(group, studentRanks)
    return groupsOfTwo, studentsLeft

#Chooses a student based on his number of maxRank
#Returns a number, corresponding to a student in the matrix.
def chooseStudent(studentRanks, ranksCount, maxRank):
    studentsChosen = []
    if maxRank == 1:
        return None
    for i in range(len(ranksCount)):
        if studentRanks[i][1] == -1:
            for j in range(22):
                ranksCount[i][j] =0
        if ranksCount[i][maxRank] == 1 and studentRanks[i][1] != -1:
            studentsChosen.append(i)
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
    count = len(studentList) + 1
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

#This function sets the students in 
def setStudentsPicked(students, studentRanks):
    for student in students:
        for i in range(len(studentRanks)):
            studentRanks[student][i] = -1
    return studentRanks

def createGroupsOfThree(groupsOfTwo, studentsLeft, studentRanks):
    maxRankPerGroup = [[0] * len(groupsOfTwo) for _ in range(len(studentsLeft))]
    minRankPerGroup = [[0] * len(groupsOfTwo) for _ in range(len(studentsLeft))]
    groupsOfThree = []
    #Useful if there are two groups with the same max rank
    for studentIndex, student in enumerate(studentsLeft): #We find the max rank for each group for student
        groupNumber = 0
        secondTimeChoosing = []
        for group in groupsOfTwo:
            stu1 = group[0]
            stu2 = group[1]
            #We look at the max rank between the student and the group's member
            if studentRanks[studentIndex][stu1] > studentRanks[student][stu2]:
                maxRankPerGroup[studentIndex][groupNumber] = studentRanks[studentIndex][stu1]
                minRankPerGroup[studentIndex][groupNumber] = studentRanks[studentIndex][stu2]
            else:
                maxRankPerGroup[studentIndex][groupNumber] = studentRanks[studentIndex][stu2]
                minRankPerGroup[studentIndex][groupNumber] = studentRanks[studentIndex][stu1]
            groupNumber += 1
        groupForStudent = -1
        chosenGroups = []
        for group in range(len(groupsOfTwo)):
            #If there is a group with a higher rank
            if maxRankPerGroup[studentIndex][group] > groupForStudent:
                groupForStudent = maxRankPerGroup[studentIndex][group]
                chosenGroups = []
                chosenGroups.append(group)
            elif maxRankPerGroup[studentIndex][group] == groupForStudent:
                chosenGroups.append(group)
        if len(chosenGroups) > 1:
            #If there is another group to place the student
            groupForStudent = -1
            for group in chosenGroups:
                #We search for the group with the highest rank
                if groupForStudent < minRankPerGroup[studentIndex][group]:
                    groupForStudent = minRankPerGroup[studentIndex][group]
                    secondTimeChoosing = []
                    secondTimeChoosing.append(group)
                elif groupForStudent == minRankPerGroup[studentIndex][group]:
                    secondTimeChoosing.append(group)

        #We proceed to add the student to a group.
        groupForStudent = -1
        if len(chosenGroups) == 1:
            groupForStudent = chosenGroups[0] 
        elif len(secondTimeChoosing) >= 1:
            groupForStudent = secondTimeChoosing[0] #If there are more than one choice, we take thee first one.
        groupOfThree = groupsOfTwo[groupForStudent]
        groupOfThree.append(student)
        groupsOfThree.append(groupOfThree)
        groupsOfTwo.remove(groupsOfTwo[groupForStudent])

    return groupsOfTwo, groupsOfThree