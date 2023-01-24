import copy


class SudokuSolver:

    def __init__(self, board):
        self.board = board
        self.boxKey = [(0,0), (0,3), (0,6), (3,0), (3,3), (3,6), (6,0), (6,3), (6,6)]
        
        box1 = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        box2 = [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)]
        box3 = [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)]
        
        box4 = [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)]
        box5 = [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]
        box6 = [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)]

        box7 = [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)]
        box8 = [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)]
        box9 = [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]
        
        self.boxRef = [box1, box2, box3, box4, box5, box6, box7, box8, box9]

    def print_board(self):
        for row in range(0, 9):
            for col in range(0, 9):
                if (col) % 3 == 0:
                    print("   ", self.board[row][col], end=" ")
                else:
                    print("", self.board[row][col], end= " ")
                if(row + 1) % 3 == 0 and col == 8:
                    print("\n")
            print()
    def solved(self):
        # returns True if the board both full and correctly solved
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return self.correct();

    def correct(self):
        # returns True if the board does not break any rules
        foundNums = set()

        # check each box for repeats
        for (r, c) in self.boxKey:
            for row in range(r, r+3):
                for col in range(c, c+3):
                    if self.board[row][col] not in foundNums and self.board[row][col] != 0:
                        foundNums.add(self.board[row][col])
                    elif self.board[row][col] in foundNums:
                        return False
            foundNums.clear()
            
        # check each row for repeats
        foundNums.clear()
        for row in self.board:
            for cell in row:
                if cell not in foundNums and cell != 0:
                    foundNums.add(cell)
                elif cell in foundNums:
                    return False
            foundNums.clear()
        
        # cheack each column for repeats
        foundNums.clear()
        for col in range(0, 9):
            for row in range(0, 9):
                if self.board[row][col] not in foundNums and self.board[row][col] != 0:
                    foundNums.add(self.board[row][col])
                elif self.board[row][col] in foundNums:
                    return False
            foundNums.clear()
            
        return True
    
    def checkCol(self, col):
        # returns the missing numbers from a column
        foundNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        for row in range(0, 9):
            if self.board[row][col] in foundNums:
                foundNums.remove(self.board[row][col])
                
        if len(foundNums) == 0:
            return None
        return foundNums
        
    def checkRow(self, row):
        # returns the missing numbers from a row
        foundNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        for cell in self.board[row]:
            if cell in foundNums:
                foundNums.remove(cell)
        
        if len(foundNums) == 0:
            return None
        return foundNums

    def checkBox(self, boxNum):
        # returns the missing numbers from a box
        box = self.boxKey[boxNum]
        foundNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        for row in range(box[0], box[0] + 3):
            for col in range(box[1], box[1] + 3):
                if self.board[row][col] in foundNums:
                    foundNums.remove(self.board[row][col])
        
        if len(foundNums) == 0:
            return None
        return foundNums

    def common_member(self, a, b):
        result = [i for i in a if i in b]
        return result

    def canPlace(self, row, col, cell):
        # returns True if it is possible to play cell at position (row, col)
        tempBoard = copy.deepcopy(self.board)

        if tempBoard[row][col] == 0:
            tempBoard[row][col] = cell
            ss = SudokuSolver(tempBoard)
            return ss.correct()

        return False

    def getBoxNum(self, row, col):
        # returns the number of the box based on the row and col
        # returns -1 if invalid
        boxNum = -1
        for i in range(0, 9):
            if (row, col) in self.boxRef[i]:
                boxNum = i
        return boxNum

    def getPossibleNums(self, row, col):
        # returns the possible numbers that could go in (row, col)
        missingRow = self.checkRow(row)
        missingCol = self.checkCol(col)
        missingBox = self.checkBox(self.getBoxNum(row, col))
        common = self.common_member(missingRow, missingCol)
        return self.common_member(common, missingBox)


    def solveCell(self, row, col):
        # returns a number [1, 9] if it finds a definite solution
        # otherwise returns None

        # first determine which box the cell is in
        # this also shows if row and col are valid
        boxNum = self.getBoxNum(row, col)
                 
        if boxNum != -1 and self.board[row][col] == 0:
            # if it is a valid row and col

            # check if the cell is the last in a row
            missingRow = self.checkRow(row)
            if len(missingRow) == 1:
                self.board[row][col] = missingRow[0]
                return missingRow[0]

            # checks if the cell is the last in a column
            missingCol = self.checkCol(col)
            if len(missingCol) == 1:
                self.board[row][col] = missingCol[0]
                return missingCol[0]

            # checks if the cell is the last in a box
            missingBox = self.checkBox(boxNum)
            if len(missingBox) == 1:
                self.board[row][col] = missingBox[0]
                return missingBox[0]

            # otherwise, finds the numbers it could be
            # by finding the numbers common to the row, col, and box
            common = self.common_member(missingRow, missingCol)
            possibleNums = self.common_member(common, missingBox)

            # if only one possibility, it is solved
            if len(possibleNums) == 1:
                self.board[row][col] = possibleNums[0]
                # print(self.board[row][col], "success")
                return possibleNums[0]
            else:
                # otherwise, check if there is a number that can only be placed at (row, col)
                box = self.boxKey[boxNum]
                defNum = copy.deepcopy(possibleNums)
                for num in possibleNums:
                    # check if there is a number that can only be placed there
                    for bRow in range(box[0], box[0] + 3):
                        for bCol in range(box[1], box[1] + 3):
                            if self.canPlace(bRow, bCol, num) and (bRow, bCol) != (row, col) and num in defNum:
                                defNum.remove(num)
                # print("defNum", defNum)
                if len(defNum) == 1:
                    self.board[row][col] = defNum[0]
                    return defNum[0]

                # if it finds no definite solution, returns None
                return None

    def solveBoard(self):
        while not self.solved():
            tempBoard = copy.deepcopy(self.board)
            for row in range(0, 9):
                for col in range(0, 9):
                    self.solveCell(row, col)
            if not self.correct():
                # print("error solving")
                return None
            elif tempBoard == self.board and not self.solved():
                # print("unable to solve - too difficult")
                # print("this is as far as I got:")
                # self.print_board()
                # print("I am going to have to guess!")
                for row in range(0, 9):
                    for col in range(0, 9):
                        if self.board[row][col] == 0:
                            for num in self.getPossibleNums(row, col):
                                guess = self.make_guess(row, col, num, tempBoard)
                                if guess is not None:
                                    print("found a solution")
                                    self.board = guess
                                    return self.board
                return None
        self.print_board()
        return self.board


    def make_guess(self, row, col, num, board):
        tempBoard = copy.deepcopy(board)
        tempBoard[row][col] = num
        ss = SudokuSolver(tempBoard)
        return ss.solveBoard()
