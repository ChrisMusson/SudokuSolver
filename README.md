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

## How to Use
You can see some valid examples of puzzles in the `puzzles/` folder. They all conform to the following rules

### General Instructions

1. All puzzles must have a 9x9 grid made of dots and digits, where dots are unknowns and digits are the given digits.

1. For constraints that are either True or False (diagonal, anticonsecutive, antiking, antiknight, negative Kropki), add a line to the puzzle file with the constraint name and true, e.g. - `anticonsecutive: true`. If nothing is written about a rule, it is set to False.

1. When giving co-ordinates (i, j) for certain constraints, note that they are indexed from 1, with i denoting the row and j denoting the column, and that (1, 1) is the upper leftmost cell of the grid. For clarity, the cell below (1, 1) is (2, 1), while the cell to the right of (1, 1) is (1, 2).

### Variant-Specific Instructions
1. In Kropki puzzles, you need to enter a line to your puzzle file for every dot. For each Kropki dot, enter the two cells that the Kropki dot is between, followed by either B (black) or W (white). For example, a black Kropki dot between the top left cell and the cell to its right would be `1112B`.

1. In Thermo puzzles, you need to enter a line to your puzzle file for every thermometer. You do this by entering all cells that are on the thermometer starting from the bulb end, followed by a T. For example, a C-shaped thermometer of length 4 starting in the central cell would read `55546465T`. If multiple thermometers start at the same bulb, then enter them seperately.

1. In Killer puzzles, you need to enter a line to your puzzle file for every region. You do this by entering all cells that are in a region, followed by a K, followed by their sum. If the sum is not given, set the sum to 0. For example, an L-shaped region of size 5 in the central 3x3 box that sums to 26 would read `4454646566K26`.

1. In Arrow puzzles, you need to enter a line to your puzzle file for every arrow. You do this by entering the circled cell, followed by all cells on the adjoining arrow, followed by an A. For example, a 3-cell L-shaped arrow that has the central cell as it's circle would read `55657576A`.

1. In Palindrome puzzles, you need to enter a line to your puzzle file for every palindrome line. You do this by entering the cells on the line, starting from one end a traversing it to the other end, followed by a P. For example, a 5-cell staircase palindrome line could read `6667777888P`.

## To add

- XV (with negative XV constraint)
- Odd/Even
- Fortress

### Possible Future Additions:

- German Whispers
- Renban
- X-Sums
- Windoku
- Argyle
- Battenburg
- More...