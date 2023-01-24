# sudoku
An AI to solve sudoku puzzles

----------------

I undertook this as a personal project for fun. I don't have very much experience building AIs, but I thought sudoku would be a simple enough example that I could handle it. I also wanted to try out a bigger project with Python, as I use primarily Java for other personal projects. 

At the moment, my AI can solve easy or medium ranked puzzles(the scale coming from a sudoku book I have), but when it comes to hard or expert puzzles, it hits a roadblock. The code is functional with the caveat that it isn't realistic on your average computer. My algorithm isn't able to make enough conclusions using the information availible, so it is forced to make guesses, which pulls it into the rabbit hole of sudoku's 6 sextillion possible boards. Put briefly, the program will test out a number at a position to see if the puzzle can be solved with that position. This test only leads to more positions where it cannot make a definite conclusion, and so it guesses again, ad infinitem(figuratively -- mathematically this approach guarentees success but you would probably need a quantum computer or portion of America's defense budget to support the memory usage. My laptop doesn't even scratch the surface). Of course, my algorithm is only making educated guesses, but even if it narrows the combinations down to a few quadrillion, thats not much better. 

------------------------

To reduce the need of these educated guesses, I plan to implement logical inferences based on the possible positions of numbers on the board. Here is an example of where I want my computer to be able to make an inference:

Note: 0 represents an empty square

```md
Y Y Y  0 0 0  0 D 0
2 3 1  0 0 0  0 X 0
0 0 0  0 5 0  0 0 0


0 0 0  0 0 0  0 0 5
0 0 0  0 0 0  0 0 0
0 0 0  0 0 0  0 0 0


0 0 0  0 0 0  5 0 0
0 0 0  0 0 0  0 0 0
0 0 0  0 0 0  0 0 0
```
Now, as this is a mostly empty board, there are tons of possible solutions to this, but I want to focus on the inference possible in finding where the 5 goes in box 3, or the top right box. By observing the other 5s on the board, my AI can conclude that a 5 can either be placed at X or D. You can make the inference that in box 1 (the top left box), 5 must be placed in the top row as it cannot be in the bottom or middle rows. Therefore, it can be concluded with absolute certainty that the 5 is placed at X.

I have not decided how I am going to implement this yet, but I believe that this logic will largely eliminate the need for my systematic guessing system as it is. Even if it is still required for harder problems, it's combinations should be greatly reduced and the algorithm may be realistic to run on an average computer.

My goal is to eliminate the need to guess altogether by building up the logic. No person playing sudoku guesses -- they just figure it out. You can certainly try to guess to solve a sudoku puzzles, but good luck being faster than a computer. 

If anyone has suggestions on how to implement the above described logic, feel free to reach out or comment on the post. I am very open to ideas and improvement, and I desperately need to make this algorithm more efficient. 

------------------------
