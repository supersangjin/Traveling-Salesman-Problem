import sys
import getopt
import math
import random
import time

class City:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNum(self):
        return self.num

    def calculateDistance(self, city):
        return math.sqrt((self.getX() - city.getX())**2 + (self.getY() - city.getY())**2)

class CitiesList:
    def __init__(self):
        self.citiesList = []

    def addCity(self, city):
        self.citiesList.append(city)

    def getList(self):
        return self.citiesList

    def getCity(self, idx):
        return self.citiesList[idx]

class Path:
    def __init__(self, citieslist, dimension, fit, temp, rate):
        self.citieslist = citieslist
        self.dimension = dimension
        self.path = []
        self.fit = fit
        self.temp = temp
        self.rate = rate

    def addCity(self, city):
        self.path.append(city)

    def getCity(self, idx):
        return self.path[idx]

    def generateRandomPath(self):
        for i in range(0, self.dimension):
            self.path.append(self.citieslist.getCity(i))
        random.shuffle(self.citieslist.getList())

    def getTotalDistance(self):
        distance = 0
        for i in range(0, self.dimension-1):
            distance += self.path[i].calculateDistance(self.path[i+1])
        distance += self.path[self.dimension-1].calculateDistance(self.path[0])
        return distance

    def rotate(self, n):
        copy = self.path[:]
        self.path = copy[n:] + copy[:n]

    def getAcceptanceProb(self, city1, city2):
        self.fit -= 1
        beforeDistance = self.path[city1 - 1].calculateDistance(self.path[city1]) + self.path[city2].calculateDistance(self.path[city2+1])
        afterDistance = self.path[city1 - 1].calculateDistance(self.path[city2]) + self.path[city1].calculateDistance(self.path[city2+1])
        if (beforeDistance > afterDistance):
            return 1
        else:
            prob = math.exp((beforeDistance - afterDistance)/self.temp)
            return prob

    def reverse(self, city1, city2):
        reversedPath = self.path[:]
        reversedPath[city1 : city2+1] = reversed(self.path[city1 : city2+1])
        self.path = reversedPath

    def simulatedAnnealing(self):
        for i in range(1, dimension - 2):
            for j in range(i, dimension - 1):
                if (self.getAcceptanceProb(i , j) > random.random()):
                    self.reverse(i , j)
                if (self.fit == 0):
                    return
        self.rotate(5000)
        self.temp *= (1 - self.rate)

    def organize(self):
        for i in range(dimension):
            if (self.path[i].getNum() == 1):
                start = i
                break
        copy = self.path[:]
        self.path = copy[start:] + copy[:start]

def help():
    print("-f maximum fitness evaluation\n-t starting temperature\n-r temperature cool rate\n-h help")

def getParam(argv):
    try:
        opts, args = getopt.getopt(argv[1:],"f:r:t:h")

    except getopt.GetoptError as err:
        print (str(err))
        help()
        sys.exit(1)

    fitness = 100000   # default fitness
    temp = 20          # default temperature
    rate = 0.1         # default rate
    filename = argv[0]

    for opt,arg in opts:
        if (opt == "-f"):
            fitness = int(arg)
        elif (opt == "-t"):
            temp = int(arg)
        elif (opt == "-r"):
            rate = float(arg)
        elif (opt == "-h"):
            help()
    return fitness, temp, rate, filename

#Parse the coordinates of the cities from the file and store it in city_dict
def parse(file):
    tsp_list = []
    numeric = False
    f = open(file,'r')
    while True:
        line = f.readline()
        if not line: break
        if line.startswith('DIMENSION'):
            dimension = int(line.strip().split(':')[1])
        if line.startswith('1'):
            numeric = True
        if line.startswith('EOF'):
            numeric = False
        if (numeric):
            tsp_list.append([int(float(x.strip())) for x in line.strip().split(' ')])
    f.close()
    return tsp_list, dimension

if __name__ == '__main__':
    t0 = time.time()
    fit, temp, rate, filename = getParam(sys.argv[1:])
    tspList, dimension = parse(filename)
    citiesList = CitiesList()
    for node in tspList:
        city = City(node[1], node[2], node[0])
        citiesList.addCity(city)
    initialPath = Path(citiesList, dimension, fit, temp, rate)
    initialPath.generateRandomPath()
    i = 0
    while(initialPath.temp > 1):
        initialPath.simulatedAnnealing()
        i += 1
        distance = initialPath.getTotalDistance()
        #print(str(i) + "th distance : " + str(distance))
        #print("temp : " + str(initialPath.temp))
        if (initialPath.fit == 0):
            break;
    t1 = time.time()
    total = t1-t0
    #print("final distance : " + str(initialPath.getTotalDistance()) + "      "   +str(total))
    print(str(initialPath.getTotalDistance()))
    initialPath.organize()
    f = open("solution.csv",'w')
    for i in range(dimension):
        data = "%d\n" % initialPath.path[i].getNum()
        f.write(data)
    f.close
