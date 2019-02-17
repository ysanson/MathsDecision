import csv 

#This function reads the CSV containing the preferences of each student.
#Returns a dictionary row-name, and the matrix of appreciations.
def readAppreciationsCSV():
    with open('preferences.csv', mode='r') as preferences:
        csv_reader = csv.reader(preferences, delimiter=',')
        line_count=0
        nameCorrelation = {'0':''}
        appreciations = []
        for line in csv_reader:
            if line_count == 0: #Retrieve student names
                studentNames = line.split(",")
                for name, pos in enumerate(studentNames):
                    nameCorrelation[pos] = name
                line_count +=1
            else:
                appr = line.split(",")
                appreciations.append(appr.pop(0))
                line_count +=1
        return nameCorrelation, appreciations