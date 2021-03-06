import src.globals as glo
import copy

def createGroupsOfTwo(studentRanks, ranksCount, numberOfGroups):
    """
    This function creates groups of 2, based on the appreciations given, and the groups we have to form.
    :param studentRanks: matrix containing the ranks between each student.
    :param ranksCount: matrix containing the number of each rank for each student.
    :param numberOfGroups: the number of groups we have to form.
    :type studentRanks: list of lists
    :type ranksCount: list of lists
    :type numberOfGroups: int
    :return: a list of list, containing the groups, and a list containing the students left.
    :return type: tuple (list, list)
    """
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


def chooseStudent(studentRanks, ranksCount, maxRank):
    """ 
    Chooses a student based on his number of maxRank.
    :param studentRanks: matrix containing the ranks between each student.
    :param ranksCount: matrix containing the number of each rank for each student.
    :param maxRank: the maximum rank we search for.
    :type studentRanks: list of lists
    :type ranksCount: list of lists
    :type maxRank: int
    :return: a student from the available students.
    :return type: int
    """
    studentsChosen = []
    if maxRank==1: #If the students are equal in the last rank, we take the first one.
        for i in range(len(studentRanks)):
            if studentRanks[i][1] != -1:
                return i
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


def distinguishStudents(studentList, ranksCount, maxRank):
    """ 
    This function is used to separate students that have the same maxRank.
    :param studentList: the possible students to choose.
    :param ranksCount: matrix containing the number of each rank for each student.
    :param maxRank: the maximum rank we search for.
    :type studentList: list of int
    :type ranksCount: list of lists
    :type maxRank: int
    :return: a student distinguished from the other.
    :return type: int
    """
    count = len(studentList) + 1
    studentsChosen = []
    if maxRank==1 : #If the students are equal in the last rank, we take the first one.
        if len(studentList) >1:
            glo.equalsStudentsList.append(studentList)
        return studentList[0]

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


def maximumRank(matrix):
    """ 
    This function returns the maximum rank of the matrix.
    :param matrix: the ranksCount, the number of ranks for each student
    :type matrix: list of lists
    :return: the current maximum rank
    :return type: int
    """
    maxR = 0
    for i in range(21, 0, -1):
        if matrix[0][i] != -1 and i >= maxR:
            maxR = i
    return maxR

def disableRank(studentsLeft, studentRanks, ranksCount, maxRank):
    """ 
    This function puts -1 to a rank if the students left doesn't have that rank.
    :param studentsLeft: the leftover students.
    :param studentRanks: matrix containing the ranks between each student.
    :param ranksCount: matrix containing the number of each rank for each student.
    :param maxRank: the maximum rank we search for.
    :type studentsLeft: list of int
    :type studentRanks: list of lists
    :type ranksCount: list of lists
    :type maxRank: int
    :return: a parameter to see if the rank has been disabled, and the updated studentRanks
    :return type: tuple(boolean, list)
    """
    isDisable = True
    for i in studentsLeft:
        if ranksCount[i][maxRank] != 0:
            isDisable = False
    if isDisable:
        for i in len(studentRanks):
            ranksCount[i][maxRank] = -1
    return isDisable, studentRanks

def findOtherStudent(studentRanks, ranksCount, stu):
    """ 
    This function searches the best student to form a group with the one in parameter.
    :param studentRanks: matrix containing the ranks between each student.
    :param ranksCount: matrix containing the number of each rank for each student.
    :param stu: the student to match with
    :type studentRanks: list of lists
    :type ranksCount: list of lists
    :param stu: int
    :return: the student to associate
    :return type: int
    """
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


def setStudentsPicked(students, studentRanks):
    """
    This function sets the students picked.
    :param students: the students to set
    :param studentRanks: matrix containing the ranks between each student.
    :type students: list of int
    :type studentRanks: list of lists
    :return: the updated studentRanks matrix.
    :return type: list of lists
    """
    for student in students:
        for i in range(len(studentRanks)):
            studentRanks[student][i] = -1
    return studentRanks


def createGroupsOfThree(groupsOfTwo, studentsLeft, studentRanks):
    """ 
    This function creates the groups of three based on the actual groups of 2 and the students left.
    :param groupsOfTwo: the groups of two that has been created.
    :param studentsLeft: the leftover students
    :param studentRanks: matrix containing the ranks between each student.
    :type groups of two: list of lists
    :type studentsLeft: list of int
    :type studentRanks: list of lists
    :return: the groups of three created, along with the groups of two
    :return type: list of lists
    """
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

    for _ in range(len(studentsLeft)):
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
                    if not stu.__contains__(student):
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
                        if not stu2.__contains__(student):
                            stu2.append(student)
        else:
            stu2 = stu
    
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
                    # on change les matrices pour ne pas replacer l'étudiant placé
        for j in range(len(groupsOfTwo)):
            minRankPerGroup[stu2[0]][j] = -1
            maxRankPerGroup[stu2[0]][j] = -1

        # We proceed to add the student to a group.
        groupForStudent = -1
        if len(chosenGroups) == 1:
            groupForStudent = chosenGroups[0]
        elif len(secondTimeChoosing) >= 1:
            if len(secondTimeChoosing) > 1:
                glo.equalsStudentsList.append(secondTimeChoosing)
            groupForStudent = secondTimeChoosing[0]  # If there are more than one choice, we take thee first one.
        groupOfThree = groupsOfTwo[groupForStudent]
        # on place l'étudiant dans le groupe
        groupOfThree.append(studentsLeft[stu2[0]])
        groupsOfThree.append(groupOfThree)
        groupsOfTwo.remove(groupsOfTwo[groupForStudent])
    return groupsOfTwo, groupsOfThree


def createMultipledivisions(numberOfResults):
    """
    This function creates multiple divisions whenever it is necessary.
    It appends the divisions in the global divisions list.
    For each equal students, we create a division in which we intervert the student in first place with the other one considered.
    :param numberOfResults: the number of divisions to create
    :type numberOfResults: int
    """
    for students in glo.equalsStudentsList:
        for i,otherStudent in enumerate(students):
            if i != 0:
                glo.divisions.append(copy.deepcopy(glo.divisions[0]))
                intervertStudents(students[0], otherStudent, len(glo.divisions)-1)
            if numberOfResults != -1:
                if len(glo.divisions) >= numberOfResults:
                    return

            

def intervertStudents(stu1, stu2, divisionIndex):
    """
    This function interverts 2 students in their relative groups, in a given division.
    :param stu1: the first student 
    :param stu2: the second student
    :param divisionIndex: the considered division.
    :type stu1: int
    :type stu2: int
    :type divisionIndex: int
    """
    groupStu1 = findStudentInGroup(stu1, glo.divisions[0])
    groupStu2 = findStudentInGroup(stu2, glo.divisions[0])
    glo.divisions[divisionIndex][groupStu1].remove(stu1)
    glo.divisions[divisionIndex][groupStu1].append(stu2)
    glo.divisions[divisionIndex][groupStu2].remove(stu2)
    glo.divisions[divisionIndex][groupStu2].append(stu1)


def findStudentInGroup(stu, division):
    """
    This function finds the group of a student, from a given division.
    :param stu: the student to find
    :param division: the division to find the student in
    :type stu: int
    :type division: list of lists of int
    """
    for i,group in enumerate(division):
        if group.__contains__(stu):
            return i
    return -1


