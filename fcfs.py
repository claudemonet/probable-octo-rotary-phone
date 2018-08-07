from queue import queue
from pcb import PCB
import sys

class FCFS(queue):
    def __init__(self):
        super().__init__()
        self.type = "FCFS"

    def runNew(self):
        """
        Runs through the queue once, processing in First Come First Served order.
        """
        if self.size == 0:          # If there's nothing in queue,
            self.times.step += 1    #   increment CPU step to enable new arrivals to happen.
            return
        tmpPtr = self.head
        self.processPCB(tmpPtr)
        tmpPtr = self.head

        return self.size