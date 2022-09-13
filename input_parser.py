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

    def parse_arrow(self, input: list[str]) -> list[str]:
        pattern = re.compile("^\d{4,}a$")
        return list(filter(pattern.match, input))

    def parse_entropic(self, input: list[str]) -> list[str]:
        pattern = re.compile("^\d{4,}ent$")
        return list(filter(pattern.match, input))

    def parse_even_odd(self, input: list[str]) -> list[str]:
        pattern = re.compile("^\d{2,}[oe]$")
        return list(filter(pattern.match, input))

    def parse_extra_regions(self, input: list[str]) -> list[str]:
        pattern = re.compile("^\d{2,}er$")
        return list(filter(pattern.match, input))

    def parse_german_whispers(self, input: list[str]) -> list[str]:
        pattern = re.compile("^\d{4,}gw$")
        return list(filter(pattern.match, input))

    def parse_killer(self, input: list[str]) -> list[str]:
        pattern = re.compile("^\d{2,}k\d{1,3}$")
        return list(filter(pattern.match, input))

    def parse_kropki(self, input: list[str]) -> list[str]:
        pattern = re.compile("^\d{4}[bw]$")
        return list(filter(pattern.match, input))

    def parse_palindrome(self, input: list[str]) -> list[str]:
        pattern = re.compile("^\d{4,}p$")
        return list(filter(pattern.match, input))

    def parse_quadruple(self, input: list[str]) -> list[str]:
        pattern = re.compile("^\d{4,}q$")
        return list(filter(pattern.match, input))

    def parse_renban(self, input: list[str]) -> list[str]:
        pattern = re.compile("^\d{4,}r$")
        return list(filter(pattern.match, input))

    def parse_thermo(self, input: list[str]) -> list[str]:
        pattern = re.compile("^\d{4,}t$")
        return list(filter(pattern.match, input))

    def parse_xv(self, input: list[str]) -> list[str]:
        pattern = re.compile("^\d{4}[xv]$")
        return list(filter(pattern.match, input))

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

    def is_diagonal(self, input: list[str]) -> bool:
        pattern = re.compile("diagonal:?.*true")
        valid = list(filter(pattern.match, input))
        return len(valid) > 0

    def is_negative_kropki(self, input: list[str]) -> bool:
        pattern = re.compile("neg(ative)?-?\s?_kropki:?.*true")
        valid = list(filter(pattern.match, input))
        return len(valid) > 0

    def is_negative_xv(self, input: list[str]) -> bool:
        pattern = re.compile("neg(ative)?-?\s?_xv:?.*true")
        valid = list(filter(pattern.match, input))
        return len(valid) > 0

    def parse(self) -> dict[str, list[str] | bool]:
        parsed_puzzle = {}
        input = self.read_file()

        parsed_puzzle["givens"] = self.parse_givens(input)
        parsed_puzzle["arrow"] = self.parse_arrow(input)
        parsed_puzzle["entropic"] = self.parse_entropic(input)
        parsed_puzzle["even_odd"] = self.parse_even_odd(input)
        parsed_puzzle["extra_regions"] = self.parse_extra_regions(input)
        parsed_puzzle["german_whispers"] = self.parse_german_whispers(input)
        parsed_puzzle["killer"] = self.parse_killer(input)
        parsed_puzzle["kropki"] = self.parse_kropki(input)
        parsed_puzzle["palindrome"] = self.parse_palindrome(input)
        parsed_puzzle["quadruple"] = self.parse_quadruple(input)

        parsed_puzzle["renban"] = self.parse_renban(input)
        parsed_puzzle["thermo"] = self.parse_thermo(input)
        parsed_puzzle["xv"] = self.parse_xv(input)

        parsed_puzzle["anticonsecutive"] = self.is_anticonsecutive(input)
        parsed_puzzle["antiking"] = self.is_antiking(input)
        parsed_puzzle["antiknight"] = self.is_antiknight(input)
        parsed_puzzle["diagonal"] = self.is_diagonal(input)
        parsed_puzzle["neg_kropki"] = self.is_negative_kropki(input)
        parsed_puzzle["neg_xv"] = self.is_negative_xv(input)

        return parsed_puzzle
