import csv 

#This function reads the CSV containing the preferences of each student.
#Returns a dictionary row-name, and the matrix of appreciations.
def readAppreciationsCSV():
    with open('preferences.csv', mode='r') as preferences:
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