from pcb import *
from queue import queue
from random import randint
from time import sleep
import sys
from fcfs import FCFS
from priority import Priority
from roundrobin import RoundRobin

"""This isn't fully complete..."""


FILENAME = 'sample_data.txt'

def getKey(PCB):
    return PCB.simArrival

def loadFromFile():
    """Loads data from the file, defined in gloabl FILENAME above """
    simulateAdding = []

    with open(FILENAME) as f:
        for line in f.readlines():
            # CSV Headers: Process_id, arrival_time, burst_time, priority
            content = line.split(',')
            PID = int(content[0])
            simArrival = int(content[1])
            simBurst = int(content[2])
            priority = int(content[3])
            simulateAdding.append( PCB(PID, simArrival=simArrival, simBurst=simBurst, priority=priority) )

    return simulateAdding

def simulateArrivals(option):
    """Powers the simulation"""
    simulateAdding = loadFromFile()
    simulateAdding.sort(key=getKey)
    ready = None

    if option == 1:
        ready = FCFS()
    elif option == 2:
        ready = Priority()
    elif option == 3:
        q = 2
        try:
            q = int(input("Enter Quantum (Defauult=2):"))
        except:
            print("Invalid entry. Using default Quantum of 2.")
            pass
        ready = RoundRobin(q)
    elif option == 4:
        runAllQueues()
        return
    elif option == 5:
        exit(1)
    else:
        print("Invalid option.")
        return

    print("\r")
    print("***************************************************")
    print("Running %s Scheduler" % ready.type)

    remainingQueueSize = 0
    while len(simulateAdding) > 0 or remainingQueueSize > 0:
        for k in simulateAdding[:]:
            if k.simArrival <= ready.times.step:
                try:
                    ready.add( PCB(k.pid, simArrival=k.simArrival, simBurst=k.simBurst, priority=k.priority))
                except Exception as e:
                    print (e)
                simulateAdding.remove(k)

        print("Current Queue:")
        ready.show()
        remainingQueueSize = ready.runNew()

    ready.finishQueue()
    ready.printQueueSimStats(ready.type)

def runAllQueues():
    """If user wants to run all queues"""
    for k in range(1,4):
        simulateArrivals(k)


def printQueueOptions():
    options = [
        "Which operation do you want to perform?",
        "1) Run First Come First Served Simulation",
        "2) Run Priority Simulation",
        "3) Run Round Robin Simulation",
        "4) Run All",
        "5) Exit"
    ]

    for option in options:
        print(option)

def main():
    while True:
        print("\r")
        printQueueOptions()
        choice = 0
        try:
            choice = int(input())
        except:
            pass

        simulateArrivals( choice )

#hw3()
#exit(0)
#stress_test() #--works yay!
#small_rand_test()

main()
#adding_by_arrival_simulation()

#simulateArrivals()


#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#Old Deprecated Testing Functions Below

