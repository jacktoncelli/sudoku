# sudoku
An AI to solve sudoku puzzles

----------------

### Intro January 23, 2023

I undertook this as a personal project for fun. I don't have very much experience building AIs, but I thought sudoku would be a simple enough example that I could handle it. I also wanted to try out a bigger project with Python, as I use primarily Java for other personal projects. 

At the moment, my AI can solve easy or medium ranked puzzles(the scale coming from a sudoku book I have), but when it comes to hard or expert puzzles, it hits a roadblock. The code is functional with the caveat that it isn't realistic on your average computer. 

My algorithm isn't able to make enough conclusions using the information availible, so it is forced to make guesses, which pulls it into the rabbit hole of sudoku's 6 sextillion possible boards. Put briefly, when unable to make a guarenteed move, the program will test out a number at a position to see if the puzzle can be solved with that position. This test only leads to more positions where it cannot make a definite conclusion, and so it guesses again, ad infinitem until it either breaks the rules of sudoku or finds a solution. Logically, this approach guarentees success, but you would probably need a quantum computer or portion of America's defense budget to support the memory usage. My laptop doesn't even scratch the surface. Of course, my algorithm is only making educated guesses, but even if it narrows the combinations down to a few quadrillion, thats not much better. 

To reduce the need of these educated guesses, I plan to implement logical inferences based on the possible positions of numbers on the board. Here is an example of where I want my computer to be able to make an inference:

Note: 0 represents an empty square

```md
 Y  Y  Y   0  0  0   0  D  0
 2  3  1   0  0  0   0  X  0
 0  0  0   0  5  0   0  0  0 


 0  0  0   0  0  0   0  0  5
 0  0  0   0  0  0   0  0  0
 0  0  0   0  0  0   0  0  0


 0  0  0   0  0  0   5  0  0
 0  0  0   0  0  0   0  0  0
 0  0  0   0  0  0   0  0  0
```
Now, as this is a mostly empty board, there are tons of possible solutions to this, but I want to focus on the inference possible in finding where the 5 goes in box 3, or the top right box. By observing the other 5s on the board, my AI can conclude that a 5 can either be placed at X or D. You can make the inference that in box 1 (the top left box), 5 must be placed in the top row as it cannot be in the bottom or middle rows. Therefore, it can be concluded with absolute certainty that the 5 is placed at X.

I have not decided how I am going to implement this yet, but I believe that this logic will largely eliminate the need for my systematic guessing system as it is. Even if it is still required for harder problems, it's combinations should be greatly reduced and the algorithm may be realistic to run on an average computer.

My goal is to eliminate the need to guess altogether by building up the logic. No person playing sudoku makes guesses -- they just figure it out. I am absolutely open to suggestions on improving my working code or implementing the new logic - please reach out with any ideas!


------------------------

### Update January 24, 2023

I have implemented the above described logic. The AI now is capable of reaching conclusions given information such as the board above. However, it still gets stuck sometimes and is forced to guess. The guess is also more likely to succeed, because conclusions are drawn much more reliably. At the board below, the AI had to guess, but was able to find a solution fairly quickly. Here is an example:

```md
    7  0  4     9  0  0     6  0  8 
    0  0  9     8  0  0     0  3  0 
    0  0  6     2  7  0     0  9  0 


    9  0  0     5  0  8     0  0  2 
    C  6  0     0  2  9     0  5  3 
    4  A  B     0  0  7     0  0  9 


    0  7  0     0  8  0     9  0  0 
    0  4  0     0  9  2     3  8  0 
    6  9  8     0  0  5     0  0  1 

```

The AI has filled in several squares (10 to be exact), but cannot reach a definite conclusion in this situation. If I had to solve this puzzle, I would (hopefully) notice squares A and B. In box 4 (left middle box), there obviously needs to be a 2 and a 5. Both 2 and 5 can ONLY go in either A or B. This means that no OTHER number can go in A or B, allowing you to make conclusions, including that an 8 is played at C. 

This is the next step I want to take to make my AI smarter. I expect this to be a significant challenge, but I have some ideas on how to implement this. Like always, feel free to suggest improvements to my current code or ideas for my next challenge. 

--------------------------
