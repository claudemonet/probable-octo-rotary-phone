from datetime import datetime

class PCB(object):
    def __init__(self, pid=0, name="", priority=0, arrival=0, burst=0, simArrival=0, simBurst=0):
        """ Variables were initially made to handle real-time CPU processing;
        However, all "sim" variables were later added to account for simulating CPU times."""
        self.pid = pid
        self.name = name
        self.priority = priority
        self.after = None
        self.before = None
        self.arrival = arrival

        self.child = None
        self.state = None
        self.inQueue = None
        self.startTime = datetime.now()
        self.endTime = 0
        self.runTime = 0
        self.waitTime = 0
        self.age = 0

        self.burst = burst
        self.lastBurst = 0
        self.avgBurst = 0
        self.numBursts = 0
        self.predictedBurst = 0

        self.registers = []

        #All simulation elements below:
        self.simArrival = simArrival
        self.simBurst = simBurst
        self.simWait = 0
        self.simTurnAround = 0
        self.simStartTime = 0
        self.simEndTime = 0
        self.simInitDefinedBurst = simBurst

    def complete(self, CPUStep):
        """
        Called when a process has finished.
        Updates CPU times, and sim times.
        """
        self.endTime = datetime.now()
        self.calculageAge()
        self.waitTime = self.age - self.runTime
        self.processSimTimes(CPUStep)

    def calculageAge(self):
        """Called to calculate the "real time" age an object lived."""
        diff = self.endTime - self.startTime
        self.age = diff.total_seconds() * 1000

    def inProcessing(self, CPUStep):
        """Update times when a PCB is admitted into CPU."""
        self.runTime = datetime.now()
        self.simStartTime = CPUStep

    def outProcessing(self, CPUStep):
        """Update times when a PCB is leaving the CPU."""
        diff = datetime.now() - self.runTime
        self.runTime = diff.total_seconds() * 1000
        self.simEndTime = CPUStep

    def processSimTimes(self, CPUStep):
        """Calculate simulation times."""
        self.simTurnAround = (CPUStep - self.simArrival)
        self.simWait = self.simTurnAround - self.simInitDefinedBurst

    def printSimTimes(self):
        """Print the simulation times."""
        print("Finished PID:", self.pid)
        print("Arrived:", self.simArrival)
        print("Wait Time:", self.simWait)
        print("Turnaround:", self.simTurnAround)

    def printRawTime(self):
        """Print the raw CPU processing times."""
        arrival = tmpPCB.arrival  # comment out if you don't want to consider 'arrival' time, i.e., you want true arrival
        print("Arrived:", tmpPCB.arrival)
        print("Runtime:", tmpPCB.runTime)
        print("Wait Time:", tmpPCB.waitTime)# - tmpPCB.arrival)
        print("Turnaround:", tmpPCB.age)# - tmpPCB.arrival)