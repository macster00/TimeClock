import sqlite3
import datetime
import time

conn = sqlite3.connect('TCTest1.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
c = conn.cursor()

pins = []

def enter_pin():
        pin = int(raw_input("Enter your 4 digit PIN: "))
        get_times(pin)
    
def get_rids():
    for row in c.execute('select pin, status from Employees'):
        pin = row[0]
        status = row[1]
        pins.append([pin, status])
     
    for a in pins:
        p = a[0]
        s = a[1]
        if s == 1:
            print p


#enter_pin()
#get_rids() 

#change_clockin()      
#get_times()
get_rids()
#update()    


