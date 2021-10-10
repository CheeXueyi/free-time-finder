import time



#defining global variables
seconds = time.time()
currentyear = time.localtime(seconds).tm_year



#defining functions
def freeDates(*date):   #to insert free dates of a person before calculations
    datesandtimes = []
    if len(date) > 1:
        for i in date:
            currentdate = [i]
            currentdate.append(0.0)
            currentdate.append(24.0)
            datesandtimes.append(currentdate)
    else:
        datesandtimes.append(date[0])
    return(datesandtimes)

def parse(input):       #to parse rawinput
    x = input.copy()
    for i in range(len(x)):
        x[i] = x[i].split() 
        for j in range(1, len(x[i])):
            x[i][j] = x[i][j].split(",")
            for k in range(1, len(x[i][j])):
                x[i][j][k] = x[i][j][k].split("-")
    return x



#defining classes
class person():
    def __init__(self, name, *date):
        self.name = name
        self.free = freeDates(date)



#opening file
f = open("input.txt", "r" )
lines = f.read().strip()
rawinput = lines.split("\n")



#turn input into objects
people = []
print(parse(rawinput))

    