import unittest
from SudokuBoard import SudokuBoard
from SudokuSolver import SudokuSolver
import copy

class TestSudokuBoardMethods(unittest.TestCase):
    # testing methods for all class methods of Sudoku Board
    board_array = [
        [7, 0, 0, 0, 0, 0, 0, 6, 3],
        [0, 0, 2, 6, 7, 3, 4, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],

        [0, 3, 9, 0, 0, 0, 2, 0, 1],
        [5, 7, 4, 0, 2, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 5, 8, 7, 0],

        [1, 8, 0, 2, 6, 0, 0, 3, 0],
        [0, 0, 0, 0, 0, 7, 0, 2, 8],
        [0, 6, 0, 0, 9, 0, 1, 0, 0]
    ]
    
    ex_board = SudokuBoard(board_array)

    def test_init(self):
        with self.assertRaises(Exception):
            # check that boards of the wrong size cannot be initialized
            SudokuBoard([
                [0, 0, 0],
                [0, 1, 2]
            ])
            # check that a board that breaks the rules of sudoku cannot be initialized
            SudokuBoard([
                [7, 0, 0, 0, 0, 7, 0, 6, 3],
                [0, 0, 2, 6, 7, 3, 4, 0, 0],
                [0, 4, 0, 0, 0, 0, 0, 0, 0],

                [0, 3, 9, 0, 0, 0, 2, 0, 1],
                [5, 7, 4, 0, 2, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 5, 8, 7, 0],

                [1, 8, 0, 2, 6, 0, 0, 3, 0],
                [0, 0, 0, 0, 0, 7, 0, 2, 8],
                [0, 6, 0, 0, 9, 0, 1, 0, 0]
            ])
            
    def test_top_left_of_box(self):
        self.assertEqual(self.ex_board.top_left_of_box(boxNum=0), (0, 0))
        self.assertEqual(self.ex_board.top_left_of_box(boxNum=1), (0, 3))
        self.assertEqual(self.ex_board.top_left_of_box(boxNum=2), (0, 6))
        self.assertEqual(self.ex_board.top_left_of_box(boxNum=3), (3, 0))
        self.assertEqual(self.ex_board.top_left_of_box(boxNum=4), (3, 3))
        self.assertEqual(self.ex_board.top_left_of_box(boxNum=5), (3, 6))
        self.assertEqual(self.ex_board.top_left_of_box(boxNum=6), (6, 0))
        self.assertEqual(self.ex_board.top_left_of_box(boxNum=7), (6, 3))
        self.assertEqual(self.ex_board.top_left_of_box(boxNum=8), (6, 6))
        
    def test_change_square(self):
        temp_board = SudokuBoard(board=copy.deepcopy(self.board_array))
        temp_board.change_square(row=0, col=0, newVal=9)
        self.assertEqual(temp_board.get_square(row=0, col=0), 9)
        
        temp_board.change_square(row=5, col=5, newVal=6)
        self.assertEqual(temp_board.get_square(row=5, col=5), 6)
        
        temp_board.change_square(row=8, col=8, newVal=1)
        self.assertEqual(temp_board.get_square(row=8, col=8), 1)
        
    def test_get_square(self):
        self.assertEqual(self.ex_board.get_square(row=0, col=0), 7)
        self.assertEqual(self.ex_board.get_square(row=3, col=6), 2)
        self.assertEqual(self.ex_board.get_square(row=6, col=7), 3)
        self.assertEqual(self.ex_board.get_square(row=8, col=8), 0)
        
    def test_getBoxNum(self):
        self.assertEqual(self.ex_board.getBoxNum(row=0, col=0), 0)
        self.assertEqual(self.ex_board.getBoxNum(row=1, col=7), 2)
        self.assertEqual(self.ex_board.getBoxNum(row=3, col=2), 3)
        self.assertEqual(self.ex_board.getBoxNum(row=6, col=5), 7)
        self.assertEqual(self.ex_board.getBoxNum(row=5, col=5), 4)
    
    def test_missing_from_col(self):
        self.assertListEqual(self.ex_board.missing_from_col(0), [2, 3, 4, 6, 8, 9])
        self.assertListEqual(self.ex_board.missing_from_col(1), [1, 2, 5, 9])
        self.assertListEqual(self.ex_board.missing_from_col(2), [3, 5, 6, 7, 8])
        self.assertListEqual(self.ex_board.missing_from_col(3), [1, 3, 4, 5, 7, 8, 9])
        self.assertListEqual(self.ex_board.missing_from_col(4), [1, 3, 4, 5, 8])
        self.assertListEqual(self.ex_board.missing_from_col(5), [1, 2, 4, 6, 8, 9])
        self.assertListEqual(self.ex_board.missing_from_col(6), [3, 5, 6, 7, 9])
        self.assertListEqual(self.ex_board.missing_from_col(7), [1, 4, 5, 8, 9, ])
        self.assertListEqual(self.ex_board.missing_from_col(8), [2, 4, 5, 6, 7, 9])
        
    def test_missing_from_row(self):
        self.assertListEqual(self.ex_board.missing_from_row(0), [1, 2, 4, 5, 8, 9])
        self.assertListEqual(self.ex_board.missing_from_row(1), [1, 5, 8, 9])
        self.assertListEqual(self.ex_board.missing_from_row(2), [1, 2, 3, 5, 6, 7, 8, 9])
        self.assertListEqual(self.ex_board.missing_from_row(3), [4, 5, 6, 7, 8])
        self.assertListEqual(self.ex_board.missing_from_row(4), [1, 3, 6, 8, 9])
        self.assertListEqual(self.ex_board.missing_from_row(5), [2, 3, 4, 6, 9])
        self.assertListEqual(self.ex_board.missing_from_row(6), [4, 5, 7, 9])
        self.assertListEqual(self.ex_board.missing_from_row(7), [1, 3, 4, 5, 6, 9])
        self.assertListEqual(self.ex_board.missing_from_row(8), [2, 3, 4, 5, 7, 8])
    
    def test_can_place(self):
        self.assertFalse(self.ex_board.can_place(row=0, col=0, value=2))
        self.assertFalse(self.ex_board.can_place(row=0, col=1, value=4))
        self.assertFalse(self.ex_board.can_place(row=3, col=5, value=1))
        self.assertFalse(self.ex_board.can_place(row=8, col=0, value=8))
        
        self.assertTrue(self.ex_board.can_place(row=0, col=1, value=5))
        self.assertTrue(self.ex_board.can_place(row=5, col=4, value=3))
        self.assertTrue(self.ex_board.can_place(row=6, col=6, value=7))
        self.assertTrue(self.ex_board.can_place(row=2, col=7, value=9))
        
    def test_missing_from_box(self):
        self.assertEqual(self.ex_board.missing_from_box(0), [1, 3, 5, 6, 8, 9])
        self.assertEqual(self.ex_board.missing_from_box(1), [1, 2, 4, 5, 8, 9])
        self.assertEqual(self.ex_board.missing_from_box(2), [1, 2, 5, 7, 8, 9])
        self.assertEqual(self.ex_board.missing_from_box(3), [2, 6, 8])
        self.assertEqual(self.ex_board.missing_from_box(4), [1, 3, 4, 6, 7, 8, 9])
        self.assertEqual(self.ex_board.missing_from_box(5), [3, 4, 5, 6, 9])
        self.assertEqual(self.ex_board.missing_from_box(6), [2, 3, 4, 5, 7, 9])
        self.assertEqual(self.ex_board.missing_from_box(7), [1, 3, 4, 5, 8])
        self.assertEqual(self.ex_board.missing_from_box(8), [4, 5, 6, 7, 9])
    
    def test_possible_placements_in_box(self):
        self.assertEqual(
            self.ex_board.possible_placements_in_box(num=2, boxNum=0), 
            [])
        self.assertEqual(
            self.ex_board.possible_placements_in_box(num=4, boxNum=3),
            [])
        self.assertEqual(
            self.ex_board.possible_placements_in_box(num=1, boxNum=0), 
            [(0, 1), (1, 1)])
        self.assertEqual(
            self.ex_board.possible_placements_in_box(num=3, boxNum=0), 
            [(2, 0), (2, 2)])
        self.assertEqual(
            self.ex_board.possible_placements_in_box(num=4, boxNum=4), 
            [(3, 3), (3, 4), (3, 5), (5, 3), (5, 4)])
        self.assertEqual(
            self.ex_board.possible_placements_in_box(num=9, boxNum=8),
            [(6, 6), (6, 8), (7, 6)])
        self.assertEqual(
            self.ex_board.possible_placements_in_box(num=5, boxNum=6),
            [(6, 2), (7, 1), (7, 2), (8, 2)])
        
    def test_possible_row_placements_in_box(self):
        self.assertEqual(
            self.ex_board.possible_row_placements_in_box(num=1, boxNum=0), [0, 1])
        self.assertEqual(
            self.ex_board.possible_row_placements_in_box(num=7, boxNum=0), [])
        self.assertEqual(
            self.ex_board.possible_row_placements_in_box(num=3, boxNum=0), [2])
        self.assertEqual(
            self.ex_board.possible_row_placements_in_box(num=9, boxNum=5), [4, 5])
        self.assertEqual(
            self.ex_board.possible_row_placements_in_box(num=3, boxNum=7), [7, 8])
        self.assertEqual(
            self.ex_board.possible_row_placements_in_box(num=4, boxNum=6), [7, 8])
        
    def test_possible_col_placements_in_box(self):
        self.assertEqual(
            self.ex_board.possible_col_placements_in_box(num=1, boxNum=0), [1])
        self.assertEqual(
            self.ex_board.possible_col_placements_in_box(num=7, boxNum=0), [])
        self.assertEqual(
            self.ex_board.possible_col_placements_in_box(num=3, boxNum=0), [0, 2])
        self.assertEqual(
            self.ex_board.possible_col_placements_in_box(num=9, boxNum=5), [6, 7, 8])
        self.assertEqual(
            self.ex_board.possible_col_placements_in_box(num=3, boxNum=7), [3, 4])
        self.assertEqual(
            self.ex_board.possible_col_placements_in_box(num=4, boxNum=6), [0])
        
    def test_possible_values(self):
        self.assertEqual(self.ex_board.possible_values(row=0, col=0), [])
        self.assertEqual(self.ex_board.possible_values(row=0, col=1), [1, 5, 9])
        self.assertEqual(self.ex_board.possible_values(row=3, col=0), [6, 8])
        self.assertEqual(self.ex_board.possible_values(row=4, col=3), [1, 3, 8, 9])
        self.assertEqual(self.ex_board.possible_values(row=6, col=6), [5, 7, 9])
        self.assertEqual(self.ex_board.possible_values(row=7, col=4), [1, 3, 4, 5])
        self.assertEqual(self.ex_board.possible_values(row=8, col=8), [4, 5, 7])
        
    def test_solved(self):
        self.assertFalse(self.ex_board.solved())
        
        self.assertTrue(SudokuBoard([
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],

            [3, 1, 2, 6, 4, 5, 9, 7, 8],
            [9, 7, 8, 3, 1, 2, 6, 4, 5],
            [6, 4, 5, 9, 7, 8, 3, 1, 2],

            [2, 3, 1, 5, 6, 4, 8, 9, 7],
            [8, 9, 7, 2, 3, 1, 5, 6, 4],
            [5, 6, 4, 8, 9, 7, 2, 3, 1]
        ]).solved())
        
    def test_valid(self):
        temp_board = SudokuBoard(copy.deepcopy(self.board_array))
        self.assertTrue(temp_board.valid())
        
        # same as another number in the box
        temp_board.change_square(row=0, col=1, newVal=7)
        self.assertFalse(temp_board.valid())
        temp_board.change_square(row=0, col=1, newVal=0)
        
        # same as another number in the row
        temp_board.change_square(row=0, col=2, newVal=3)
        self.assertFalse(temp_board.valid())
        temp_board.change_square(row=0, col=2, newVal=0)
        
        # same as another number in the column
        temp_board.change_square(row=0, col=1, newVal=8)
        self.assertFalse(temp_board.valid())
        