def adding_by_arrival_simulation():
    simulateAdding = []
    simulateAdding.append(PCB(9999, simArrival=0, simBurst=1))
    for y in range(1, 5):
        randPID = randint(1, 10000)
        randArrive = (randint(1, 4))
        randBurst = (randint(1, 9))
        randPriority = (randint(1, 10))
        simulateAdding.append( PCB(randPID, simArrival=randArrive, simBurst=randBurst, priority=randPriority) )

    #simulateAdding = []
    simulateAdding.sort(key=getKey)

    classGivenQueue = []
    classGivenQueue.append(PCB(2710, simArrival=8, simBurst=6, priority=2))
    classGivenQueue.append(PCB(2720, simArrival=8, simBurst=2, priority=1))
    classGivenQueue.append(PCB(2730, simArrival=0, simBurst=8, priority=1))
    classGivenQueue.append(PCB(2740, simArrival=2, simBurst=5, priority=3))
    classGivenQueue.append(PCB(2750, simArrival=6, simBurst=10, priority=4))

    classGivenQueue.sort(key=getKey)
    simulateAdding = classGivenQueue

    #ready = FCFS()
    #521pm, FCFS is ok!!!
    ready = Priority()
    #620pm, priority is ok!!!
    #ready = randPriority()
    #ready = RoundRobin(1)

    print("Pid, arrival, burst, priority")
    for k in simulateAdding:
        print(k.pid, k.simArrival, k.simBurst, k.priority)

    j = 0
    remainingQueueSize = 0
    while len(simulateAdding) > 0 or remainingQueueSize > 0:
        j += 1
        for k in simulateAdding[:]:
            if k.simArrival <= ready.times.step:
                print("in sim...curr step:", ready.times.step)
                if j == 1: position = 0
                else: position = 1
                print("In sim...adding: %s to position %s" % (k.pid, position))
                try:
                    ready.add( PCB(k.pid, simArrival=k.simArrival, simBurst=k.simBurst, priority=k.priority))#), position=position )
                except Exception as e:
                    print (e)
                #ready.show()

                simulateAdding.remove(k)

        remainingQueueSize = ready.runNew()

    ready.finishQueue()
    ready.printQueueSimStats("ready")
    #ready.times.finishQueue()
    #ready.times.printQueueSimStats()






def first_test():
    a = PCB(1,priority=3)
    b = PCB(2,priority=2)
    c = PCB(3,priority=3)
    d = PCB(4,priority=2)
    e = PCB(5,priority=1)

    ready = queue()
    ready.add(a,1)
    ready.add(b,1)
    ready.add(c,-1)
    ready.add(d,1)
    ready.add(e,1)

    print ('a:', a)
    print ('b:', b)
    print ('c:', c)

    ready.showReverse()
    print("\r\n")
    ready.show()

    y = PCB(111,priority=44)
    print("\r\n")
    print("\r\n")
    ready.add(y,position=3)
    ready.add(y,position=4)
    ready.add(y,position=4)

    ready.show()
    print("\r\n")
    ready.showReverse()
    print("\r\n")


#    ready.delete(3)
    ready.showReverse()
    print("\r\n")
    ready.show()

def stress_test():
    ready = queue()

    y = 0
    #while True:
    for y in range(1,100):
        rand = randint(2,4)
        PCBRand = randint(0, 1000)
        #print("---------Rolling Dice, Start of Round---------")
        if rand == 1:
            #print("Adding PCB", PCBRand)
            ready.add(PCB(PCBRand, priority=randint(1, 4)))
        elif rand == 2:
            print("Adding PCB PID: ", PCBRand)
            ready.add( PCB(PCBRand, priority=randint(1, 4)), position=randint(0, 1))
        elif rand == 3:
            #print("Deleting PCB!")
            ready.delete()
        elif rand == 4:
            print("Deleting a PCB by PID!")
            print("Trying to delete ", PCBRand)
            ready.delete(PCBRand)

    print("Final queue size:", ready.size)
    #sleep(4)
    ready.show()

def small_rand_test():
    ready = queue()
    y = 0
    for y in range(1,20):
        randPID = randint(1, 10)
        randArrive = (randint(0,10))
        randBurst = (randint(0,10))
        tmpPCB = PCB(randPID,arrival=randArrive, burst=randBurst)

    simulateAdding = []
    simulateAdding.append(tmpPCB)

    simulateAdding.sort()

    print (simulateAdding)




def hw3():
    ready = queue()

    while True:
        print("\r")
        printOptions()
        choice = input()
        choice = int(choice)

        if choice == 1:
            PIDtoAdd = input("What is the PID to add:")
            if ready.add( PCB(int(PIDtoAdd)) ):
                print("PID Added to the Queue")
        elif choice == 2:
            print("Deleting from front of queue.")
            ready.delete()
        elif choice == 3:
            ready.show()
        elif choice == 4:
            return
        else:
            continue

def printOptions():
    options = [
        "Which operation do you want to perform?",
        "1) Add PCB to the queue",
        "2) Delete PCB from a queue",
        "3) Print the queue",
        "4) Exit"]

    for option in options:
        print(option)
