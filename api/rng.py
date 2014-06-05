import api.qmrandom

def rng(l):
    s = l[0]
    if s == '':
        return str(api.qmrandom.random())
    else:
        x = s[1:].split()
        return str(api.qmrandom.randint(int(x[0]), int(x[1])))