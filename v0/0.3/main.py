import datetime

#class definitions
class timerange:
    def __init__(self, starttime, endtime):
        self.starttime = starttime
        self.endtime = endtime

class person:
    def __init__(self, name, notfreetimes):
        self.name = name
        self.notfreetimes = notfreetimes

class timerangemarks:
    def __init__(self, starttime, endtime, notfree):
        self.starttime = starttime
        self.endtime = endtime
        self.notfree = notfree

mastertimeranges = []
people = []
dailyTimeRange = None
rawfinal = []
final = None

def addnewperson():
    name = input("New person name: ")
    notfreetimes = []
    addmoretimes = 'y'
    while addmoretimes[0].lower() != 'n':
        date = input("busy date: ").strip()
        starttime = input("busy starting from what time on that date: ").strip()
        endtime = input("busy till what time on that date: ").strip()
        starttime = datetime.datetime.strptime(date + " " + starttime, "%d/%m/%Y %H:%M")
        endtime = datetime.datetime.strptime(date + " " + endtime, "%d/%m/%Y %H:%M")
        notfreetimes.append(timerange(starttime, endtime))
        addmoretimes = input("add more busy times?\n(y/n)\n").strip()
        #if addmoretimes[0].lower() == 'n':
        #    break
    people.append(person(name, notfreetimes))
    
def gettimerange():
    startingdate = datetime.datetime.strptime(input("find free times starting what date?\n").strip(), "%d/%m/%Y")
    endingdate = datetime.datetime.strptime(input("find free times ending what date?\n").strip(), "%d/%m/%Y")
    startingtime = datetime.datetime.strptime(input("starting on what time everyday?\n").strip(), "%H:%M")
    endingtime = datetime.datetime.strptime(input("ending on what time everyday?\n").strip(), "%H:%M")
    global dailyTimeRange
    dailyTimeRange = timerange(startingtime.time(), endingtime.time())
    mastertimeranges.clear()
    i = startingdate
    while i != endingdate:
        starttime = datetime.datetime.combine(i.date(), startingtime.time())
        endtime = datetime.datetime.combine(i.date(), endingtime.time())
        mastertimeranges.append(timerange(starttime, endtime))
        i += datetime.timedelta(days = 1)

def time_in_range(start, end, x):
    return start <= x <= end

def calculate():
    criticalpoints = []
    for i in people:
        for j in range(len(i.notfreetimes)):
            if i.notfreetimes[j].starttime.time() >= dailyTimeRange.endtime or i.notfreetimes[j].endtime.time() <= dailyTimeRange.starttime:
                continue
            elif i.notfreetimes[j].starttime.time() < dailyTimeRange.starttime:
                i.notfreetimes[j].starttime = datetime.datetime.combine(i.notfreetimes[j].starttime.date(), dailyTimeRange.starttime)
            if i.notfreetimes[j].endtime.time() > dailyTimeRange.endtime:
                i.notfreetimes[j].endtime = datetime.datetime.combine(i.notfreetimes[j].endtime.date(), dailyTimeRange.endtime)    
            if i.notfreetimes[j].starttime not in criticalpoints: 
                criticalpoints.append(i.notfreetimes[j].starttime)
            if i.notfreetimes[j].endtime not in criticalpoints:
                criticalpoints.append(i.notfreetimes[j].endtime)
    for i in mastertimeranges:
        if i.starttime not in criticalpoints: 
            criticalpoints.append(i.starttime)
        if i.endtime not in criticalpoints:
            criticalpoints.append(i.endtime)
    criticalpoints.sort()
    for i in range(1, len(criticalpoints)):
        if criticalpoints[i-1].date() == criticalpoints[i].date():
            notfree = 0
            starttime = criticalpoints[i-1]
            endtime = criticalpoints[i]
            for j in people:
                for k in j.notfreetimes:
                    if time_in_range(k.starttime, k.endtime, starttime) and time_in_range(k.starttime, k.endtime, endtime):
                        notfree += 1
            rawfinal.append(timerangemarks(starttime, endtime, notfree))
    global final
    final = sorted(rawfinal, key=lambda timerange: timerange.notfree)

def showsessions():
    for i in final:
        print(i.starttime, i.endtime, i.notfree)
    


def main():
    print("1. Add new person\n2. Set time range\n3. Calculate free times\n4. Show not free times")
    choice = input("Please enter your selection: ")
    if choice[0] == "1":
        addnewperson()
        main()
    elif choice[0] == "2":
        gettimerange()
        main()
    elif choice[0] == "3":
        if len(people) > 0:
            try:
                calculate()
                main()
            except:
                print("Please complete step 1 and step 2 before calculating free times.")
                main()
        else:
            print("An error has occured, please try again.")
            main()
    elif choice[0] == "4":
        showsessions()
        main()

if __name__ == "__main__":
    print("***Welcome to Free Time Finder***\n\n")
    main()