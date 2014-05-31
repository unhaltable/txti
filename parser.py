import re

class Parser:

    def __init__(self):
        self.formulae = []

    def parse(self, input):
        for formula in self.formulae:
            mat = re.search(formula.pieces[0], input)
            if(mat != None and mat.pos == 0):
                return self.analyze(formula, input)


    def analyze(self, formula, input):
        inputs = []
        i = 0
        while i < len(formula.pieces) - 1:
            begin = re.search(formula.pieces[i], input)
            end = re.search(formula.pieces[i + 1], input)
            num1 = begin.end(0)
            num2 = end.start(0)
            inputs.append(input[num1:num2])
            i+=1
        inputs.append(input[end.end():])
        return formula.f(inputs)

    def addFormula(self, formula):
        self.formulae.append(formula)


class Formula:

    def __init__(self, id, formula, f):
        self.id  = id
        self.f = f
        l = re.split(r"{{|}}", formula)
        while '' in l:
            l.remove('')
        self.pieces = [l[i] for i in range(0, len(l), 2)]
        self.head = l[0]



def testfunc():
    pass

if __name__ == "__main__":
    f = Formula("bustime", "Next bus for {{route}} at {{intersection}}", testfunc)
    p = Parser()
    p.addFormula(f)
    p.parse("Next bus for 116 at Coronation and Lawrence")