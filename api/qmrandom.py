import random
import requests



url = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=hex16&size=4"

def _getSeed():
    r = requests.get(url, verify=False)
    j = r.json()
    num = j["data"][0]
    i = int(num, 16)
    return i

class qmrandom(random.Random):

    def seed(self, x=None):
        super(qmrandom, self).seed(_getSeed())

    def random(self):
        return super(qmrandom, self).random()

_inst = qmrandom()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits

if __name__ == "__main__":
    x = qmrandom()
    _getSeed()
