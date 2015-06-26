__author__ = 'Andrei'

import math
import time
import win32com.client
import sqlite3
import os


class monitor:
    os.system('cls')
    observer = []

    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('''CREATE TABLE Monitor(section str, value str, percentage real )''')

    def __init__(self, N):
        self.seconds = N

    def notify(self):
        start = time.time()
        while (time.time() - start) < int(self.seconds):
            # Information regarding MEMORY
            strComputer = "."
            objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")

            objSWbemServices = objWMIService.ConnectServer(strComputer, "root\cimv2")
            colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_OperatingSystem")
            freePhysical = colItems[0].FreePhysicalMemory
            totalPhysical = colItems[0].TotalVisibleMemorySize
            fPercentage = float(freePhysical) * 100 / float(totalPhysical)
            freeVirtual = colItems[0].FreeVirtualMemory
            totalVirtual = colItems[0].TotalVirtualMemorySize
            vPercentage = float(freeVirtual) * 100 / float(totalVirtual)
            # Information regarding CPU

            colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_Processor")
            loadPerc = colItems[0].LoadPercentage

            totalPhysical = int(totalPhysical) / (1024.0 * 1024)
            totalVirtual = int(totalVirtual) / (1024.0 * 1024)
            freePhysical = int(freePhysical) / (1024.0 * 1024)
            freeVirtual = int(freeVirtual) / (1024.0 * 1024)
            self.c.execute(
                "INSERT INTO Monitor VALUES('%s', '%.2fGB', '')" % ('Total Physical Memory Size', totalPhysical))
            self.c.execute("INSERT INTO Monitor VALUES('%s', '%.2fGB', '(%.2f%%)')" % (
                'Free Physical Memory ', freePhysical, fPercentage))
            self.c.execute(
                "INSERT INTO Monitor VALUES('%s', '%.2fGB', '')" % ('Total Virtual Memory Size', totalVirtual))
            self.c.execute("INSERT INTO Monitor VALUES('%s', '%.2fGB', '(%.2f%%)')" % (
                'Free Virtual Memory ', freeVirtual, fPercentage))
            self.c.execute("INSERT INTO Monitor VALUES('%s', '', '%.2f%%')" % ('CPU Load Percentage ', loadPerc))

            print "Seconds past since running: " + str(time.time() - start)
            print "##########################################"
        print '\n DB\'s Content: '
        i = 0
        print "\n"
        for row in self.c.execute('SELECT * FROM Monitor'):
            if i == 5:
                print "##########################################\n"
                i = 0
            print "%s : %s %s" % (row[0], row[1], row[2])
            i += 1


p = raw_input("The program will stop after how many seconds? ")
t1 = monitor(p)
t1.notify()
