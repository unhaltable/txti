import random

def rng(l):
    s = l[0]
    if s == '':
        return str(random.random())
    else:
        x = s[1:].split()
        return str(random.randint(int(x[0]), int(x[1])))