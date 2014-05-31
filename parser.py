from __future__ import unicode_literals, print_function
from pypeg2 import *

class _Parameter(str):
    grammar = re.compile(r"[\w\s]+")

class _Structure(str):
    grammar = re.compile(r"[\w\s]+")

class _Formula(List):
    grammar = maybe_some(_Structure, "{{", _Parameter, "}}")


class Parser:

    def __init__(self):
        pass

    def __parse__(self, input):
        pass

class Formula:

    def __init__(self, id, formulae, f):
        self.id  = id
        self.f


if __name__ == "__main__":
    f = parse("Next bus for {{route}} at {{intersection}}", _Formula)