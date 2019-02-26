import csv, os.path

#This function reads the CSV containing the preferences of each student.
#Returns a dictionary row-name, and the matrix of appreciations.
def readAppreciationsCSV(fileName):
    relPath = os.path.abspath(os.path.dirname(__file__))
    pathToFile = os.path.join(relPath, "../DONNEES/"+fileName)
    with open(pathToFile, mode='r') as preferences:
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
        appreciations = truncateMatrix(appreciations, 11)
        return nameCorrelation, appreciations

def truncateMatrix(appreciations, numberToKeep):
    if len(appreciations) < numberToKeep:
        return appreciations
    else:
        appreciations = appreciations[:numberToKeep]
        for index, col in enumerate(appreciations):
            appreciations[index]  = col[:numberToKeep]
        return appreciations

#This function writes a CSV conforming to the standards required by the project.
def writeCSV(groupsOfTwo, groupsOfThree, nameCorrelation):
    with open('SSS.csv', 'w') as rendu:
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