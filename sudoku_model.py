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

    def add_arrow_constraints(self) -> None:
        arrow = self.input["arrow"]
        if not arrow:
            return

        for clue in arrow:
            circle = (int(clue[0]), int(clue[1]))
            others = [(int(clue[2*i]), int(clue[2*i+1]))
                      for i in range(1, len(clue[2:-1]) // 2 + 1)]

            # sum of all digits in others equals digit in circle
            self += xsum(xsum((k + 1) * self.sol[x[0] - 1][x[1] - 1][k] for x in others) for k in range(
                9)) == xsum((k+1) * self.sol[circle[0] - 1][circle[1] - 1][k] for k in range(9))

    def add_entropic_constraints(self) -> None:
        entropic = self.input["entropic"]
        if not entropic:
            return
        for clue in entropic:
            clue = clue[:-3]
            cells = [(int(clue[2*i]), int(clue[2*i+1]))
                     for i in range(len(clue) // 2)]
            for i in range(len(cells) - 2):
                cell1 = self.sol[cells[i][0] - 1][cells[i][1] - 1]
                cell2 = self.sol[cells[i + 1][0] - 1][cells[i + 1][1] - 1]
                cell3 = self.sol[cells[i + 2][0] - 1][cells[i + 2][1] - 1]

                self += xsum(x[k] for k in [0, 1, 2]
                             for x in [cell1, cell2, cell3]) == 1

                self += xsum(x[k] for k in [3, 4, 5]
                             for x in [cell1, cell2, cell3]) == 1

                self += xsum(x[k] for k in [6, 7, 8]
                             for x in [cell1, cell2, cell3]) == 1
                # xsum(cell2[k] for k in [0, 1, 2]) + \
                # xsum(cell3[k] for k in [0, 1, 2]) == 1

    def add_even_odd_constraints(self) -> None:
        even_odd = self.input["even_odd"]
        if not even_odd:
            return
        for clue in even_odd:
            cells, oe = [(int(clue[2*i]), int(clue[2*i+1]))
                         for i in range(len(clue) // 2)], clue[-1]

            if oe == "e":
                for cell in cells:
                    sol_cell = self.sol[cell[0]-1][cell[1]-1]
                    # index 1,3,5,7 == value 2,4,6,8
                    self += xsum(sol_cell[k] for k in [1, 3, 5, 7]) == 1
            if oe == "o":
                for cell in cells:
                    sol_cell = self.sol[cell[0]-1][cell[1]-1]
                    # index 0,2,4,6,8 == value 1,3,5,7,9
                    self += xsum(sol_cell[k] for k in [0, 2, 4, 6, 8]) == 1

    def add_extra_regions_constraints(self) -> None:
        extra_regions = self.input["extra_regions"]
        if not extra_regions:
            return

        for region in extra_regions:
            region_cells = [(int(region[2*i]), int(region[2*i+1]))
                            for i in range((len(region) - 2) // 2)]

            for k in range(9):
                self += xsum(self.sol[x[0] - 1][x[1] - 1][k]
                             for x in region_cells) == 1

    def add_german_whispers_constraints(self) -> None:
        german_whispers = self.input["german_whispers"]
        if not german_whispers:
            return

        all_pairs = [(x+1, y+1) for x in range(9) for y in range(9)]

        valid_pairs = [(x+1, y+1) for x in range(9)
                       for y in range(9) if abs(x-y) >= 5]

        for clue in german_whispers:
            cells = [(int(clue[2*i]), int(clue[2*i+1]))
                     for i in range((len(clue) - 2) // 2)]
            # take off 1 because looking ahead along the german whisper line
            for i in range(len(cells) - 1):
                cell1 = self.sol[cells[i][0] - 1][cells[i][1] - 1]
                cell2 = self.sol[cells[i + 1][0] - 1][cells[i + 1][1] - 1]

                # iterate through invalid pairs for a german whisper
                # only a maximum of one of the values in these pairs may correspond to the true value
                for pair in set(all_pairs) - set(valid_pairs):
                    self += cell1[pair[0] - 1] + cell2[pair[1] - 1] <= 1

    def add_killer_constraints(self) -> None:
        killer = self.input["killer"]
        if not killer:
            return

        for clue in killer:
            region, s = clue.split("k")
            region_cells = [(int(region[2*i]), int(region[2*i+1]))
                            for i in range(len(region) // 2)]

            # digits cannot repeat in region cells
            for k in range(9):
                self += xsum(self.sol[x[0] - 1][x[1] - 1][k]
                             for x in region_cells) <= 1

            # if a sum is given, ensure region cells add to that sum. Otherwise, continue
            if int(s) != 0:
                self += xsum(xsum((k + 1) * self.sol[x[0] - 1][x[1] - 1][k]
                             for x in region_cells) for k in range(9)) == int(s)

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

    def add_modular_lines_constraints(self) -> None:
        modular_lines = self.input["modular_lines"]
        if not modular_lines:
            return
        for clue in modular_lines:
            clue = clue[:-2]
            cells = [(int(clue[2*i]), int(clue[2*i+1]))
                     for i in range(len(clue) // 2)]

            if len(cells) == 2:
                cell1 = self.sol[cells[i][0] - 1][cells[i][1] - 1]
                cell2 = self.sol[cells[i + 1][0] - 1][cells[i + 1][1] - 1]

                self += xsum(x[k] for k in [0, 3, 6]
                             for x in [cell1, cell2]) <= 1

                self += xsum(x[k] for k in [1, 4, 7]
                             for x in [cell1, cell2]) <= 1

                self += xsum(x[k] for k in [2, 5, 8]
                             for x in [cell1, cell2]) <= 1

            else:
                for i in range(len(cells) - 2):
                    cell1 = self.sol[cells[i][0] - 1][cells[i][1] - 1]
                    cell2 = self.sol[cells[i + 1][0] - 1][cells[i + 1][1] - 1]
                    cell3 = self.sol[cells[i + 2][0] - 1][cells[i + 2][1] - 1]

                    self += xsum(x[k] for k in [0, 3, 6]
                                 for x in [cell1, cell2, cell3]) == 1

                    self += xsum(x[k] for k in [1, 4, 7]
                                 for x in [cell1, cell2, cell3]) == 1

                    self += xsum(x[k] for k in [2, 5, 8]
                                 for x in [cell1, cell2, cell3]) == 1

    def add_palindrome_constraints(self) -> None:
        palindrome = self.input["palindrome"]
        if not palindrome:
            return
        for clue in palindrome:
            cells = [(int(clue[2*i]), int(clue[2*i+1]))
                     for i in range(len(clue) // 2)]
            for i in range(len(cells) // 2):
                # take the ith and (n-i)th cells from the list of cells
                cell1 = self.sol[cells[i][0] - 1][cells[i][1] - 1]
                cell2 = self.sol[cells[-i-1][0] - 1][cells[-i-1][1] - 1]
                # set them equal to each other
                for k in range(9):
                    self += cell1[k] == cell2[k]

    def add_quadruple_constraints(self) -> None:
        quadruple = self.input["quadruple"]
        if not quadruple:
            return

        for q in quadruple:
            row = int(q[0])
            col = int(q[1])
            cells = [(row, col), (row, col + 1),
                     (row + 1, col), (row + 1, col + 1)]
            digits = [int(x) for x in q[2:-1]]
            for d in set(digits):
                self += xsum(self.sol[x[0] - 1][x[1] - 1][d - 1]
                             for x in cells) == digits.count(d)

    def add_region_sum_line_constraints(self) -> None:
        region_sum_line = self.input["region_sum_lines"]
        if not region_sum_line:
            return

        for clue in region_sum_line:
            cells = [(int(clue[2*i]), int(clue[2*i+1]))
                     for i in range((len(clue) - 3) // 2)]

            # separate groups of cells into each distinct region
            separated = [[cells[0]]]
            for i in range(len(cells) - 1):
                c1 = cells[i]
                c2 = cells[i + 1]

                # check c1 and c2 are in the same 3x3 region
                if (c1[0] - 1) // 3 == (c2[0] - 1) // 3 and (c1[1] - 1) // 3 == (c2[1] - 1) // 3:
                    separated[-1].append(c2)
                else:
                    separated.append([c2])

            # set all regions to have the same sum
            # this turns out faster than just setting the sum of region1 to be equal to region 2, 2 to 3, etc.
            for a in separated:
                for b in separated:
                    if a != b:
                        sum_a = xsum(xsum(
                            (k + 1) * self.sol[x[0] - 1][x[1] - 1][k] for k in range(9)) for x in a)

                        sum_b = xsum(xsum((k + 1) * self.sol[x[0] - 1][x[1] - 1][k]
                                          for k in range(9)) for x in b)

                        self += sum_a == sum_b

    def add_renban_constraints(self) -> None:
        renban = self.input["renban"]
        if not renban:
            return

        for clue in renban:
            cells = [(int(clue[2*i]), int(clue[2*i+1]))
                     for i in range(len(clue) // 2)]

            # ensure that all pairs of cells in the renban group
            # have a maximum difference of num cells - 1
            for c1 in cells:
                for c2 in cells:
                    v1 = xsum(
                        (k + 1) * self.sol[c1[0] - 1][c1[1] - 1][k] for k in range(9))
                    v2 = xsum(
                        (k + 1) * self.sol[c2[0] - 1][c2[1] - 1][k] for k in range(9))
                    self += v1 - v2 <= len(cells) - 1
                    self += v2 - v1 <= len(cells) - 1

            # ensure that no digit is repeated in the renban group
            for k in range(9):
                self += xsum(self.sol[c[0] - 1][c[1] - 1][k]
                             for c in cells) <= 1

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

    def add_xv_constraints(self) -> None:
        xv = self.input["xv"]
        if not xv:
            return
        all_pairs = [(x+1, y+1) for x in range(9) for y in range(9)]
        poss_v = [(i+1, j+1) for i in range(9)
                  for j in range(9) if i + j + 2 == 5]
        poss_x = [(i+1, j+1) for i in range(9)
                  for j in range(9) if i + j + 2 == 10]

        for rule in xv:
            # rule must always be 4 digits + b/w, as dictated by InputParser
            cell1 = self.sol[int(rule[0]) - 1][int(rule[1]) - 1]
            cell2 = self.sol[int(rule[2]) - 1][int(rule[3]) - 1]
            colour = rule[4]

            if colour == "v":
                for pair in set(all_pairs) - set(poss_v):
                    self += cell1[pair[0] - 1] + cell2[pair[1] - 1] <= 1

            if colour == "x":
                for pair in set(all_pairs) - set(poss_x):
                    self += cell1[pair[0] - 1] + cell2[pair[1] - 1] <= 1

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

    def add_diagonal_constraints(self) -> None:
        # numbers 1-9 in both long diagonals
        if not self.input["diagonal"]:
            return
        for k in range(9):
            self += xsum(self.sol[i][i][k] for i in range(9)) == 1
            self += xsum(self.sol[i][8 - i][k] for i in range(9)) == 1

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

    def add_neg_xv_constraints(self) -> None:
        neg_xv = self.input["neg_xv"]
        if not neg_xv:
            return

        # need to find all intersections without any X or V
        xv_intersections = [((int(x[0]), int(x[1])), (int(x[2]), int(x[3])))
                            for x in self.input["xv"]]

        all_intersections = [((i, j), (i+1, j)) for i in range(1, 9) for j in range(
            1, 10)] + [((i, j), (i, j+1)) for i in range(1, 10) for j in range(1, 9)]

        bare_intersections = set(all_intersections) - set(xv_intersections)

        # possible pairs of cell values for V
        poss_v = [(i+1, j+1) for i in range(9)
                  for j in range(9) if i + j + 2 == 5]
        # possible pairs of cell values for X
        poss_x = [(i+1, j+1) for i in range(9)
                  for j in range(9) if i + j + 2 == 10]

        for inter in bare_intersections:
            cell1 = self.sol[inter[0][0] - 1][inter[0][1] - 1]
            cell2 = self.sol[inter[1][0] - 1][inter[1][1] - 1]
            for poss in poss_v + poss_x:
                # in the valid pairs for V + X, a maximum of
                # 1 of the values must be true in the intersection
                self += cell1[poss[0] - 1] + cell2[poss[1] - 1] <= 1

    def add_constraints(self):
        self.add_standard_constraints()
        self.add_given_constraints()
        self.add_arrow_constraints()
        self.add_entropic_constraints()
        self.add_even_odd_constraints()
        self.add_extra_regions_constraints()
        self.add_german_whispers_constraints()
        self.add_killer_constraints()
        self.add_kropki_constraints()
        self.add_modular_lines_constraints()
        self.add_palindrome_constraints()
        self.add_quadruple_constraints()
        self.add_region_sum_line_constraints()
        self.add_renban_constraints()
        self.add_thermo_constraints()
        self.add_xv_constraints()

        self.add_anticonsecutive_constraints()
        self.add_antiking_constraints()
        self.add_antiknight_constraints()
        self.add_diagonal_constraints()
        self.add_neg_kropki_constraints()
        self.add_neg_xv_constraints()
