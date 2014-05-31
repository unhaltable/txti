__author__ = 'jonathanwebb'
from plex import *
import cStringIO

class Parser:

    def __init__ (self):
        self.formulae = {} ## dict of string to Formula objects
        self.lex = [] ## list of lexical rules


    def addFormula(self, formula):
        if (self.__checkIfIDUsed(formula.id)):
            raise DuplicateIDException
        else:
            self.formulae[formula.id] = formula
            for rule in formula.rules:
                self.lex.append(rule)

    def __checkIfIDUsed(self, id):
        for key in self.formulae.keys():
            if id == key:
                return True
        return False

    def parse(self, input):
        new = self.lex[:]
        #new.append((Rep(Range("AZaz") | Range("09") | Str(" ")), TEXT))
        lex = Lexicon(new)
        s = cStringIO.StringIO(input)
        scanner = Scanner(lex, s)

        id = None
        inputs = []
        while 1:
            token = scanner.read()
            if token[1] is '':
                break
            else:
                if (token[0][:3] == 'id_'):
                    if (not id):
                        id = token[0][3:]
                    elif (id and id != token[0][3:]):
                        raise Exception

                else:
                    inputs.append(token[0])


class Formula:

    def __init__(self, id, formula, f):
        '''
        :param id: str
        :param formula: str
        :param f: a function that takes a list of strings
        :return: None
        '''

        self.func = f
        self.id = id

        letter = Range("AZaz")
        digit = Range("09")
        text = Rep(letter | digit | Str(" "))
        open_bracket = Str('{{')
        close_bracket = Str('}}')
        lex = Lexicon([
            (text, 'terminal'),
            (open_bracket, 'open'),
            (close_bracket, 'close')
        ])
        s = cStringIO.StringIO(formula)
        scanner = Scanner(lex, s)

        tokens = []
        while 1:
            token = scanner.read()
            if token[1] is '':
                break
            else:
                tokens.append(token)
                print token

        lexl = []
        param = False
        for instance in tokens:
            if (instance[0] == 'terminal' and not param):
                lexl.append((Str(instance[1]), 'id_' + self.id))
            elif(instance[0] == 'open'):
                param = True
            elif(instance[0] == 'close'):
                param = False

        self.rules = lexl

        for x in lexl:
            print x

class DuplicateIDException(Exception):
    pass

def testfunc():
    print "x"

if __name__ == '__main__':
    y = Formula('testfunc', 'Next bus for {{route}} at {{intersection}}', testfunc)
    x = Parser()
    x.addFormula(y)
    x.parse("Next bus for 116 at Coronation and Lawrence")