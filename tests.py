import csv, sys
from multiprocessing import Process, Queue
import fileOperations, groupsMulti, ranks

#This function prints a matrix on screen.
def printMatrix(matrix):
    for line in matrix:
        print(line)

#TODO: complete this function
def createRepartition(groupsOfTwo, studentsLeft, chosenStudent, nbBinomes, nbTrinomes, queue):
    groupsToCreate = nbBinomes+nbTrinomes-len(groupsOfTwo)
    for i in range(groupsToCreate):
        maxRank = groupsMulti.maximumRank(NR)
        student = groupsMulti.chooseStudent(ME, NR, maxRank)
        if len(student) >1:
            multiThread(groupsOfTwo, studentsLeft, nbBinomes, nbTrinomes, names)

        otherStudent = groupsMulti.findOtherStudent(ME, NR, student)
        group = [student, otherStudent]
        groupsOfTwo.append(group)
        studentsLeft.remove(student)
        studentsLeft.remove(otherStudent)
        studentRanks = groupsMulti.setStudentsPicked(group, studentRanks)
    return 0

def multiThread(groupsOfTwo, studentsLeft, nbBinomes, nbTrinomes, names):
    proc = []
    q = Queue()
    repartitions = []
    for i in len(studentsLeft):
        proc.append(Process(target=createRepartition, args=(groupsOfTwo, studentsLeft, studentsLeft[i], nbBinomes, nbTrinomes,q)))
        proc[i].start()
    for process in proc:
        process.join()
        repartitions.append(q.get())
    fileOperations.writeCSV(repartitions, names)
    sys.exit()

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
    
    groupsOfTwo = []
    studentsLeft = []
    maxRank = 21
    for i in range(n):
        studentsLeft.append(i)
    #Creating the groups of 2
    for i in range(nbBinomes+nbTrinomes):
        maxRank = groupsMulti.maximumRank(NR)
        student = groupsMulti.chooseStudent(ME, NR, maxRank)
        if len(student) >1:
            multiThread(groupsOfTwo, studentsLeft, nbBinomes, nbTrinomes, names)

        otherStudent = groupsMulti.findOtherStudent(ME, NR, student)
        group = [student, otherStudent]
        groupsOfTwo.append(group)
        studentsLeft.remove(student)
        studentsLeft.remove(otherStudent)
        studentRanks = groupsMulti.setStudentsPicked(group, studentRanks)

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
    repartitions = []
    repartition = []
    for group in groupsOfThree:
        repartition.append(group)
    for group in groupsOfTwo:
        repartition.append(group)
    repartitions.append(repartition)
    fileOperations.writeCSV(repartitions, names)
    print("Writing complete.\nEnd of the script.")