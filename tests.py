import csv, sys
from multiprocessing import Process, Queue
import src.fileOperations as fileOperations
import srcTest.groupsMulti as groupsMulti
import src.ranks as ranks

#This function prints a matrix on screen.
def printMatrix(matrix):
    for line in matrix:
        print(line)

#TODO: complete this function
def createRepartition(groupsOfTwo, studentsLeft, chosenStudent, nbBinomes, nbTrinomes, studentRanks, ranksCount, queue):
    otherStudent = groupsMulti.findOtherStudent(ME, NR, chosenStudent)
    group = [chosenStudent, otherStudent]
    groupsOfTwo.append(group)
    studentsLeft.remove(chosenStudent)
    studentsLeft.remove(otherStudent)
    studentRanks = groupsMulti.setStudentsPicked(group, studentRanks)
    groupsToCreate = nbBinomes+nbTrinomes-len(groupsOfTwo)-1
    repartitions = []
    for i in range(groupsToCreate):
        maxRank = groupsMulti.maximumRank(NR)
        student = groupsMulti.chooseStudent(ME, NR, maxRank)
        if len(student) > 1: #If there is more than 1 student chosen, we create a possible matching for each student.
            repMulti = multiProc(groupsOfTwo, studentsLeft, nbBinomes, nbTrinomes, ME, NR, names)
            for rep in repMulti:
                repartitions.append(rep)
            queue.put(repartitions)
            return
        otherStudent = groupsMulti.findOtherStudent(ME, NR, student)
        group = [student, otherStudent]
        groupsOfTwo.append(group)
        studentsLeft.remove(student)
        studentsLeft.remove(otherStudent)
        studentRanks = groupsMulti.setStudentsPicked(group, studentRanks)
    
    if nbTrinomes>=1:
        groupsOfTwo, groupsOfThree = groupsMulti.createGroupsOfThree(groupsOfTwo, studentsLeft, ME)
        repartition = []
        for group in groupsOfThree:
            repartition.append(group)
        for group in groupsOfTwo:
            repartition.append(group)
        repartitions.append(repartition)
    else:
        repartitions.append(groupsOfTwo)
    queue.put(repartitions)

def multiProc(groupsOfTwo, studentsLeft, nbBinomes, nbTrinomes, studentRanks, ranksCount, names):
    proc = []
    q = Queue()
    repartitions = []
    for i in len(studentsLeft):
        proc.append(Process(target=createRepartition, args=(groupsOfTwo, studentsLeft, studentsLeft[i], nbBinomes, nbTrinomes,q)))
        proc[i].start()
    for process in proc:
        process.join()
        repartitions.append(q.get())
    return repartitions

if __name__ == "__main__":
    ext = sys.argv[1][1:]
    fileName = "preferences"+ext+".csv"
    names, students = fileOperations.readAppreciationsCSV(fileName)
    n = len(students)
    ME = ranks.attributeRanks(students)
    NR = ranks.countRanks(ME, n)
    nbBinomes, nbTrinomes=0,0
    #Number of groups determination
    if n<36:
        if n%2==0:
            nbBinomes, nbTrinomes = (int)(n/2), 0
        else:
            nbBinomes, nbTrinomes = (int)((n-3)/2), 1 
    else:
        nbTrinomes = n-36
        nbBinomes = 18-nbTrinomes
    repartitions = []
    groupsOfTwo = []
    studentsLeft = []
    maxRank = 21
    for i in range(n):
        studentsLeft.append(i)
    #Creating the groups of 2
    for i in range(nbBinomes+nbTrinomes):
        maxRank = groupsMulti.maximumRank(NR)
        student = groupsMulti.chooseStudent(ME, NR, maxRank)
        if type(student) == list: #If there is more than 1 student chosen, we create a possible matching for each student.
            repMulti = multiProc(groupsOfTwo, studentsLeft, nbBinomes, nbTrinomes, ME, NR, names)
            for rep in repMulti:
                repartitions.append(rep)
            fileOperations.writeCSV(repartitions, names)
            sys.exit()

        otherStudent = groupsMulti.findOtherStudent(ME, NR, student)
        group = [student, otherStudent]
        groupsOfTwo.append(group)
        studentsLeft.remove(student)
        studentsLeft.remove(otherStudent)
        ME = groupsMulti.setStudentsPicked(group, ME)

    groupsOfTwo, studentsLeft = groupsMulti.createGroupsOfTwo(ME, NR, (nbBinomes+nbTrinomes))
    groupsOfThree=[]
    print("Groups of : ")
    printMatrix(groupsOfTwo)
    print("Students left : ", studentsLeft)
    if nbTrinomes>=1:
        groupsOfTwo, groupsOfThree = groupsMulti.createGroupsOfThree(groupsOfTwo, studentsLeft, ME)
    print("Final results :")
    print("Groups of 2 : ")
    printMatrix(groupsOfTwo)
    print("Groups of 3 : ")
    printMatrix(groupsOfThree)
    print("Writing CSV...")
    
    repartition = []
    for group in groupsOfThree:
        repartition.append(group)
    for group in groupsOfTwo:
        repartition.append(group)
    repartitions.append(repartition)
    fileOperations.writeCSV(repartitions, names)
    print("Writing complete.\nEnd of the script.")