import csv

def readCSV():
    with open("SSS.csv", mode ='r') as fichier:
        csv_reader = csv.reader(fichier, delimiter=',')
        matrix = []
        for line in csv_reader:
            matrix.append(line)
        return matrix

matrix = readCSV()
for i1, line1 in enumerate(matrix):
    for i2, line2 in enumerate(matrix):
        if line1 != line2:
            print("line ", i1, " is different from ", i2)
        #else:
           #print("line ", i1, " is equal to ", i2)
