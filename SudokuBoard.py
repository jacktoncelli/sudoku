class SudokuBoard:
    # key of the top right corners of each box of the board
    boxKey = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
    
    
    def __init__(self, board):
        """
        Initilize a sudoku board object with a 9x9 matrix input
        Raises an exception for invalid input
        
        Parameters:
        board([int][int]) - a 9x9 matrix where a 0 is an empty square, a 1-9 is the number i a puzzle
        """
        
        self.board = board
        if len(board) != 9 or len(board[0]) != 9  or not self.valid():
            raise Exception("Invalid board input")
        
        
    def print_board(self):
        """
        Prints a user-friendly representation of the current board
        """
        for row in range(0, 9):
            for col in range(0, 9):
                if (col) % 3 == 0:
                    print("   ", self.board[row][col], end=" ")
                else:
                    print("", self.board[row][col], end=" ")
                if (row + 1) % 3 == 0 and col == 8:
                    print("\n")
            print()
            
    def top_left_of_box(self, boxNum):
        """
        Given a box number from 0-8, returns the coordinate of 
        the top left corner of that box
        
        Ex: top_left_of_box(3) => (3, 0)
        
        Parameters:
        boxNum(int) - the box number on the board where box 0 is the top left and 
                      box 8 is the bottom right box and the box number increments left-right first
        
        Returns:
        top_left((int, int)) - a tuple in the format (row, column), where board[row][col]
                               is the top left corner of the given box
        """
        return self.boxKey[boxNum]
            
    def change_square(self, row, col, newVal):
        """
        Given a row and column and a new value for the square,
        replaces the value in the board of the square with newVal
        
        Parameters:
        row(int) - 0 <= row <= 8
        col(int) - 0 <= col <= 8
        newVal(int) - 1 <= newVal <= 9, the new value for the square
        
        """
        self.board[row][col] = newVal
        

    def get_square(self, row, col):
        """
        Get the current number at board[row][col]
        
        Parameters:
        row(int) - 0 <= row <= 8
        col(int) - 0 <= col <= 8
        
        Returns:
        square(int) - the current number at board[row][col], where 0 is an empty square
        
        """
        return self.board[row][col]
    
    def getBoxNum(self, row, col):
        """
        Given a row and column, returns the box number from 0-8
        where box 0 is the top left and box 8 is the bottom right box
        and the box number increments left-right first
        
        Ex: getBoxNum(0, 7) => 6
        
        Parameters:
        row(int) - 0 <= row <= 8
        col(int) - 0 <= col <= 8
        
        Returns:
        boxNum(int) - the box number between 0 and 8
        """
        
        box_row = row // 3
        box_col = col // 3
        boxNum = box_row * 3 + box_col
        return boxNum
    
    def missing_from_col(self, col):
        """
        Given a column between 0 and 8, 
        returns the numbers that do not yet appear
        from 1-9
        
        Parameters:
        col(int) - the column to check for missing numbers
        
        Returns:
        missing([int]) - List of the numbers not yet found        
        """
        missing = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        for row in range(0, 9):
            if self.get_square(row, col) in missing:
                missing.remove(self.get_square(row=row, col=col))
                
        return missing
    
    def missing_from_row(self, row):
        """
        Given a row between 0 and 8, 
        returns the numbers that do not yet appear from 1-9
        
        Parameters:
        row(int) - the row to check for missing numbers
        
        Returns:
        missing([int]) - List of the numbers not yet found        
        """
        missing = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        for col in range(0, 9):
            if self.get_square(row, col) in missing:
                missing.remove(self.get_square(row=row, col=col))
                
        return missing
    
    def can_place(self, row, col, value):
        """
        For a given coordinate at (row, col) on the board, 
        determines if value can be placed there without breaking any rules
        
        Parameters:
        row(int) - 0 <= row <= 8
        col(int) - 0 <= col <= 8
        value(int) - 1 <= value <= 9
        
        Returns:
        can_place(boolean) - True if value can be placed at self.board[row][col]
        """
        return value in self.possible_values(row, col)
    
    def missing_from_box(self, boxNum):
        """
        Given a box number from 0-8, 
        returns the numbers that do not yet appear in that box from 0-9
        
        Parameters:
        boxNum(int) - index of which box to check, where 0 is top left and 8 is bottom right
        
        Returns:
        missing([int]) - List of numbers not yet found
        """
        missing = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        # gets the top left corner of the given box
        box = self.top_left_of_box(boxNum)

        for row in range(box[0], box[0] + 3):
            for col in range(box[1], box[1] + 3):
                if self.board[row][col] in missing:
                    missing.remove(self.board[row][col])

        return missing
    
    def possible_placements_in_box(self, num, boxNum):
        """
        Given a number 1-9 and a box number returns a list of all the possible placements in the box
        in the format (row, column) without breaking any rules
        
        Parameters:
        num(int) - 1 <= num <= 9
        boxNum - 0 <= boxNum <= 8
        
        Returns:
        possible_placements([(int, int)]) - list of the coordinates where num can be placed in 
        the given box
        """
        possible_placements = []
        
        (top_left_row, top_left_col) = self.top_left_of_box(boxNum=boxNum)
        
        for row in range(top_left_row, top_left_row + 3):
            for col in range(top_left_col, top_left_col + 3):
                if self.can_place(row=row, col=col, value=num):
                    possible_placements.append((row, col))
                    
        return possible_placements
    
    def possible_row_placements_in_box(self, num, boxNum):
        """
        Given a number 1-9 and a box number returns a list of all the possible rows 
        that the number could be placed in without breaking any rules
        
        Parameters:
        num(int) - 1 <= num <= 9
        boxNum - 0 <= boxNum <= 8
        
        Returns:
        possible_rows([int]) - list of the rows where num can be placed in 
        the given box
        """
        possible_rows = []
        
        (top_left_row, top_left_col) = self.top_left_of_box(boxNum=boxNum)
        
        for row in range(top_left_row, top_left_row + 3):
            for col in range(top_left_col, top_left_col + 3):
                if self.can_place(row=row, col=col, value=num) and row not in possible_rows:
                    possible_rows.append(row)
        return possible_rows
    
    def possible_col_placements_in_box(self, num, boxNum):
        """
        Given a number 1-9 and a box number returns a list of all the possible columns 
        that the number could be placed in without breaking any rules
        
        Parameters:
        num(int) - 1 <= num <= 9
        boxNum - 0 <= boxNum <= 8
        
        Returns:
        possible_columns([int]) - list of the columns where num can be placed in 
        the given box
        """
        possible_cols = []
        
        (top_left_row, top_left_col) = self.top_left_of_box(boxNum=boxNum)
        
        for row in range(top_left_row, top_left_row + 3):
            for col in range(top_left_col, top_left_col + 3):
                if self.can_place(row=row, col=col, value=num) and col not in possible_cols:
                    possible_cols.append(col)
        return possible_cols
        
    
    def possible_values(self, row, col):
        """
        Given a row and column, returns the only current possible values for the square
        at self.board[row][col] by removing the numbers found in the same box, row, and column
        
        Parameters:
        row(int) - 0 <= row <= 8
        col(int) - 0 <= col <= 8
        
        Returns:
        possible_values([int]) - list of the values that could be filled in at self.board[row][col]
        """
        if self.board[row][col] != 0:
            return []
        missing_from_box = self.missing_from_box(self.getBoxNum(row, col))
        missing_from_row = self.missing_from_row(row)
        missing_from_col = self.missing_from_col(col)
        
        return sorted(list(set(missing_from_box).intersection(set(missing_from_row).intersection(set(missing_from_col)))))
    
    def solved(self):
        """
        is the board fully filled in and correctly solved?
        
        Returns:
        solved(boolean) - True if the puzzle is complete and correct
        """
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return self.valid()
    
    def valid(self):
        """
        Does the board follow the rules of sudoku?
        (I.e., no repeats in rows, columns, or boxes, 
        and only values of 0-9)
        
        Returns:
        correct(boolean) - True if the puzzle follows all rules
        """
        # verifies that every value is between 0 and 9
        for row in self.board:
            for cell in row:
                if not (0 <= cell <= 9):
                    return False
        
        seenNumsBox = set()

        # check each box for repeats
        for boxNum in range(0, 9):
            (r, c) = self.top_left_of_box(boxNum=boxNum)
            for row in range(r, r + 3):
                for col in range(c, c + 3):
                    if self.board[row][col] not in seenNumsBox and self.board[row][col] != 0:
                        seenNumsBox.add(self.board[row][col])
                    elif self.board[row][col] in seenNumsBox:
                        return False
            seenNumsBox.clear()

        seenNumsRow = set()
        
        # check each row for repeats
        for row in self.board:
            for cell in row:
                if cell not in seenNumsRow and cell != 0:
                    seenNumsRow.add(cell)
                elif cell in seenNumsRow:
                    return False
            seenNumsRow.clear()

        seenNumsCol = set()
        # check each column for repeats
        seenNumsCol.clear()
        for col in range(0, 9):
            for row in range(0, 9):
                if self.board[row][col] not in seenNumsCol and self.board[row][col] != 0:
                    seenNumsCol.add(self.board[row][col])
                elif self.board[row][col] in seenNumsCol:
                    return False
            seenNumsCol.clear()

        return True