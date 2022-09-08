class Solver:

    def __init__(self, model) -> None:
        self.model = model
        self.model.verbose = False

    def solve(self) -> None:
        self.model.optimize()
        return self.model.sol
