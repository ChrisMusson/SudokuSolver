import re


class InputParser:

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def read_file(self) -> list[str]:
        with open(self.filename, "r") as f:
            # strip whitespace from lines and remove any line that is only whitespace
            return list(filter(None, [x.strip().lower() for x in f.readlines()]))

    def parse_givens(self, input: list[str]) -> list[str]:
        pattern = re.compile("^[\d\.]{9}$")
        valid = list(filter(pattern.match, input))
        if len(valid) != 9:
            raise ValueError(
                f"There are not exactly 9 valid rows in {self.filename}")
        return valid

    def is_diagonal(self, input: list[str]) -> bool:
        pattern = re.compile("diagonal:?.*true")
        valid = list(filter(pattern.match, input))
        return len(valid) > 0

    def is_anticonsecutive(self, input: list[str]) -> bool:
        pattern = re.compile("anti-?consecutive:?.*true")
        valid = list(filter(pattern.match, input))
        return len(valid) > 0

    def is_antiking(self, input: list[str]) -> bool:
        pattern = re.compile("anti-?king:?.*true")
        valid = list(filter(pattern.match, input))
        return len(valid) > 0

    def is_antiknight(self, input: list[str]) -> bool:
        pattern = re.compile("anti-?knight:?.*true")
        valid = list(filter(pattern.match, input))
        return len(valid) > 0

    def parse_kropki(self, input: list[str]) -> list[str]:
        pattern = re.compile("\d{4}[bw]")
        return list(filter(pattern.match, input))

    def is_negative_kropki(self, input: list[str]) -> bool:
        pattern = re.compile("neg(ative)?-?\s?_kropki:?.*true")
        valid = list(filter(pattern.match, input))
        return len(valid) > 0

    def parse_thermo(self, input: list[str]) -> list[str]:
        pattern = re.compile("\d{4,}t")
        return list(filter(pattern.match, input))

    def parse(self) -> dict[str, list[str] | bool]:
        parsed_puzzle = {}
        input = self.read_file()

        parsed_puzzle["givens"] = self.parse_givens(input)
        parsed_puzzle["kropki"] = self.parse_kropki(input)
        parsed_puzzle["thermo"] = self.parse_thermo(input)
        parsed_puzzle["diagonal"] = self.is_diagonal(input)
        parsed_puzzle["anticonsecutive"] = self.is_anticonsecutive(input)
        parsed_puzzle["antiking"] = self.is_antiking(input)
        parsed_puzzle["antiknight"] = self.is_antiknight(input)
        parsed_puzzle["neg_kropki"] = self.is_negative_kropki(input)

        return parsed_puzzle
