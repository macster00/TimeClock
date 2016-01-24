import sqlite3
import datetime
import time
#import Employee
#from Employee import Employee
import newTC
from newTC import *

conn = sqlite3.connect('TCTest2.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
c = conn.cursor()

pins = []

def clockOutAll():
    emp = Employee.Employee()
    tc = newTC(emp)
    for row in c.execute('select pin, status from Employees'):
        pin = row[0]
        status = row[1]
        pins.append([pin, status])
     
    for a in pins:
        p = a[0]
        s = a[1]
        if s == 1:
            tc.set_pin(p)
            tc.in_or_out()
            print p
            
clockOutAll()



