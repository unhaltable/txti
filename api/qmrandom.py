import random
import requests

class qmrandom(random.Random):

    def __init__(self):
        self.nums = []
        super(qmrandom, self).__init__()

    def seed(self, x=None):
        pass

    def random(self):
        if (len(self.nums) == 0):
            self._getNums()
        return int(self.nums.pop(), 16) / (16 ** 8)

    def getstate(self):
        pass

    def setstate(self):
        pass

    def getrandbits(self, k):
        if k <= 0:
            raise ValueError('number of bits must be greater than zero')
        if k != int(k):
            raise TypeError('number of bits should be an integer')
        num = (k + 7) // 8                      # bits / 8 and rounded up
        r = requests.get("https://qrng.anu.edu.au/API/jsonI.php?length={}&type=uint8&".format(num),
                         verify=False)
        n = r.json()['data']
        i = 0
        for l in range(len(n)):
            i += n[l] << (8 * l)

        return i >> (num * 8 - k)

    def _getNums(self):
        r = requests.get("https://qrng.anu.edu.au/API/jsonI.php?length=100&type=hex16&size=4", verify=False)
        j = r.json()
        self.nums = j["data"]

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
    for i in range(100):
        print(x.randint(0, 100))

