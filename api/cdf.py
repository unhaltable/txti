import urllib2
import sre

class Lab():
    def __init__(self):
        self.name = ''
        self.avail = ''
        self.busy = ''
        self.total = ''
        self.percent_busy = ''
        self.timestamp = ''

    def set_name(self, name):
        self.name = name

    def set_avail(self, avail):
        self.avail = avail

    def set_busy(self, busy):
        self.busy = busy

    def set_total(self, total):
        self.total = total

    def set_percent(self, percent):
        self.percent_busy = percent

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def __str__(self):
        return '{0}: {1} available of {2} machines ({3}% busy)'.format(self.name, self.avail, self.total, self.percent_busy)


address = 'http://www.cdf.toronto.edu/usage/'

def get_data():
    try:
        website = urllib2.urlopen(address)
        html = website.read()
        matches = sre.findall('<TD>[A-Za-z0-9\.]*', html)
        return matches
    except:
        return "Could not retrieve data."

def parse():
    data = get_data()
    i = 0
    labs = []
    for item in data:
        item = str(item).strip('<TD>')
        if i == 0:
            lab = Lab()
            if not (item == 'NX' or item == 'gerstein'):
                lab.set_name('BA' + item)
            elif item == 'gerstein':
                lab.set_name('Gerstein')
            else:
                lab.set_name(item)
        elif i == 1:
            lab.set_avail(item)
        elif i == 2:
            lab.set_busy(item)
        elif i == 3:
            lab.set_total(item)
        elif i == 4:
            lab.set_percent(item)
        elif i == 5:
            lab.set_timestamp(item)
            labs.append(lab)
            i = -1
        i += 1
    return labs

def get_lab(query):
    if (query.lower() == 'korea'):
        query = 'BA2240'
    elif(query.lower() == 'china'):
        query = 'BA2210'
    labs = parse()
    for lab in labs:
        if lab.name == query:
            return str(lab)
    return "Could not find {0}".format(query)

def lab(l):
    return get_lab(l[0])


if __name__ == '__main__':
    labs = parse()
    #for lab in labs:
    #    print lab

    print get_lab("BA2200")
    print get_lab("BA3200")
    print get_lab("NX")
    print get_lab("awjrlarwa")

    print lab(["BA3200"])