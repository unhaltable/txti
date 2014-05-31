import re

class Parser:

    def __init__(self):
        self.formulae = []

    def parse(self, input):
        for formula in self.formulae:
            mat = re.search(formula.pieces[0], input)
            if(mat != None and mat.pos == 0):
                self.analyze(formula, input)
                return

    def analyze(self, formula, input):
        inputs = []
        pass

    def addFormula(self, formula):
        self.formulae.append(formula)


class Formula:

    def __init__(self, id, formula, f):
        self.id  = id
        self.f = f
        l = re.split(r"{{|}}", formula)
        while '' in l:
            l.remove('')
        self.pieces = l
        self.head = l[0]



def testfunc():
    pass

if __name__ == "__main__":
    f = Formula("bustime", "Next bus for {{route}} at {{intersection}}", testfunc)
    p = Parser()
    p.addFormula(f)
    p.parse("Next bus for 116 at Coronation and Lawrence")