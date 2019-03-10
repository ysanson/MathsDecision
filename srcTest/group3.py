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
            #We look at the max rank between the student and the group's member
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
        stu =[]
        stu2 =[]
        # on regarde les rangs min et on cherche le max
        for group in range(len(minRankPerGroup)):
            for student in range(len(studentsLeft)):
                if minRankPerGroup[student][group] > minMaxRank:
                    minMaxRank = minRankPerGroup[student][group]
                    stu=[]
                    stu.append(student)
                elif minRankPerGroup[student][group] == minMaxRank:
                    stu.append(student)
        if len(stu) > 1:
            # on regarde les rangmax et on cherche le max
            for group in range(len(maxRankPerGroup)):
                for student in range(len(stu)):
                    if maxRankPerGroup[student][group] > maxMaxRank:
                        maxMaxRank = maxRankPerGroup[student][group]
                        stu2=[]
                        stu2.append(student)
                    elif maxRankPerGroup[student][group] == maxMaxRank:
                        stu2.append(student)
        elif len(stu) == 1:
            stu2 = stu
        if len(stu2) > 1:
            # on fait un truc
            stuInter=stu2[0]
            stu2 = stuInter
        elif len(stu2) == 1:
            #on affecte l'étudiant à un groupe
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
            #on place l'étudiant dans le groupe
            groupOfThree.append(studentsLeft[stu2[0]])
            groupsOfThree.append(groupOfThree)
            groupsOfTwo.remove(groupsOfTwo[groupForStudent])
    return groupsOfTwo, groupsOfThree