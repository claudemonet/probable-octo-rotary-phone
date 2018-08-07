from queue import queue
from pcb import PCB

class RoundRobin(queue):
    def __init__(self, q=2):
        super().__init__()
        self.q = q
        self.type = "Round Robin (Quantum=%s)" % self.q
        self.nextToRun = None
        self.lastRun = None
        self.queueSizeBeforeNextRun = 0

    def runNew(self):
        """
        Runs through the queue once, looking for the next PCB to run.
        """
        if self.size == 0:          # If there's nothing in queue,
            self.times.step += 1    #   increment CPU step to enable new arrivals to happen.
            return

        tmpPtr = self.head

        if self.nextToRun != None:
            while (type(tmpPtr) is PCB):        # Iterate through queue, looking for the next PCB to run
                if tmpPtr == self.nextToRun:
                    break
                else:
                    tmpPtr = tmpPtr.after

        """The following code block checks if a new PCB was added since last preemption.
            If new PCBs have been added, then update nextToRun to the new PCB. 
        """
        if self.nextToRun == None:
            if self.queueSizeBeforeNextRun != self.size:
                if self.lastRun != None:
                    tmpPtr = self.lastRun
                    tmpPtr = tmpPtr.after

        self.processPCB(tmpPtr, self.q)
        self.lastRun = tmpPtr
        self.nextToRun = tmpPtr.after
        self.queueSizeBeforeNextRun = self.size

        return self.size