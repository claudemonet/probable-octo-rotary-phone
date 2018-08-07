from datetime import datetime

class QueueTimes(object):
    """
    This class supports queues, by giving all the timing functionality.
    Variables were initially made to handle real-time CPU processing;
        However, all "sim" variables were later added to account for simulating CPU times.
    """
    def __init__(self):
        self.startTime = datetime.now()
        self.endTime = 0
        self.runTime = 0
        self.avgTurnaround = 0
        self.avgWait = 0
        self.step = 0       # equivalent to cpu clock 'counter'
        self.__turnarounds = []
        self.__waits = []

        #Simulation variables below
        self.__simTurnarounds = []
        self.__simWaits = []
        self.avgSimTurnaround = 0
        self.avgSimWait = 0

    def updateQueueTimes(self, tmpPCB):
        """ Processes Raw and Sim times """
        self.processQueueRawTimes(tmpPCB)
        self.processQueueSimTimes(tmpPCB)

    def processQueueRawTimes(self, tmpPCB):
        """ Processes Raw times """
        self.__turnarounds.append(tmpPCB.age)
        self.__waits.append(tmpPCB.waitTime)

    def processQueueSimTimes(self, tmpPCB):
        """ Processes Sim times """
        self.__simTurnarounds.append(tmpPCB.simTurnAround)
        self.__simWaits.append(tmpPCB.simWait)

    def finishQueue(self):
        self.endTime = datetime.now()
        self.runTime = (self.endTime - self.startTime).total_seconds() * 1000
        self.calcAvgTurnaround()
        self.calcAvgWait()

    def printQueueRawStats(self, type="[Undefined Type]"):
        print("\r")
        print("%s Queue Complete, completed in [raw]: %sms." % (type, self.runTime))
        print("Average Raw Turnaround: %sms." % self.avgTurnaround)
        print("Average Raw Wait: %sms." % self.avgWait)

    def printQueueSimStats(self, type="[Undefined Type]"):
        print("\r")
        print("***************************************************")
        print("%s Queue Complete, completed in: %sms." % (type, self.step))
        print("Average Turnaround: %sms." % self.avgSimTurnaround)
        print("Average Wait: %sms." % self.avgSimWait)
        print("***************************************************")
        print("\r")

    #Math functions
    def calcAvgTurnaround(self):
        self.avgTurnaround = self.getAverage(self.__turnarounds)
        self.avgSimTurnaround = self.getAverage(self.__simTurnarounds)

    def calcAvgWait(self):
        self.avgWait = self.getAverage(self.__waits)
        self.avgSimWait = self.getAverage(self.__simWaits)

    def getAverage(self, tmpList):
        if len(tmpList) > 0:
            return sum(tmpList) / len(tmpList)
        else:
            print("queuetimes.py/getAverage(): Error, unable to calculate average of ", tmpList)
            return False
    
