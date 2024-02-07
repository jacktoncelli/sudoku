class SudokuSolver:
    calls_to_solve_square = 0
    calls_to_solve_box = 0
    
    def __init__(self, board):
        """
        Intializes a new SudokuSolver instance
        
        Parameters:
        board(SudokuBoard) - the puzzle to be solved
        """
        self.board = board
    
    def print_board(self):
        """
        Prints a user-friendly text representation of the current board
        """
        self.board.print_board()
        
    def get_square(self, row, col):
        """
        Get the current number at board[row][col]
        
        Parameters:
        row(int) - 0 <= row <= 8
        col(int) - 0 <= col <= 8
        
        Returns:
        square(int) - the current number at board[row][col], where 0 is an empty square
        
        """
        return self.board.get_square(row=row, col=col)
            
    def horizontally_adjacent_boxes(self, boxNum):
        """
        Given a box number, will return the box numbers of the horizontally adjacent boxes
        Note: this includes all boxes at the same horizontal level, 
        for example, horizontally_adjacent_boxes(0) => (1, 2)
        
        Parameters:
        boxNum(int) - 0 <= boxNum <= 8, where 0 is top left box, 8 is bottom right box, and box number increments left-right first
        
        Returns:
        h_adj_boxNums((int, int)) - the box numbers of the two horizontally adjacent boxes
        """
        h_adj_box_key = [
            (1, 2), 
            (0, 2), 
            (0, 1), 
            (4, 5), 
            (3, 5), 
            (3, 4), 
            (7, 8), 
            (6, 8), 
            (6, 7)
        ]
        return h_adj_box_key[boxNum]
    
    def vertically_adjacent_boxes(self, boxNum):
        """
        Given a box number, will return the box numbers of the vertically adjacent boxes
        Note: this includes all boxes at the same vertical level, 
        for example, vertcally_adjacent_boxes(0) => (3, 6)
        
        Parameters:
        boxNum(int) - 0 <= boxNum <= 8, where 0 is top left box, 8 is bottom right box, and box number increments left-right first
        
        Returns:
        v_adj_boxNums((int, int)) - the box numbers of the two horizontally adjacent boxes
        """
        v_adj_box_key = [
            (3, 6), 
            (4, 7), 
            (5, 8), 
            (0, 6), 
            (1, 7), 
            (2, 8), 
            (0, 3), 
            (1, 4), 
            (2, 5)
        ]
        return v_adj_box_key[boxNum]
        
        
    def solve_square(self, row, col):
        """
        Given a row and column, tries to solve the square in the puzzle 
        at self.baord[row][col]. Will leave as 0 if not currently able to.
        
        Parameters:
        row(int) - 0 <= row <= 8
        col(int) - 0 <= col <= 8
        
        Returns:
        updated(boolean) - True if a solution was found, False otherwise
        """
        self.calls_to_solve_square += 1
        
        if self.board.get_square(row, col) != 0:
            return False
       
        possible_vals = self.board.possible_values(row, col)
        
        updated = False
        
        if len(possible_vals) == 1:
            self.board.change_square(row=row, col=col, newVal=possible_vals[0])
            updated = True
            
        return updated
    
    def pair_elimination(self, boxNum, target_num):
        """
        Given a box number from 0-8 and a number from 1-9 not yet found in that box, will determine if the 
        possible placements for num in the box can be reduced using pair elimination
        
        Parameters:
        boxNum(int) - 0 <= boxNum <= 8, where 0 is top left box, 8 is bottom right box, and box number increments left-right first
        target_num(int) - 1 <= num <= 9, the number to determine possible placements for 
        
        Returns:
        possible_placements([(int, int)]) - a list of possible placements for target_num
        """
        missing_nums = self.board.missing_from_box(boxNum)
        if target_num not in missing_nums:
            return []
        missing_nums.remove(target_num)
        
        possible_placements = self.board.possible_placements_in_box(boxNum=boxNum, num=target_num)
        
        seen_pair_placements = []
        # the already seen pair placements for the other numbers in the box
        
        to_remove = []
        # the placements to be removed from possible_placements
        
        for num in missing_nums:
            possible_placements_other = self.board.possible_placements_in_box(num=num, boxNum=boxNum)
            if len(possible_placements_other) == 2 and possible_placements_other in seen_pair_placements:
                # if the pair is already seen, then there are two and it can be removed from possible_placements
                to_remove.append(possible_placements_other[0])
                to_remove.append(possible_placements_other[1])
            elif len(possible_placements_other) == 2:
                seen_pair_placements.append(possible_placements_other)
                
        for i in range(len(to_remove)):
            if(to_remove[i] in possible_placements):
                possible_placements.remove(to_remove[i])
            
        return possible_placements
    
    def row_column_elimination(self, boxNum, target_num):
        """
        Given a box number and a target number, will find the possible placements in the box for 
        the target number using row/column elimination
        
        Parameters:
        boxNum(int) - 0 <= boxNum <= 8, where 0 is top left box, 8 is bottom right box, and box number increments left-right first
        target_num(int) - 1 <= num <= 9, the number to determine possible placements for 
        
        Returns:
        possible_placements([(int, int)]) - a list of possible placements for target_num
        """
        possible_placements = self.board.possible_placements_in_box(boxNum=boxNum, num=target_num)
                
        horiz_adj_boxes = self.horizontally_adjacent_boxes(boxNum=boxNum)
        # row elimination
        
        # first eliminate the definite rows from possible_placements
        for h_adj_box in horiz_adj_boxes:
            possible_rows_other = self.board.possible_row_placements_in_box(num=target_num, boxNum=h_adj_box)
            
            # then it is known that in another box, num will go in this row, so it cannot go there in this box
            if len(possible_rows_other) == 1:
                for (possible_row, possible_col) in possible_placements:
                    to_remove = []
                    if len(possible_placements) > 0 and possible_row == possible_rows_other[0]:
                        to_remove.append((possible_row, possible_col))
                    for i in range(len(to_remove)):
                        possible_placements.remove(to_remove[i])
                
        possible_rows_horiz = set()
        # in case the other two rows have narrowed the certainty down to two rows total, 
        # that would want to be removed form possible_placements as well
        for h_adj_box in horiz_adj_boxes:
            possible_rows_horiz = possible_rows_horiz.union(
                self.board.possible_row_placements_in_box(num=target_num, boxNum=h_adj_box))
            
        possible_rows_horiz = list(possible_rows_horiz)
        # if there were 3 possible rows in the other two boxes, 
        # no conclusions would be able to be drawn
        if len(possible_rows_horiz) != 3:
            # remove the coordinates from possible_placements in the rows 
            # that match the possible rows of the horizontally adjacent boxes
            for removable_row in possible_rows_horiz:
                to_remove = []
                for (possible_row, possible_col) in possible_placements:
                    if len(possible_placements) > 0 and possible_row == removable_row:
                        to_remove.append((possible_row, possible_col))
                for i in range(len(to_remove)):
                    possible_placements.remove(to_remove[i])
                    
        # column elimination
        vert_adj_boxes = self.vertically_adjacent_boxes(boxNum=boxNum)
        
        # first eliminate the definite columns from possible_placements
        for v_adj_box in vert_adj_boxes:
            possible_cols_other = self.board.possible_col_placements_in_box(num=target_num, boxNum=h_adj_box)
            
            # then it is known that in another box, num will go in this col, so it cannot go there in this box
            if len(possible_cols_other) == 1:
                for (possible_row, possible_col) in possible_placements:
                    to_remove = []
                    if len(possible_placements) > 0 and possible_col == possible_cols_other[0]:
                        to_remove.append((possible_row, possible_col))
                    for i in range(len(to_remove)):
                        possible_placements.remove(to_remove[i])
        
        possible_cols_vert = set()
        # find the possible columns for num in the vertically adjacent boxes
        for v_adj_box in vert_adj_boxes:
            possible_cols_vert = possible_cols_vert.union(
                self.board.possible_col_placements_in_box(num=target_num, boxNum=v_adj_box)
            )
            
        possible_cols_vert = list(possible_cols_vert)
        # if there were 3 possible columns in the vertically adjacent boxes
        # then no conclusions can be drawn
        if len(possible_cols_vert) != 3:
            # remove the coordinates from possible_placements in the columns
            # that match the possible columns of the horizontally adjacent boxes
            for removeable_col in possible_cols_vert:
                to_remove = []
                for (possible_row, possible_col) in possible_placements:
                    if len(possible_placements) > 0 and possible_col == removeable_col:
                        to_remove.append((possible_row, possible_col))
                for i in range(len(to_remove)):
                    possible_placements.remove(to_remove[i])
 
        return possible_placements
            
            
    
    def solve_box_row_column_elimination(self, boxNum):
        """
        Given a box number from 0-8, tries to solve each unsolved sqaure in the box
        using row/column elimination logical inference
        Will leave unsolved squares as 0.
        
        Parameters:
        boxNum(int) - 0 <= boxNum <= 8, where 0 is top left box, 8 is bottom right box, and box number increments left-right first
        
        Returns:
        updated(boolean) - True if any changes were made, false otherwise
        """
        
        updated = True

        missing_nums = self.board.missing_from_box(boxNum)
        
        
        while updated and self.board.valid() and not self.board.solved():
            updated = False
            for num in missing_nums:
                possible_placements_in_box_rc = self.row_column_elimination(boxNum=boxNum, target_num=num)
                possible_placements_in_box_pair = self.pair_elimination(boxNum=boxNum, target_num=num)
            
                
                if not possible_placements_in_box_rc:
                    possible_placements = possible_placements_in_box_pair
                elif not possible_placements_in_box_pair:
                    possible_placements = possible_placements_in_box_rc
                else:  
                    possible_placements = list(set(possible_placements_in_box_rc).intersection(set(possible_placements_in_box_pair)))
                # if there is only one remaining possible placement for num, 
                # then a unique solution has been found and the square can be updated
                if len(possible_placements) == 1:
                    self.board.change_square(row=possible_placements[0][0], col=possible_placements[0][1], newVal=num)
                    updated = True
            
        return updated
        
    def solve_box(self, boxNum):
        """
        Given a box number from 0-8, tries to solve each unsolved sqaure in the box
        Will leave unsolved squares as 0
        
        Parameters:
        boxNum(int) - 0 <= boxNum <= 8, where 0 is top left box, 8 is bottom right box, and box number increments left-right first
        
        Returns:
        updated(boolean) - True if any changes were made, false otherwise
        """
        self.calls_to_solve_box += 1
        
        updated = False
        
        standard_logic_updated = True
        
        (top_left_row, top_left_col) = self.board.top_left_of_box(boxNum)
        
        while standard_logic_updated and self.board.valid() and not self.board.solved():
            # while updates are still being made and the board is neither invalid nor solved:
            standard_logic_updated = False
            for row in range(top_left_row, top_left_row + 3):
                for col in range(top_left_col, top_left_col + 3):
                    # try to solve each square in the box using conventional methods
                    update_square = self.solve_square(row, col)
                    if update_square:
                        updated = True
                        standard_logic_updated = True
        
        self.solve_box_row_column_elimination(boxNum=boxNum)
                    
        return updated
    
    def solve_board(self):
        """
        Attempts to solve the entire puzzle using an inference loop, 
        where it will call solve_box until no further changes are made
        
        Will print the starting board and the final state of the board 
        after all logic has been applied. 
        
        """
        print("Starting board:")
        self.print_board()
        
        updated = True
        
        while updated and self.board.valid() and not self.board.solved():
            updated = False
            for boxNum in range(0, 9):
                update_box = self.solve_box(boxNum)
                if update_box:
                    updated = True
                
                    
        if not self.board.valid():
            print("Invalid board")
        if self.board.solved():
            print("Solution found!")
        
        print("Final board:")
        self.print_board()
        
        print(f"# Calls to solve_square:{self.calls_to_solve_square}, # Calls to solve_box:{self.calls_to_solve_box}")