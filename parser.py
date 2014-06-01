import re

func = (
    '''def func(l):
        return {}
    ''')

class Parser:
    def __init__(self):
        self.formulae = []
        self.man = {}

    def parse(self, input):
        if input[:4] == "help":
            return 'I think you meant to use "man {{ function }}"'
        if input[:3] == 'man':
            return self.man(re.sub("man", '', input).strip())
        self.formulae.sort(lambda x,y: len(x) < len(y))
        for formula in self.formulae:
            mat = re.search(formula.pieces[0], input)
            if (mat != None and mat.pos == 0):
                return self.analyze(formula, input)

    def man(self, input):
        if input == "help":
            return "lol"
        else:
            return self.man[input]

    def analyze(self, formula, input):
        inputs = []
        i = 0
        if len(formula.pieces) == 1:
            inputs.append(input[re.search(formula.pieces[0], input).end(0):])
            return formula.f(inputs)
        while i < len(formula.pieces) - 1:
            begin = re.search(formula.pieces[i], input)
            end = re.search(formula.pieces[i + 1], input)
            num1 = begin.end(0)
            num2 = end.start(0)
            inputs.append(input[num1:num2])
            i += 1
        inputs.append(input[end.end():])
        return formula.f(inputs)

    def addFormula(self, formula):
        for item in self.formulae:
            if item == formula:
                return
        self.man[formula.id] = formula.form
        self.formulae.append(formula)

    def addNoParamFormula(self, req, response):
        ''' CAUSE REFLECTIVE CODE '''
        x = func.format(response)
        exec x
        self.addFormula(Formula(req, req, func))

class Formula:
    def __init__(self, id, formula, f):
        self.form = formula
        self.id = id
        self.f = f
        if (re.search(r'{{', formula) == None):
            self.pieces = [formula]
        else:
            l = re.split(r"{{|}}", formula)
            while '' in l:
                l.remove('')
            self.pieces = [l[i] for i in range(0, len(l), 2)]

    def __eq__(self, other):
        return (self.id == other.id and self.f == other.f
                and self.pieces == other.pieces)


def testfunc(l):
    print l


if __name__ == "__main__":
    # below does not work
    '''
    f = Formula("bustime", "Next bus for {{route}} {{direction}} at {{intersection}}", testfunc)
    p = Parser()
    p.addFormula(f)
    result = p.parse("Next bus for 116 North at Coronation and Lawrence")
    print(repr(result))
    '''
    f = Formula("rng", "rng{{min max}}", testfunc)
    p = Parser()
    p.addFormula(f)
    result1 = p.parse("rng")
    result2 = p.parse("rng 5 10")