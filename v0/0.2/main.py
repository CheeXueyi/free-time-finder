import datetime

#class definitions
class notfreetime:
    def __init__(self, date, starttime, endtime):
        self.date = date
        self.starttime = starttime
        self.endtime = endtime

class person:
    def __init__(self, name, notfreetimes):
        self.name = name
        self.notfreetimes = notfreetimes

class timeranges:
    None



#global variables
people = []
timeranges = timeranges()



#functions
def addnewperson():
    name = input("New person name: ")
    notfreetimes = []
    while True:
        date = input("busy date: ").strip()
        starttime = input("busy starting from what time on that date: ").strip()
        endtime = input("busy till what time on that date: ").strip()
        starttime = datetime.datetime.strptime(date + " " + starttime, "%d/%m/%Y %H:%M")
        endtime = datetime.datetime.strptime(date + " " + endtime, "%d/%m/%Y %H:%M")
        notfreetimes.append(notfreetime(date, starttime, endtime))
        addmoretimes = input("add more busy times?\n(y/n)\n")
        if addmoretimes[0].lower() == 'n':
            break
    people.append(person(name, notfreetimes))

def asktimerange():
    global mastertimerange
    masterTimeRange = timeranges()
    startingdate = datetime.datetime.strptime(input("find free times starting what date?\n"), "%d/%m/%Y")
    endingdate = datetime.datetime.strptime(input("find free times ending what date?\n"), "%d/%m/%Y")
    startingtime = datetime.datetime.strptime(input("starting on what time everyday?\n"), "%H:%M")
    endingtime = datetime.datetime.strptime(input("ending on what time everyday?\n"), "%H:%M")
    i = startingdate
    while i != endingdate + datetime.timedelta(days = 1):
        setattr(masterTimeRange, "date" +  i.strftime("%d/%m/%Y"), 
     
    
asktimerange()