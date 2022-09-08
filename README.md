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

## How to Use
You can see some valid examples of puzzles in the `puzzles/` folder. They all conform to the following rules

### General Instructions

1. All puzzles must have a 9x9 grid made of dots and digits, where dots are unknowns and digits are the given digits.

1. For constraints that are either True or False (diagonal, anticonsecutive, antiking, antiknight, negative Kropki), add a line to the puzzle file with the constraint name and true, e.g. - `anticonsecutive: true`. If nothing is written about a rule, it is set to False.

1. When giving co-ordinates (i, j) for certain constraints, note that they are indexed from 1, with i denoting the row and j denoting the column, and that (1, 1) is the upper leftmost cell of the grid. For clarity, the cell below (1, 1) is (2, 1), while the cell to the right of (1, 1) is (1, 2).

### Variant-Specific Instructions
1. In Kropki puzzles, you need to enter a line to your puzzle file for every dot. For each Kropki dot, enter the two cells that the Kropki dot is between, followed by either B (black) or W (white). For example, a black Kropki dot between the top left cell and the cell to its right would be `1112B`.

1. In Thermo puzzles, you need to enter a line to your puzzle file for every thermometer. You do this by entering all cells that are on the thermometer starting from the bulb end, followed by a T. For example, a C-shaped thermometer of length 4 starting in the central cell would read `55546465T`.

## To add

- XV (with negative XV constraint)
- Killer
- Arrow
- Odd/Even
- Palindrome
- Fortress

### Possible Future Additions:

- German Whispers
- Renban
- X-Sums
- Windoku
- Argyle
- Battenburg
- More...