class TestSudokuSolverMethods(unittest.TestCase):
    board_array = [
        [7, 0, 0, 0, 0, 0, 0, 6, 3],
        [0, 0, 2, 6, 7, 3, 4, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],

        [0, 3, 9, 0, 0, 0, 2, 0, 1],
        [5, 7, 4, 0, 2, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 5, 8, 7, 0],

        [1, 8, 0, 2, 6, 0, 0, 3, 0],
        [0, 0, 0, 0, 0, 7, 0, 2, 8],
        [0, 6, 0, 0, 9, 0, 1, 0, 0]
    ]
    
    ex_board = SudokuBoard(board_array)
    ex_solver = SudokuSolver(ex_board)
    
    def test_horizontally_adjacent_boxes(self):
        self.assertEqual(self.ex_solver.horizontally_adjacent_boxes(0), (1, 2))
        self.assertEqual(self.ex_solver.horizontally_adjacent_boxes(1), (0, 2))
        self.assertEqual(self.ex_solver.horizontally_adjacent_boxes(2), (0, 1))
        self.assertEqual(self.ex_solver.horizontally_adjacent_boxes(3), (4, 5))
        self.assertEqual(self.ex_solver.horizontally_adjacent_boxes(4), (3, 5))
        self.assertEqual(self.ex_solver.horizontally_adjacent_boxes(5), (3, 4))
        self.assertEqual(self.ex_solver.horizontally_adjacent_boxes(6), (7, 8))
        self.assertEqual(self.ex_solver.horizontally_adjacent_boxes(7), (6, 8))
        self.assertEqual(self.ex_solver.horizontally_adjacent_boxes(8), (6, 7))
    
    def test_vertically_adjacent_boxes(self):
        self.assertEqual(self.ex_solver.vertically_adjacent_boxes(0), (3, 6))
        self.assertEqual(self.ex_solver.vertically_adjacent_boxes(1), (4, 7))
        self.assertEqual(self.ex_solver.vertically_adjacent_boxes(2), (5, 8))
        self.assertEqual(self.ex_solver.vertically_adjacent_boxes(3), (0, 6))
        self.assertEqual(self.ex_solver.vertically_adjacent_boxes(4), (1, 7))
        self.assertEqual(self.ex_solver.vertically_adjacent_boxes(5), (2, 8))
        self.assertEqual(self.ex_solver.vertically_adjacent_boxes(6), (0, 3))
        self.assertEqual(self.ex_solver.vertically_adjacent_boxes(7), (1, 4))
        self.assertEqual(self.ex_solver.vertically_adjacent_boxes(8), (2, 5))
    
    def test_solve_square(self):
        temp_solver = SudokuSolver(SudokuBoard(copy.deepcopy(self.board_array)))
        
        update_4_6 = temp_solver.solve_square(row=4, col=6)
        self.assertFalse(update_4_6)
        # it should not be able to solve the (4, 6) square using standard logic
        
        update_0_1 = temp_solver.solve_square(row=0, col=1)
        self.assertFalse(update_0_1)
        
        update_0_2 = temp_solver.solve_square(row=0, col=2)
        self.assertFalse(update_0_2)
        
        update_5_1 = temp_solver.solve_square(row=5, col=1)
        self.assertTrue(update_5_1)
        self.assertEqual(temp_solver.get_square(row=5, col=1), 2)
        # it can update the (5, 1) square to 2 using standard logic
        
        update_5_0 = temp_solver.solve_square(row=5, col=0)
        self.assertTrue(update_5_0)
        self.assertEqual(temp_solver.get_square(row=5, col=0), 6)
        
        update_3_0 = temp_solver.solve_square(row=3, col=0)
        self.assertTrue(update_3_0)
        self.assertEqual(temp_solver.get_square(row=3, col=0), 8)
        
        update_3_4 = temp_solver.solve_square(row=3, col=4)
        self.assertTrue(update_3_4)
        self.assertEqual(temp_solver.get_square(row=3, col=4), 4)
        
    def test_row_column_elimination(self):
        # using row/column elimination, it can reduce the possible placements for 8 in box 0 to [(0, 2), (2, 2)]
        self.assertEqual(self.ex_solver.row_column_elimination(boxNum=0, target_num=8), [(0, 2), (2, 2)])
        self.assertEqual(self.ex_solver.row_column_elimination(boxNum=0, target_num=6), [(2, 2)])        

        self.assertEqual(self.ex_solver.row_column_elimination(boxNum=5, target_num=3), [(4, 6)])
        
    def test_pair_elimination(self):
        temp_board = [
            [0, 0, 0, 0, 0, 0, 1, 2, 0],
            [6, 5, 4, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        temp_solver = SudokuSolver(SudokuBoard(temp_board))
        
        self.assertEqual(temp_solver.pair_elimination(boxNum=0, target_num=7),
                         [(0, 0), (0, 1), (0, 2)])
        self.assertEqual(temp_solver.pair_elimination(boxNum=0, target_num=8),
                         [(0, 0), (0, 1), (0, 2)])
        self.assertEqual(temp_solver.pair_elimination(boxNum=0, target_num=9),
                         [(0, 0), (0, 1), (0, 2)])
        
    
if __name__ == '__main__':
    unittest.main()