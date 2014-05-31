import re

class Parser:

    def __init__(self):
        pass

    def __parse__(self, input):
        pass

class Formula:

    def __init__(self, id, formulae, f):
        self.id  = id
        self.f = f
        l = re.split(r"{{|}}", formulae)
        while '' in l:
            l.remove('')
        print l

def testfunc():
    pass

if __name__ == "__main__":
    f = Formula("bustime", "Next bus for {{route}} at {{intersection}}", testfunc)