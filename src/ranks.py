# Matrix of ranks
RANKS = [[21, 20, 18, 15, 11, 6],
         [20, 19, 17, 14, 10, 5],
         [18, 17, 16, 13, 9, 4],
         [15, 14, 13, 12, 8, 3],
         [11, 10, 9, 8, 7, 2],
         [6, 5, 4, 3, 2, 1]]

# Correlation between a rank and a line of the matrix
RANKS_CORRELATION = {
    "TB": 0,
    "B": 1,
    "AB": 2,
    "P": 3,
    "I": 4,
    "AR": 5
}

def attributeRanks(students):
    """ 
    This function creates a matrix containing the ranks between each student.
    :param students: bi-dimensional array containing the students appreciations for each other.
    :type students: list of lists
    :return: bi-dimensional array containing the rank of each student's matching.
    :return type: list of lists
    """
    n = len(students)
    ME = [[-1] * n for _ in range(n)]
    for i in range(n):
        for j in range(i):
            markA = students[i][j]
            markB = students[j][i]
            rank = RANKS[RANKS_CORRELATION[markA]][RANKS_CORRELATION[markB]]
            ME[i][j] = ME[j][i] = rank
    return ME

def countRanks(ME, n):
    """ 
    Counts the number of specific ranks a student have.
    :param ME: the matrix containing the ranks between each student
    :param n: the nnumber of students
    :type ME: list of lists
    :type n: int
    :return: a matrix containing the numbre of each rank for each student.
    :return type: list of lists
    """
    NR = [[0] * 22 for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rank = ME[i][j]
            NR[i][rank] += 1
    return NR
