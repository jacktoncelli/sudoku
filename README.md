# sudoku
A rules-engine AI model using logical inference to solve sudoku puzzles

----------------

## Introduction

This project was built with the intention of being able to easily scale it's logical capabilites, and to challenge myself to find more and more ways to solve sudoku puzzles. The original code dates back to when I was in high school, but I've rewritten it after my first semester in college to produce more readable, clean, and less redundant code and apply the design principles that I have been learning in college. I've also since created a test suite to help with development and debugging. 

If you would like to understand what methods I have, and what they are for, feel free to look at the code directly. I've included docstrings on every method, and the majority of the methods are very simple and obvious, with a few exceptions. If you have any questions about how they work or suggestions to improve any part of this project, please feel free to reach out to me.

I've provided a high-level overview of how I designed this code and how I approached it from a logical standpoint.

<hr>

## Structure

There are two main classes in this project, **SudokuBoard** and **SudokuSolver**. 

**SudokuBoard** is meant to update the internal representation of the puzzle and provide various forms of information about it when asked. For this reason, a majority of the methods of **SudokuBoard** do not seem to do much in terms of logical inference, although when the information is utilized correctly, it becomes quite simple. Some examples of the information that the **SudokuBoard** methods provide include the current value of a given square, the numbers that are yet to be filled in a given box, etc. 

**SudokuSolver** is the class which collects the information about the board and uses it to draw conclusions about the board. For any given square on the board there is one definite solution, and it is up to the solver to find it. In order to do so, the various logical techniques, which are described below, are employed. Once the solver has either solved the board, found that it is unsolvable (i.e., breaks the rules of sudoku), or exhausted every logical technique and is unable to go further, it stops. In previous iterations of the project I had built in a guessing framework which makes an educated guess as to what a square _could_ be and tries it until it either solves it or breaks the rules. However, in rewriting the code, I found this to be a lazy and kind of sloppy decision, although it is effective. I would rather build in more advanced logical capabilites than resort to the obvious solution, as I consider the former to be more challenging and educational. I may eventually rewrite the guessing framework for the sake of it, once I'm satisfied with the other aspects of the AI. 

I will refer to box numbers, row numbers, and column numbers throughout this documentation, so here is a reference on how the numbering system works:

```md

Box number:

    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8

Row/column number:

Row increments going down, column increments going right.

       | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
     0 |   |   |   |   |   |   |   |   |   |
     1 |   |   |   |   |   |   |   |   |   |
     2 |   |   |   |   |   |   |   |   |   |
     3 |   |   |   |   |   |   |   |   |   |
     4 |   |   |   |   |   |   |   |   |   |
     5 |   |   |   |   |   |   |   |   |   |
     6 |   |   |   |   |   |   |   |   |   |
     7 |   |   |   |   |   |   |   |   |   |
     8 |   |   |   |   |   |   |   |   |   |

```

<hr>

## Logical Techniques

### Standard

The first technique is the route that many people take when initially playing sudoku. In every row, column, and box, each number from 1-9 must appear exactly once. So, if you check the numbers that are not yet found in the row, column, and box of a given square, and if there happens to be only one that isn't found in any of the three, than that is guaranteed to be the solution for that square. 

Below is an example: (a 0 represents an empty square)

```md

    7  0  0     0  0  0     0  6  3
    0  0  2     6  7  3     4  0  0
    0  4  0     0  0  0     0  0  0


    0  3  9     0  0  0     2  0  1
    5  7  4     0  2  0     0  0  0
    0  X  1     0  0  5     8  7  0


    1  8  0     2  6  0     0  3  0
    0  0  0     0  0  7     0  2  8
    0  6  0     0  9  0     1  0  0
```
On the board above, X is at row 5 and column 1. X currently does not have a solution. 

All the possible values for X are [1, 2, 3, 4, 5, 6, 7, 8, 9].

The values that already appear in row 5 already are [1, 5, 7, 8]. Removing these from the possible values for X leaves [2, 3, 4, 6, 9].

The values that already appear in column 1 are [3, 4, 6, 7, 8]. Removing these from the possible values for X leaves [2, 9].

The values that already appear in box 4 (middle left box) are [1, 3, 4, 5, 7, 9]. Removing these from the possible values for X leaves [2].

