from pcb import PCB
from queuetimes import QueueTimes
from time import sleep

class queue(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.times = QueueTimes()

    def add(self, newPCB, position=0, arrival=0, DEBUG=False):
        """Add a PCB to the end of the queue (default).
        If position is given, calls AddAt() to insert at the desired position."""

        if self.inQueue(newPCB.pid):
            print("queue.py/add(): Error, attempted to add duplicate PID to queue.")
            return False
        elif position < 0:
            print("queue.py/add(): Error, attempted to add to a negative position.")
            return False
        elif position > 0:
            self.addAt(newPCB, position, DEBUG)
        elif self.__insertBeginning(newPCB):
            return True
        else:
            self.tail.after = newPCB
            newPCB.before = self.tail
            self.tail = newPCB
            self.size += 1
            return True

    def __insertBeginning(self, newPCB):
        """Case where inserting new node to an empty list."""
        if self.head == None and self.tail == None and self.size == 0:
            #Insert first node
            self.head = newPCB
            self.tail = newPCB
            self.size += 1
            return True

        return False

    def addAt(self, newPCB, position, DEBUG=False):
        """Add a PCB to the desired Queue position."""

        if position < 0:
            print("queue.py/addAt(): Error, attempted to add to a negative position.")
            return False
        elif self.inQueue(newPCB.pid):
            print("queue.py/addAt(): Error, attempted to add duplicate PID to queue.")
            return False
        elif position > self.size:
            print("AddAt() wants to add at %s, but size of %s" % (position, self.size))
            return False
        elif position == 1:
            oldHeadPCB = self.head
            oldHeadPCB.before = newPCB
            newPCB.after = self.head
            self.head = newPCB
            self.size += 1
        else:
            tmpPtr = self.head
            for x in range(1,position-1):
                if DEBUG: print('current pid:', tmpPtr.pid)
                if DEBUG and type(tmpPtr.after) is PCB: print('next pid:', tmpPtr.after.pid)
                tmpPtr = tmpPtr.after

            newPCB.after = tmpPtr.after
            newPCB.before = tmpPtr
            tmpPtr.after.before = newPCB
            tmpPtr.after = newPCB
            self.size += 1

    def show(self):
        """Used to output the list to screen. """
        if self.size == 0:
            print("queue.py/show(): ERROR: Attempted to show empty queue.")
            return False
        else:
            tmpPtr = self.head
            while (type(tmpPtr) is PCB):
                # CSV Headers: Process_id, arrival_time, burst_time, priority
                print("PID:%s, Arrival:%s, Burst:%s, Pri:%s, Mem Location:%s" % (tmpPtr.pid, tmpPtr.simArrival,
                                                                                 tmpPtr.simBurst, tmpPtr.priority,
                                                                                 tmpPtr))
                tmpPtr = tmpPtr.after

    def showReverse(self):
        """Used to output the list to screen, starting from the tail. """
        if self.size == 0:
            print("queue.py/showReverse(): ERROR: Attempted to show empty queue.")
            return False
        else:
            tmpPtr = self.tail
            while (type(tmpPtr) is PCB):
                print("PID:%s Pri:%s -- obj: %s" % (tmpPtr.pid, tmpPtr.priority, tmpPtr))
                tmpPtr = tmpPtr.before

    def delete(self, pid=None):
        """Delete a given pid from queue.
        If no PID given, defaults to removing head node."""
        if pid:
            self.deleteByPID(pid)
            return
        elif self.head is None:
            print("queue.py/delete(): ERROR: Tried to delete empty queue.")
            return
        elif self.head.after is None:
            self.head = None
            self.tail = None
            self.size = 0
        else:
            try:
                self.head = self.head.after
                self.head.before = None
                self.size -= 1
            except Exception as e:
                print("queue.py/delete(): Error, unable to delete: ", pid)

    def deleteByPID(self, pid):
        """Delete by PID"""

        if not self.inQueue(pid):
            print("queue.py/deleteByPID(): Error, attempted to delete PID that was not in queue.")
            return False

        deleteMe = self.findByPID(pid)      # Find PCB in the linked list

        if deleteMe.before is None:
            self.delete()
            return
        elif deleteMe.after is None:
            deleteMe.before.after = None
            self.tail = deleteMe.before
        else:
            deleteMe.before.after = deleteMe.after
            deleteMe.after.before = deleteMe.before

        self.size -= 1

    def findByPID(self, pid):
        """Find via PID, return PCB once found"""
        tmpPtr = self.head
        while (type(tmpPtr) is PCB):
            if tmpPtr.pid == pid:
                return tmpPtr
            tmpPtr = tmpPtr.after
        return False

    def inQueue(self, pid):
        """Find via PID, return True if exists in queue, otherwise False."""
        if self.head is not None:
            tmpPtr = self.head
            while (type(tmpPtr) is PCB):
                if tmpPtr.pid == pid:
                    return True
                tmpPtr = tmpPtr.after
            return False
        return False

    def processPCB(self, tmpPCB, q=None):
        """This function 'simulates' the processor working on a specified process.
        sleep() is used to simulate work.
        Upon completion: the PCB burst is decremented, and CPU step is incremented.
        """

        print("\r")
        print("CPU now processing PID : %s, Burst: %s" % (tmpPCB.pid, tmpPCB.simBurst))
        tmpPCB.inProcessing(self.times.step)    #Update PCB timing

        if type(q) is int:
            while tmpPCB.simBurst > 0 and q > 0:
                sleep(0.001)  # sleep for 1 MS
                tmpPCB.simBurst -= 1
                q -= 1
                self.times.step += 1  # increment the cpu 'counter'
        else:
            while tmpPCB.simBurst > 0:
                sleep(0.001) #sleep for 1 MS
                tmpPCB.simBurst -= 1
                self.times.step += 1  # increment the cpu 'counter'

        tmpPCB.outProcessing(self.times.step)   #Update PCB timing

        if tmpPCB.simBurst == 0:    # If the PCB is fully complete, update times accordingly.
            tmpPCB.complete(self.times.step)
            self.times.updateQueueTimes(tmpPCB)
            tmpPCB.printSimTimes()
            try:
                self.delete(tmpPCB.pid)
            except Exception as e:
                print("queue.py/processPCB():", e)

    def finishQueue(self):
        self.times.finishQueue()

    def printQueueSimStats(self, type="[Undefined Type]"):
        self.times.printQueueSimStats(type)