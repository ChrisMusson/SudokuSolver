from mip import BINARY, Model, xsum


class SudokuModel(Model):

    def __init__(self, input: dict[str: list[str]]) -> None:
        super().__init__()
        self.input = input

        # define sol, the solution 3D boolean matrix where correct value is given
        # by the index (+1) where k == 1
        self.sol = [[[self.add_var(var_type=BINARY) for i in range(9)]
                     for j in range(9)] for k in range(9)]

    def add_standard_constraints(self):
        # exactly 1 value per cell
        for i in range(9):
            for j in range(9):
                self += xsum(self.sol[i][j][k] for k in range(9)) == 1

        # numbers 1-9 in each row
        for i in range(9):
            for k in range(9):
                self += xsum(self.sol[i][j][k] for j in range(9)) == 1

        # numbers 1-9 in each column
        for j in range(9):
            for k in range(9):
                self += xsum(self.sol[i][j][k] for i in range(9)) == 1

        # numbers 1-9 in each 3x3 region
        for i2 in range(3):
            for j2 in range(3):
                for k in range(9):
                    self += xsum(self.sol[i][j][k]
                                 for i in range(i2 * 3, i2 * 3 + 3)
                                 for j in range(j2 * 3, j2 * 3 + 3)
                                 ) == 1

    def add_given_constraints(self) -> None:
        for i in range(9):
            for j in range(9):
                char = self.input["givens"][i][j]
                if char != ".":
                    self += self.sol[i][j][int(char) - 1] == 1

    def add_diagonal_constraints(self) -> None:
        # numbers 1-9 in both long diagonals
        if not self.input["diagonal"]:
            return
        for k in range(9):
            self += xsum(self.sol[i][i][k] for i in range(9)) == 1
            self += xsum(self.sol[i][8 - i][k] for i in range(9)) == 1

    def add_anticonsecutive_constraints(self) -> None:
        # no cells containing consecutive digits orthogonally adjacent to each other
        if not self.input["anticonsecutive"]:
            return

        orthog_adjacent = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for i in range(9):
            for j in range(9):
                for adj in orthog_adjacent:
                    # ignore adjacencies where it would go out of bounds
                    if i + adj[0] not in list(range(9)) or j + adj[1] not in list(range(9)):
                        continue
                    for k in range(9):
                        # for cell values (k) in 1-8, the cell value (k+1) in 2-9
                        # can't be in the adjacent cell given by adj
                        if k < 8:
                            self += self.sol[i][j][k] + \
                                self.sol[i + adj[0]][j + adj[1]][k + 1] <= 1

                        # for cell values (k) in 2-9, the cell value (k-1) in 1-8
                        # can't be in the adjacent cell given by adj
                        if k > 0:
                            self += self.sol[i][j][k] + \
                                self.sol[i + adj[0]][j + adj[1]][k - 1] <= 1

    def add_antiking_constraints(self) -> None:
        # no orthogonally or diagonally adjacent cells may contain the same digit
        if not self.input["antiking"]:
            return

        # can ignore orthogonally adjacent cells as they will be ruled out my normal sudoku rules
        diag_adjacent = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for i in range(9):
            for j in range(9):
                # ignore adjacencies where it would go out of bounds
                for move in diag_adjacent:
                    if i + move[0] not in list(range(9)) or j + move[1] not in list(range(9)):
                        continue
                    else:
                        for k in range(9):
                            self += self.sol[i][j][k] + \
                                self.sol[i + move[0]][j + move[1]][k] <= 1

    def add_antiknight_constraints(self) -> None:
        # no cells that are a knight's move away from each other in chess may contain the same digit
        if not self.input["antiknight"]:
            return

        # offsets from a particular cell that denote which cells are a single knight's move away
        knight_adjacent = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                           (1, -2), (1, 2), (2, -1), (2, 1)]
        for i in range(9):
            for j in range(9):
                for move in knight_adjacent:
                    # ignore adjacencies where it would go out of bounds
                    if i + move[0] not in list(range(9)) or j + move[1] not in list(range(9)):
                        continue
                    else:
                        for k in range(9):
                            self += self.sol[i][j][k] + \
                                self.sol[i + move[0]][j + move[1]][k] <= 1

    def add_kropki_constraints(self) -> None:
        kropki = self.input["kropki"]
        if not kropki:
            return

        # all tuples (a, b) where a,b are in 1-9
        all_pairs = [(x+1, y+1) for x in range(9) for y in range(9)]

        # possible pairs of cell values for black dots (quotient of 2)
        poss_b = [(i+1, j+1) for i in range(9)
                  for j in range(9) if (i+1)/(j+1) == 2 or (j+1)/(i+1) == 2]
        # possible pairs of cell values for white dots (difference of 1)
        poss_w = [(i+1, j+1) for i in range(9)
                  for j in range(9) if abs(i-j) == 1]

        for rule in kropki:
            # rule must always be 4 digits + b/w, as dictated by InputParser
            cell1 = self.sol[int(rule[0]) - 1][int(rule[1]) - 1]
            cell2 = self.sol[int(rule[2]) - 1][int(rule[3]) - 1]
            colour = rule[4]

            if colour == "w":
                for pair in set(all_pairs) - set(poss_w):
                    self += cell1[pair[0] - 1] + cell2[pair[1] - 1] <= 1

            if colour == "b":
                for pair in set(all_pairs) - set(poss_b):
                    self += cell1[pair[0] - 1] + cell2[pair[1] - 1] <= 1

    def add_neg_kropki_constraints(self) -> None:
        neg_kropki = self.input["neg_kropki"]
        if not neg_kropki:
            return

        # need to find all intersections without any kropki dot
        kropki_intersections = [((int(x[0]), int(x[1])), (int(x[2]), int(x[3])))
                                for x in self.input["kropki"]]

        all_intersections = [((i, j), (i+1, j)) for i in range(1, 9) for j in range(
            1, 10)] + [((i, j), (i, j+1)) for i in range(1, 10) for j in range(1, 9)]

        bare_intersections = set(all_intersections) - set(kropki_intersections)

        # possible pairs of cell values for black dots (quotient of 2)
        poss_b = [(i+1, j+1) for i in range(9)
                  for j in range(9) if (i+1)/(j+1) == 2 or (j+1)/(i+1) == 2]
        # possible pairs of cell values for white dots (difference of 1)
        poss_w = [(i+1, j+1) for i in range(9)
                  for j in range(9) if abs(i-j) == 1]

        for inter in bare_intersections:
            cell1 = self.sol[inter[0][0] - 1][inter[0][1] - 1]
            cell2 = self.sol[inter[1][0] - 1][inter[1][1] - 1]
            for poss in poss_b + poss_w:
                # in the valid pairs for black+white kropki dots, a maximum of
                # 1 of the values must be true in the intersection
                self += cell1[poss[0] - 1] + cell2[poss[1] - 1] <= 1

    def add_thermo_constraints(self) -> None:
        thermo = self.input["thermo"]
        if not thermo:
            return

        # all tuples (a, b) where a,b are in 1-9
        all_pairs = set([(x+1, y+1) for x in range(9) for y in range(9)])

        # all tuples where the 2nd element is larger than the 1st
        # can use this as thermo clues are given in increasing order
        valid_pairs = set([(i, i+j) for i in range(1, 10)
                          for j in range(1, 10-i)])

        for clue in thermo:
            cells = [(int(clue[2*i]), int(clue[2*i+1]))
                     for i in range(len(clue) // 2)]

            for i in range(len(cells) - 1):
                cell1 = self.sol[cells[i][0] - 1][cells[i][1] - 1]
                cell2 = self.sol[cells[i + 1][0] - 1][cells[i + 1][1] - 1]
                # iterate over invalid pairs for consecutive, increasing cells in a thermo
                # only a maximum of one of the values in these pairs may correspond to the true value
                for pair in all_pairs - valid_pairs:
                    self += cell1[pair[0] - 1] + cell2[pair[1] - 1] <= 1

    def add_constraints(self):
        self.add_standard_constraints()
        self.add_given_constraints()
        self.add_kropki_constraints()
        self.add_thermo_constraints()
        self.add_diagonal_constraints()
        self.add_anticonsecutive_constraints()
        self.add_antiking_constraints()
        self.add_antiknight_constraints()
        self.add_neg_kropki_constraints()
