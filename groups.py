# This function creates groups of 2, based on the appreciations given, and the groups we have to form.
# Returns an array containing the groups, and another array containing the students left.
def createGroupsOfTwo(studentRanks, ranksCount, numberOfGroups):
    groupsOfTwo = []
    studentsLeft = []
    maxRank = 21
    for i in range(len(studentRanks)):
        studentsLeft.append(i)
    for i in range(numberOfGroups):
        maxRank = maximumRank(ranksCount)
        student = chooseStudent(studentRanks, ranksCount, maxRank)
        otherStudent = findOtherStudent(studentRanks, ranksCount, student)
        group = [student, otherStudent]
        groupsOfTwo.append(group)
        studentsLeft.remove(student)
        studentsLeft.remove(otherStudent)
        studentRanks = setStudentsPicked(group, studentRanks)
    return groupsOfTwo, studentsLeft


# Chooses a student based on his number of maxRank
# Returns a number, corresponding to a student in the matrix.
def chooseStudent(studentRanks, ranksCount, maxRank):
    studentsChosen = []
    if maxRank == 1:
        return None
    for i in range(len(ranksCount)):
        if studentRanks[i][1] == -1:
            for j in range(21):
                ranksCount[i][j] = 0
        if ranksCount[i][maxRank] == 1 and studentRanks[i][1] != -1:
            studentsChosen.append(i)
    if len(studentsChosen) > 1:
        student = distinguishStudents(studentsChosen, ranksCount, maxRank - 1)
        if studentRanks[student][1] != -1:
            return student
        else:
            for i in range(21):
                ranksCount[student][i] = -1
            return chooseStudent(studentRanks, ranksCount, maxRank)
    elif len(studentsChosen) == 0:
        return chooseStudent(studentRanks, ranksCount, maxRank - 1)
    return studentsChosen[0]


# This function is used to separate students that have the same maxRank.
# Returns a number representing a student, distinguished from the others.
def distinguishStudents(studentList, ranksCount, maxRank):
    count = len(studentList) + 1
    studentsChosen = []
    for i in studentList:
        if ranksCount[i][maxRank] > 0:
            # If rank number is less than found before
            if ranksCount[i][maxRank] < count and ranksCount[i][maxRank] != -1:
                studentsChosen = []
                studentsChosen.append(i)
                count = ranksCount[i][maxRank]
            # If rank number is equal to those already found
            elif ranksCount[i][maxRank] == count and ranksCount[i][maxRank] != -1:
                studentsChosen.append(i)
    if len(studentsChosen) > 1:
        return distinguishStudents(studentsChosen, ranksCount, maxRank - 1)
    elif len(studentsChosen) == 0:
        return distinguishStudents(studentList, ranksCount, maxRank - 1)
    return studentsChosen[0]


# This function returns the maximum rank of the matrix.
def maximumRank(matrix):
    maxR = 0
    for i in range(21, 0, -1):
        if matrix[0][i] != -1 and i >= maxR:
            maxR = i
    return maxR


# This function puts -1 to a rank if the students left doesn't have that rank.
def disableRank(studentsLeft, studentRanks, ranksCount, maxRank):
    isDisable = True
    for i in studentsLeft:
        if ranksCount[i][maxRank] != 0:
            isDisable = False
    if isDisable:
        for i in len(studentRanks):
            ranksCount[i][maxRank] = -1
    return isDisable, studentRanks


# This function searches the best student to form a group with the one in parameter.
# Returns a number, corresponding to the picked student.
def findOtherStudent(studentRanks, ranksCount, stu):
    bestPicks = []
    rank = 0
    for i in range(len(studentRanks)):
        if studentRanks[i][stu] > rank:  # If we find a superior rank, we clear the picks and update the rank
            bestPicks = []
            rank = studentRanks[i][stu]
            bestPicks.append(i)
        elif studentRanks[i][stu] == rank:  # If we find someone with the same rank, we add him to the list
            bestPicks.append(i)
    if len(bestPicks) == 1:
        return bestPicks[0]
    elif len(bestPicks) > 1:
        return distinguishStudents(bestPicks, ranksCount, rank - 1)


# This function sets the students in
def setStudentsPicked(students, studentRanks):
    for student in students:
        for i in range(len(studentRanks)):
            studentRanks[student][i] = -1
    return studentRanks