Since there is only one number that hasn't appeared in the row, column, and box of X, the solution _must_ be 2. 

### Row-column elimination

For a number that does not yet appear in a box, there are between 1-9 possible positions where it can be placed in that box. However, if it can only be placed in one row or one column, then that means that in the boxes around it, that number cannot be placed in the same row or column. Furthermore, if the number is already placed in adjacent boxes, then it cannot be placed in the same row or column as in the other boxes. That is why I call this method row-column elimination, because it eliminates a row where a given number can be placed from the possible positions. While standard logic focuses on what a given _square_ could be, row-column elimination finds where the _numbers_ must be, knowing that it has to appear in every box.

Below is an example illustrating how this technique works: (a 0 represents an empty square)

```md

    7  0  0     0  0  0     0  6  3
    0  0  2     6  7  3     4  0  0
    0  4  0     0  0  0     0  0  0


    0  3  9     0  0  0     2  0  1
    5  7  4     0  2  0     X  0  0
    0  0  1     0  0  5     8  7  0


    1  8  0     2  6  0     0  3  0
    0  0  0     0  0  7     0  2  8
    0  6  0     0  9  0     1  0  0
```

X is the square at row 4 and column 6. Standard logic will not be able to find a solution for this square, as the possible values are only reduced to [3, 6, 9]. We now have to narrow down the options and find which value is correct. 

Let's first list the possible placements for a 3 in box 5. In the format (row, column), that leaves [(3, 7), (4, 6), (4, 7), (4, 8), (5, 8)], since we haven't eliminated any possibilities yet. 

However, if you look at the rows where 3 can be placed within box 5, you will notice a 3 already placed in box 3 at (3, 2). This means that in box 5, we cannot place a 3 in the same row. So our updated list is [(4, 6), (4, 7), (4, 8), (5, 8)] after removing (3, 7) which has the same row as (3, 2).

Now let's look at the columns. After checking above in box 2, we see a 3 placed at (1, 8). So in box 5, we cannot place a 3 in column 8, so we can update our list of possible placements to [(4, 6), (4, 7)]. 

Looking below at box 8, we see a 3 placed at (6, 7), so we can similarly eliminate (4, 7) from our possible placements, leaving only [(4, 6)]. Thus, we have concluded that a 3 must be placed at (4, 6), where X is, as no other square in box 5 can have a 3. 

### Pair Elimination

In any given box, if 2 numbers can **only** be placed in the **same two squares**, then you can rule out all other numbers from those squares. This only applies if both numbers cannot be placed in any other square in the box using rules of elimination, and if the squares that they can be placed in are the same. This does not necessarily find a solution for those two squares, but it can lead to a solution elsewhere in the box by limiting where other numbers can be placed. 

Below is an example showing when this applies: (a 0 represents an empty square)

```md

    7  0  0     0  0  0     0  6  3
    0  0  2     6  7  3     4  0  0
    A  4  B     0  0  0     0  0  0


    0  3  9     0  0  0     2  0  1
    5  7  4     0  2  0     0  0  0
    0  0  1     0  0  5     8  7  0


    1  8  0     2  6  0     0  3  0
    0  0  0     0  0  7     0  2  8
    0  6  0     0  9  0     1  0  0
```

A is the square at row 2, column 0. B is the square at row 2, column 2. Both are in box 0.

If you look at where you can place 6 in box 0, you will narrow down your choices to [(2, 0), (2, 2)], or [A, B]. This is found by noticing the 6s placed at (1, 4) and (0, 7). 

If you look at where you can place 3 in box 0, you will find the same results of [(2, 0), (2, 2)], or [A, B]. This is similarly found by noticing the 3s at (0, 8) and (1, 5).

Therefore, either a 6 or 8 **must** be played at both A and B, because A and B are the only slots for both numbers. We do not yet know which square gets which number; however, we do know that no other number can be placed there. This allows us to reach new conclusions, such as the placement of 8. Previously, using row/column elimination and standard logic, 8 could be narrowed down to [(0, 2), (1, 0), (2, 0), (2, 2)]. Now, by elimination A and B from that list, we are left with [(0, 2), (1, 0)]. 

<hr>
