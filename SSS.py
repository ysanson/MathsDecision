import csv, sys

#This function reads the CSV containing the preferences of each student.
#Returns a dictionary row-name, and the matrix of appreciations.
def readAppreciationsCSV(fileName):
    with open(fileName, mode='r') as preferences:
        csv_reader = csv.reader(preferences, delimiter=',')
        line_count=0
        nameCorrelation = {0:''}
        appreciations = []
        for line in csv_reader:
            if line_count == 0: #Retrieve student names
                for pos, name in enumerate(line):
                    nameCorrelation[pos-1] = name #Because the names are 1 column away from the matrix column.
                line_count +=1
            else:
                line.pop(0)
                appreciations.append(line)
                line_count +=1
        del nameCorrelation[-1]
        return nameCorrelation, appreciations

#This function writes a CSV conforming to the standards required by the project.
def writeCSV(groupsOfTwo, groupsOfThree, nameCorrelation):
    with open('groupesSSS.csv', 'w') as rendu:
        writer = csv.writer(rendu, delimiter=" ")
        line=[]
        for i in range(len(groupsOfThree)): #Writing groups of three
            for stu in groupsOfThree[i]:
                line.append(nameCorrelation[stu])
            line[len(line)-1] +=";"
        for i in range(len(groupsOfTwo)): #Writing groups of two
            for stu in groupsOfTwo[i]:
                line.append(nameCorrelation[stu])
            line[len(line)-1] +=";"
        line[len(line)-1] = line[len(line)-1][:-1]
        writer.writerow(line)

#Matrix of ranks
RANKS= [[21,20,18,15,11,6],
        [20,19,17,14,10,5],
        [18,17,16,13,9,4],
        [15,14,13,12,8,3],
        [11,10,9,8,7,2],
        [6,5,4,3,2,1]]

#Correlation between a rank and a line of the matrix
RANKS_CORRELATION={
    "TB":0,
    "B":1,
    "AB":2,
    "P":3,
    "I":4,
    "AR":5
}

#Students is a bi-dimensional array containing the students appreciations for each other.
#This function returns a bi-dimensional array containing the rank of each student's matching.
def attributeRanks(students):
    n = len(students)
    ME = [[-1] * n for _ in range(n)]
    for i in range(n):
        for j in range(i):
            markA = students[i][j]
            markB = students[j][i]
            rank = RANKS[RANKS_CORRELATION[markA]][RANKS_CORRELATION[markB]]
            ME[i][j] = ME[j][i] = rank
    return ME

#Counts the number of specific ranks a student have.
#Returns a matrix, n*22, containing the count of ranks.
def countRanks(ME, n):
        NR = [[0] * 22 for _ in range(n)]
        for i in range(n):
                for j in range(n):
                        rank = ME[i][j]
                        NR[i][rank] += 1 
        return NR

#This function creates groups of 2, based on the appreciations given, and the groups we have to form.
#Returns an array containing the groups, and another array containing the students left.
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

#Chooses a student based on his number of maxRank
#Returns a number, corresponding to a student in the matrix.
def chooseStudent(studentRanks, ranksCount, maxRank):
    studentsChosen = []
    if maxRank == 1:
        return None
    for i in range(len(ranksCount)):
        if studentRanks[i][1] == -1:
            for j in range(21):
                ranksCount[i][j]=0
        if ranksCount[i][maxRank] == 1 and studentRanks[i][1] != -1:
            studentsChosen.append(i)
    if len(studentsChosen) >1:
        student = distinguishStudents(studentsChosen, ranksCount, maxRank-1)
        if studentRanks[student][1] != -1:
            return student
        else:
            for i in range(21):
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
    for i in range(21,0,-1):
        if matrix[0][i] != -1 and i>=maxR:
            maxR=i
    return maxR

#This function puts -1 to a rank if the students left doesn't have that rank.
def disableRank(studentsLeft, studentRanks, ranksCount, maxRank):
    isDisable = True
    for i in studentsLeft:
        if ranksCount[i][maxRank] != 0:
            isDisable = False
    if isDisable:
        for i in len(studentRanks):
            ranksCount[i][maxRank] = -1
    return isDisable, studentRanks

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
            if studentRanks[studentIndex][stu1] > studentRanks[studentIndex][stu2]:
                maxRankPerGroup[studentIndex][groupNumber] = studentRanks[student][stu1]
                minRankPerGroup[studentIndex][groupNumber] = studentRanks[student][stu2]
            else:
                maxRankPerGroup[studentIndex][groupNumber] = studentRanks[student][stu2]
                minRankPerGroup[studentIndex][groupNumber] = studentRanks[student][stu1]
            groupNumber += 1
        groupForStudent = -1
        chosenGroups = []
        for group in range(len(groupsOfTwo)):
            #If there is a group with a higher rank
            if minRankPerGroup[studentIndex][group] > groupForStudent:
                groupForStudent = maxRankPerGroup[studentIndex][group]
                chosenGroups = []
                chosenGroups.append(group)
            elif minRankPerGroup[studentIndex][group] == groupForStudent:
                chosenGroups.append(group)
        if len(chosenGroups) > 1:
            #If there is another group to place the student
            groupForStudent = -1
            for group in chosenGroups:
                #We search for the group with the highest rank
                if groupForStudent < maxRankPerGroup[studentIndex][group]:
                    groupForStudent = maxRankPerGroup[studentIndex][group]
                    secondTimeChoosing = []
                    secondTimeChoosing.append(group)
                elif groupForStudent == maxRankPerGroup[studentIndex][group]:
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
#This function prints a matrix on screen.
def printMatrix(matrix):
    for line in matrix:
        print(line)

#This function is the main of this script.
def main():
    ext = sys.argv[1][1:]
    fileName = "preferences"+ext+".csv"
    names, students = readAppreciationsCSV(fileName)
    n = len(students)
    ME = attributeRanks(students)
    printMatrix(ME)
    NR = countRanks(ME, n)
    nbBinomes, nbTrinomes=0,0
    if n<36:
        if n%2==0:
            nbBinomes, nbTrinomes = (int)(n/2), 0
        else:
            nbBinomes, nbTrinomes = (int)((n-3)/2), 1 
    else:
        nbTrinomes = n-36
        nbBinomes = 18-nbTrinomes
    groupsOfTwo, studentsLeft = createGroupsOfTwo(ME, NR, (nbBinomes+nbTrinomes))
    groupsOfThree=[]
    if nbTrinomes>1:
        groupsOfTwo, groupsOfThree = createGroupsOfThree(groupsOfTwo, studentsLeft, ME)
    print("Final results :")
    print("Groups of 2 : ")
    printMatrix(groupsOfTwo)
    print("Groups of 3 : ")
    printMatrix(groupsOfThree)
    print("Writing CSV...")
    writeCSV(groupsOfTwo, groupsOfThree, names)
    print("Writing complete.\nEnd of the script.")


main()