import re
from utils import Production


class Parser:
    prod_regex = "^\([a-z]\)[ ]?[a-z][ ]?:=[ 0-9a-z+\-*/]+$"
    alph_regex = "^[A-Z][ ]?=[ ]?{[a-z](,[ ]?[a-z])*}$"
    word_regex = "^w[ ]?=[ ]?[a-z]+$"

    def __init__(self, input: str) -> None:
        self.productions = []
        self.alphabet = []
        self.word = ""

        for line in input.split("\n"):
            if re.match(self.prod_regex, line):
                name = line[1]
                symbols = list(filter(lambda s: s.isalpha(), line[3:]))
                self.productions.append(Production(name, symbols[1:], [symbols[0]]))
            elif re.match(self.alph_regex, line):
                self.alphabet = list(filter(lambda s: s.isalpha(), line[2:]))
            elif re.match(self.word_regex, line):
                self.word = list(filter(lambda s: s.isalpha(), line[2:]))

    def get_alphabet(self):
        return self.alphabet

    def get_productions(self):
        return self.productions

    def get_word(self):
        return self.word
