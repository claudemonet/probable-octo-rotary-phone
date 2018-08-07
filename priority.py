from queue import queue
from pcb import PCB
import sys

class Priority(queue):
    def __init__(self):
        super().__init__()
        self.type = "Priority"

    def runNew(self):
        """
        Runs through the queue once, looking for highest priority PCB,
        then process the highest priority PCB.
        """
        if self.size == 0:          # If there's nothing in queue,
            self.times.step += 1    #   increment CPU step to enable new arrivals to happen.
            return

        tmpPtr = self.head
        highPriVal = sys.maxsize    # Lower int = highest priority. Set value to a high int,
        highPriPCB = None           #   then look for lower int priorities.
        while (type(tmpPtr) is PCB):
            if tmpPtr.priority < highPriVal:
                highPriPCB = tmpPtr
                highPriVal = highPriPCB.priority
            tmpPtr = tmpPtr.after

        if highPriPCB == None:
            tmpPtr = self.head
            return

        self.processPCB(highPriPCB)

        return self.size