def createGroupsOfThree(groupsOfTwo, studentsLeft, studentRanks):
    maxRankPerGroup = [[0] * len(groupsOfTwo) for _ in range(len(studentsLeft))]
    minRankPerGroup = [[0] * len(groupsOfTwo) for _ in range(len(studentsLeft))]
    groupsOfThree = []
    # Useful if there are two groups with the same max rank
    for studentIndex, student in enumerate(studentsLeft):  # We find the max rank for each group for student
        groupNumber = 0
        secondTimeChoosing = []
        for group in groupsOfTwo:
            stu1 = group[0]
            stu2 = group[1]
            # We look at the max rank between the student and the group's member
            if studentRanks[student][stu1] > studentRanks[student][stu2]:
                maxRankPerGroup[studentIndex][groupNumber] = studentRanks[student][stu1]
                minRankPerGroup[studentIndex][groupNumber] = studentRanks[student][stu2]
            else:
                maxRankPerGroup[studentIndex][groupNumber] = studentRanks[student][stu2]
                minRankPerGroup[studentIndex][groupNumber] = studentRanks[student][stu1]
            groupNumber += 1

    for i in range(len(studentsLeft)):
        # chose student
        minMaxRank = 0
        maxMaxRank = 0
        stu = []
        stu2 = []
        # on regarde les rangs min et on cherche le max
        for group in range(len(minRankPerGroup)):
            for student in range(len(studentsLeft)):
                if minRankPerGroup[student][group] > minMaxRank:
                    minMaxRank = minRankPerGroup[student][group]
                    stu = []
                    stu.append(student)
                elif minRankPerGroup[student][group] == minMaxRank:
                    stu.append(student)
        if len(stu) > 1:
            # on regarde les rangmax et on cherche le max
            for group in range(len(maxRankPerGroup)):
                for student in range(len(stu)):
                    if maxRankPerGroup[student][group] > maxMaxRank:
                        maxMaxRank = maxRankPerGroup[student][group]
                        stu2 = []
                        stu2.append(student)
                    elif maxRankPerGroup[student][group] == maxMaxRank:
                        stu2.append(student)
        elif len(stu) == 1:
            stu2 = stu
        if len(stu2) > 1:
            # on fait un truc
            stuInter = stu2[0]
            stu2 = stuInter
        elif len(stu2) == 1:
            # on affecte l'étudiant à un groupe
            groupForStudent = -1
            chosenGroups = []
            for group in range(len(groupsOfTwo)):
                # If there is a group with a higher rank
                if minRankPerGroup[stu2[0]][group] > groupForStudent:
                    groupForStudent = minRankPerGroup[stu2[0]][group]
                    chosenGroups = []
                    chosenGroups.append(group)
                elif minRankPerGroup[stu2[0]][group] == groupForStudent:
                    chosenGroups.append(group)
            if len(chosenGroups) > 1:
                # If there is another group to place the student
                groupForStudent = -1
                for group in chosenGroups:
                    # We search for the group with the highest rank
                    if groupForStudent < maxRankPerGroup[stu2[0]][group]:
                        groupForStudent = maxRankPerGroup[stu2[0]][group]
                        secondTimeChoosing = []
                        secondTimeChoosing.append(group)
                    elif groupForStudent == maxRankPerGroup[stu2[0]][group]:
                        secondTimeChoosing.append(group)
                        # on change les matrice pour ne pas replacer l'étudiant placé
            for j in range(len(groupsOfTwo)):
                minRankPerGroup[stu2[0]][j] = -1
                maxRankPerGroup[stu2[0]][j] = -1

            # We proceed to add the student to a group.
            groupForStudent = -1
            if len(chosenGroups) == 1:
                groupForStudent = chosenGroups[0]
            elif len(secondTimeChoosing) >= 1:
                groupForStudent = secondTimeChoosing[0]  # If there are more than one choice, we take thee first one.
            groupOfThree = groupsOfTwo[groupForStudent]
            # on place l'étudiant dans le groupe
            groupOfThree.append(studentsLeft[stu2[0]])
            groupsOfThree.append(groupOfThree)
            groupsOfTwo.remove(groupsOfTwo[groupForStudent])
    return groupsOfTwo, groupsOfThree
