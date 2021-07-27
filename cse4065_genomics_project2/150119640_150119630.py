# Py 3.8.5
# CSE4065 Computational Genomics
# Programming Assignment 2
# Ayberk Ömer Altuntabak - 150119640
# Bilal Tan - 150119630

import math,os # Basic Python system libraries

def match_check(char1, char2, positive, negative):
    #Char check for matching symbols.
    #If two char is not equal  (mismatch) each other returns negative, o
    #Else returns positive
    
    if char1 != char2:
        return -negative
    else:
        return positive
        
class OptimumAlignmentAlgorithm:
    match_score = 2
    mismatch_score = 1
    gap_start_score = 1
    gap_score = 0.5
    infinity_score = float("inf")
    def __init__(self) -> None:
        pass
    
    def dynamic_pairwise_align(self,x,y):
        M = self.matrix_setoff(x, y)
        Ix = self.matrix_setoff(x, y)
        Iy = self.matrix_setoff(x, y)
        for i in range(1, len(y)+1):
            M[i][0] = -math.inf
            Ix[i][0] = -math.inf
            Iy[i][0] = -self.gap_start_score if Iy[i-1][0] == -math.inf else Iy[i-1][0] - self.gap_score
        for j in range(1, len(x)+1):
            M[0][j] = -math.inf
            Iy[0][j] = -math.inf
            Iy[i][0] = -self.gap_start_score if Iy[i-1][0] == -math.inf else Iy[i-1][0] - self.gap_score
        for i in range(1, len(y)+1):
            for j in range(1, len(x)+1):
                M[i][j] = max(M[i-1][j-1] + match_check(x[j-1], y[i-1], self.match_score, self.mismatch_score),
                            Ix[i-1][j-1] + match_check(x[j-1], y[i-1], self.match_score, self.mismatch_score),
                            Iy[i-1][j-1] + match_check(x[j-1], y[i-1], self.match_score, self.mismatch_score))
                Ix[i][j] = max(M[i][j-1] - self.gap_start_score, Ix[i][j-1] - self.gap_score)
                Iy[i][j] = max(M[i-1][j] - self.gap_start_score, Iy[i-1][j] - self.gap_score)
        x_return = ""; y_return=""
        i = len(y); j = len(x)
        
        align_scores = (M[i][j], Iy[i][j], Ix[i][j]) #Determining the starting matrix is ​​done here
        print("Score of this sequence alignment",max(align_scores))
        matrix_idx = align_scores.index(max(align_scores))

        #matrix_index variable will monitor the current matrix through backtracking
        matrix_index = ["M", "Iy", "Ix"][matrix_idx]
        while self.isIBiggerThanZero(i) and self.isJBiggerThanZero(j):
            #Check cross moves back to all three matrices and make char alignment of M
            if self.isMatrixIndexM(matrix_index=matrix_index):
                i, j, x_return, y_return, matrix_index = self.movementInMatrixM(x, y, M, Ix, Iy, i, j, x_return, y_return,matrix_index)
            #Check up and down move to Iy and M, make char alignment of y character with x gap of Iy
            if self.isMatrixIndexIy(matrix_index=matrix_index):
                i, x_return, y_return, matrix_index = self.movementInMatrixIy(y, M, Iy, i, j, x_return, y_return,matrix_index)
            #Check left and right move to Ix and M, make char alignment of x character with y gap of Ix
            if self.isMatrixIndexIx(matrix_index=matrix_index):
                j, x_return, y_return,matrix_index = self.movementInMatrixIx(x, M, Ix, i, j, x_return, y_return,matrix_index)
        if self.isIBiggerThanZero(i):
            x_return = ("-"*i) + x_return
            y_return = y[0:i] + y_return
    # this block matches characters in x and create gap with y
        if self.isJBiggerThanZero(j):
            x_return = x[0:j] + x_return
            y_return = ("-"*j) + y_return
    # When we get to the end of the function, return strings aligned from here
        return (x_return, y_return)

    def isJBiggerThanZero(self, j):
        return j > 0

    def isIBiggerThanZero(self, i):
        return i > 0

    def movementInMatrixIx(self, x, M, Ix, i, j, x_return, y_return,matrix_index):
        if Ix[i][j] == M[i][j-1] - self.gap_start_score:
            x_return = x[j-1] + x_return
            y_return = "-" + y_return
            j -= 1
            matrix_index = "M"
            return j,x_return,y_return,matrix_index

        if Ix[i][j] == Ix[i][j-1] - self.gap_score:
            x_return = x[j-1] + x_return
            y_return = "-" + y_return
            j -= 1
            matrix_index = "Ix"
            return j,x_return,y_return,matrix_index
        return j,x_return,y_return,matrix_index

    def movementInMatrixIy(self, y, M, Iy, i, j, x_return, y_return,matrix_index):
        if Iy[i][j] == M[i-1][j] - self.gap_start_score:
            x_return = "-" + x_return
            y_return = y[i-1] + y_return
            i -= 1
            matrix_index = "M"
            return i,x_return,y_return,matrix_index
        if Iy[i][j] == Iy[i-1][j] - self.gap_score:
            x_return = "-" + x_return
            y_return = y[i-1] + y_return
            i -= 1
            matrix_index = "Iy"
            return i,x_return,y_return,matrix_index
        return i,x_return,y_return,matrix_index     

    def movementInMatrixM(self, x, y, M, Ix, Iy, i, j, x_return, y_return,matrix_index):
        if M[i][j] == M[i-1][j-1] + self.match_score or M[i][j] == M[i-1][j-1] - self.mismatch_score:
            x_return = x[j-1] + x_return
            y_return = y[i-1] + y_return
            i -= 1; j -= 1
            matrix_index = "M"
            return i,j,x_return,y_return,matrix_index
        if M[i][j] == Iy[i-1][j-1] + self.match_score or M[i][j] == Iy[i-1][j-1] - self.mismatch_score:
            x_return = x[j-1] + x_return
            y_return = y[i-1] + y_return
            i -= 1; j -= 1
            matrix_index = "Iy"
            return i,j,x_return,y_return,matrix_index
        if M[i][j] == Ix[i-1][j-1] + self.match_score or M[i][j] == Ix[i-1][j-1] - self.mismatch_score:
            x_return = x[j-1] + x_return
            y_return = y[i-1] + y_return
            i -= 1; j -= 1
            matrix_index = "Ix"
            return i,j,x_return,y_return,matrix_index
        return i,j,x_return,y_return,matrix_index
    
    def matrix_setoff(self, x, y):
        return [[0]*(len(x)+1) for i in range(len(y)+1)]
    def isMatrixIndexM(self,matrix_index):
        return matrix_index == "M"
    def isMatrixIndexIy(self,matrix_index):
        return matrix_index == "Iy"
    def isMatrixIndexIx(self,matrix_index):
        return matrix_index == "Ix"

class SequenceReading:

    def __init__(self):
        self.config = {}
        full_path = os.path.realpath(__file__)
        self.paths = [ # Input Files 
        os.path.dirname(full_path)+"/inputs/test1.seq",
        os.path.dirname(full_path)+"/inputs/test2.seq",
        os.path.dirname(full_path)+"/inputs/test3.seq",
        os.path.dirname(full_path)+"/inputs/test4.seq",
        os.path.dirname(full_path)+"/inputs/test5.seq"
        ]
        for path in self.paths:
            self.read_file(path)
        pass

    def read_file(self, path):
        file = open(path,"r")
        lines = []
        lines_start = file.readlines()
        for line in lines_start:
            temporary = line.split("\n")[0]
            lines.append(temporary)
        self.config[path] = lines

if __name__ =="__main__":
    seq_read = SequenceReading()
    aligner = OptimumAlignmentAlgorithm()
    sequences = seq_read.config.values()

    for seq in sequences:
        result = aligner.dynamic_pairwise_align(seq[0],seq[1])
        print(result[0])
        for x, y in zip(result[0], result[1]):
            if x == y:
                print("|", sep='', end='')
            else:
                print(" ", sep='', end='')
        print('')
        print(result[1])