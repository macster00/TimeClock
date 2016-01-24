import sqlite3
import datetime
import time

conn = sqlite3.connect('TCTest1.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
c = conn.cursor()

clockedin = datetime.datetime.strptime("2015-10-23 18:45:00.000001",  "%Y-%m-%d %H:%M:%S.%f")

table = []
pins = []
rids = []
pin = 7
rid = 86

def enter_pin():
        pin = int(raw_input("Enter your 4 digit PIN: "))
        get_times(pin)
    
def change_clockin():
    c.execute('update Times set timeIn=? where rowid=?', (clockedin, rid))
    conn.commit()


def get_rids():
    for row in c.execute('select pin from Employees'):
        p = row[0]
        pins.append([p])
     
    for a in pins:
        b = a[0]
        for e in c.execute('select rowid from Times where pin=?', (b,)):
            f = e[0]
            rids.append([b, f])
    print rids
def get_times():
    for row in c.execute('select timeIn, timeOut, rowid from Times where pin=?', (pin,)):
        cin = row[0]
        cout = row[1]
        #total = row[2]
        rid = row[2]
            
        table.append([cin, cout, rid])
        #print table

def update():
    number = 0
    for ids in table:
        inc = ids[0]
        out = ids[1]
        ri = ids[2]
        
        secs = (out-inc).total_seconds()
        hours = round((secs)/3600, 2)
        hours = ("%.2f" % hours)
        number += float(hours)    
        c.execute("update Times set timeIn=?, timeOut=?, today=?, hours=? where rowid=?",(inc, out, hours, number, ri))
        conn.commit()
        print ri, str(inc)[5:19], str(out)[5:19], hours, number
        #print type(hours), type(number)

        
#enter_pin()
#get_rids() 

change_clockin()      
get_times()
update()    















#print table    
#c.execute('delete from Times where pin=?', (pin,))
#conn.commit()

#c.execute('insert into times values(?, ?, ?, ?, ?)', (pin, clockedin, cout, hours, hours))

#conn.commit()

#c.execute('select timein from Times where pin=?', (pin,))
#row = c.fetchone()
#c = row[0]

#print c



#c.execute("update Times set timeIn=? where pin=?",(then, pin))
#counter = 0
#staff = []
#for row in c.execute('select timeIn, timeOut, pin from Times'):
    #cin = row[0]
    #cout = row[1]
    #pin = row[2]
    #secs = (cout-cin).total_seconds()
    #hours = round((secs)/3600, 2)
    #print type(hours)
    #c.execute('update Times set today=? where pin=?',(hours, pin))
    #staff.append([pin, hours])

#for ids in staff:
    #pin = ids[0]
    #hours = ids[1]
    #print pin, hours
    #print type(hours)
    #c.execute('update Times set today=?, hours=? where pin=?', (hours, hours, pin))
    
#c.execute('select pin from Employees where fname=?', ("Jay",))
#row = c.fetchone()
#pin = str(row[0])
#print pin
#hours = 5.6
#pin = 0001
#c.execute('update Times set today=?, hours=? where pin=?', (hours, hours, pin))
#conn.commit()

#print row[0]