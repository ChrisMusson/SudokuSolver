import json

from input_parser import InputParser
from solver import Solver
from sudoku_model import SudokuModel

FILEPATH = "puzzles/classic.txt"
parser = InputParser(FILEPATH)
model = SudokuModel(parser.parse())
model.add_constraints()

# Useful for checking you have inputted the puzzle correctly
print(json.dumps(model.input, indent=2))

solver = Solver(model)
solution = solver.solve()

solution_string = ""
for i in range(9):
    for j in range(9):
        for k in range(9):
            if solution[i][j][k].x == 1:
                solution_string += str(k + 1)
                break

print("\n== SOLUTION ==\n")
for i in range(9):
    print(solution_string[i*9: (i+1)*9])
