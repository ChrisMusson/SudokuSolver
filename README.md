# Sudoku Solver

A CLI program to solve 9x9 Sudoku and its common variants. Note that it is currently a work in progress and is likely to change in the future

## Currently Supported

- Classic

- Diagonal - the two long diagonals must also contain the digits 1-9

- Anti-king - any two cells seperated by a king's move in chess must not 
contain the same digit

- Anti-knight - any two cells seperated by a knight's move in chess must not contain the same digit

- Anti-consecutive - any two orthogonally adjacent cells must not contain digits with a difference of 1

- Kropki - cells seperated by a black dot must be in a ratio of 1:2, while cells seperated by a white dot must have a difference of 1

  - Negative Kropki - cells without a dot between them must neither be in a 1:2 ratio, nor have a difference of 1

- Thermo - cells on thermometers must increase in value, starting from the 'bulb' end

- Killer - cells in marked regions must not contain repeated digits, and must sum to the total given

- Arrow - digits placed in circled cells must be the sum of the cells on the adjoining arrows

- Palindrome - cells on marked lines must read the same from both directions

- Even/Odd - cells marked with a circle must be odd, cells marked with a square must be even

- German Whispers - adjacent cells on a marked line must differ by at least 5

- Entropic - each set of 3 consecutive cells on marked lines must contain one low digit (1, 2, 3), one medium digit (4, 5, 6), and one high digit (7, 8, 9).

- XV - cells seperated by an X must sum to 10, while cells seperated by a V must sum to 5.

  - Negative XV - cells without an X or V between them must sum to neither 10 nor 5.

- Renban - cells in marked regions must contain consecutive, non-repeating digits in any order.

- Extra Regions - cells in marked regions must contain the digits 1-9 exactly once.

- Quadruple - cells surrounding a clue must contain the given digits in that clue.

- Region Sum Lines - digits on region sum lines have an equal sum N within each box it passes through. If a line passes through the same box more than once, each individual segment of such a line within that box sums to N separately. 

## How to Use
Every variant described here has a valid example of a puzzle in the `puzzles/` folder.

### General Instructions

1. All puzzles must have a 9x9 grid made of dots and digits, where dots are unknowns and digits are the given digits.

1. For constraints that are either True or False (diagonal, anticonsecutive, antiking, antiknight, negative Kropki), add a line to the puzzle file with the constraint name and true, e.g. - `anticonsecutive: true`. If nothing is written about a rule, it is set to False.

1. When giving co-ordinates (i, j) for certain constraints, note that they are indexed from 1, with i denoting the row and j denoting the column, and that (1, 1) is the upper leftmost cell of the grid. For clarity, the cell below (1, 1) is (2, 1), while the cell to the right of (1, 1) is (1, 2).

### Variant-Specific Instructions
1. In Kropki puzzles, you need to enter a line to your puzzle file for every dot. For each Kropki dot, enter the two cells that the Kropki dot is between, followed by either B (black) or W (white). For example, a black Kropki dot between the top left cell and the cell to its right would be `1112B`.

1. In Thermo puzzles, you need to enter a line to your puzzle file for every thermometer. You do this by entering all cells that are on the thermometer starting from the bulb end, followed by a T. For example, a C-shaped thermometer of length 4 starting in the central cell would read `55546465T`. If multiple thermometers start at the same bulb, then enter them seperately.

1. In Killer puzzles, you need to enter a line to your puzzle file for every region. You do this by entering all cells that are in a region, followed by a K, followed by their sum. If the sum is not given, set the sum to 0. For example, an L-shaped region of size 5 in the central 3x3 box that sums to 26 would read `4454646566K26`.

1. In Arrow puzzles, you need to enter a line to your puzzle file for every arrow. You do this by entering the circled cell, followed by all cells on the adjoining arrow, followed by an A. For example, a 3-cell L-shaped arrow that has the central cell as it's circle would read `55657576A`.

1. In Palindrome puzzles, you need to enter a line to your puzzle file for every palindrome line. You do this by entering the cells on the line, starting from one end and traversing it to the other end, followed by a P. For example, a 5-cell staircase palindrome line could read `6667777888P`.

1. In Even/Odd puzzles, you need to enter up to 2 lines to your puzzle file - one line for all even cells, followed by an E, and one line for all odd cells, followed by an O. For example, if the antidiagonal/trailing diagonal of the grid contains alternating odds and evens, the lines to add would read `9173553719O` and `82644628E`.

1. In German Whispers puzzles, you need to enter a line to your puzzle file for every German whispers line. You do this by entering the cells on the line, starting from one end and traversing it to the other end, followed by GW. For example, a 10-cell P-shaped German whispers line could read `67685848474656667686GW`.

1. In Entropic puzzles, you need to enter a line to your puzzle file for every entropic line. You do this by entering the cells on the line, starting from one end and traversing it to the other end, followed by ENT. If the entropic line forms a closed loop, then you may start anywhere on the loop, but you must add the first two cells to the end of the line before ENT. For example, an 8-cell O-shaped loop in the top-left 3x3 box could read `11121323333231211112ENT`.

1. In XV puzzles, you need to enter a line to your puzzle file for every X or V in the puzzle. For each X or V, enter the two cells that the X or V is between, followed by either X or V. For example, an X between the bottom left cell and the cell to its right would read `9192X`.

1. In Renban puzzles, you need to enter a line to your puzzle file for every renban region. You do this by entering the cells in the region, followed by an R. For example, a renban region containing the central 5 cells of row 7 would read `7374757677R`.

1. In Extra Regions puzzles, you need to enter a line to your puzzle file for every extra region. You do this by entering the cells in the region, followed by ER. For example, an L-shaped extra region starting at (4, 2) and ending at (8, 6) would read `4252627282838485ER`.

1. In Quadruple puzzles, you need to enter a line to your puzzle file for every quadruple clue. You do this by entering the top left cell surrounding the quadruple clue, followed by the given digits, followed by Q. For example, a clue whose top left cell is (6, 3) and contains the digits 1224 would read `631223Q`.

1. In Region Sum Lines puzzles, you need to enter a line to your puzzle file for every region sum line. You do this by entering the cells on the line, starting from one end and traversing it to the other end, followed by RSL. For example, an S-shaped region sum line could read `141323243433RSL`.

## To add

- Fortress

### Possible Future Additions:

- X-Sums
- Windoku
- Argyle
- Battenburg
- More...