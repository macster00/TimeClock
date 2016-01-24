#updated 10/3
import sqlite3
conn = sqlite3.connect('TCTest2.db')
c = conn.cursor()

class Employee:
    # arguments are None until updated by the get_Employee function
    def __init__(self):
        self.fname = None
        self.lname = None
        self.pin = None
        self.rid = None
        self.status = None
        
        self.timeIn = None
        self.timeOut = None
        self.today = None
        self.total = None
    
    # receives a pin, reads in all additional data from employees table and assigns them to global variables
    def get_Employee(self, pin):
        #conn.text_factory = str
        c.execute('select * from Employees where pin=:pin', {"pin": str(pin)})
        row = c.fetchone()

        #  assert type(row[0]) is str
        if row is None:
            self.pin = None
            return
        else:
        #assert type(row[0]) is str
            self.fname = row[0]
            self.lname = row[1]
            self.pin = row[2]
            self.rid = row[3]
            self.status = row[4]
            self.get_Times()
        return
        
    # Getters/Setters    
    
    # From Employees
    def get_firstName(self):
        return self.fname
    def set_firstName(self, fname):
        self.fname = fname
    
    def get_lastName(self):
        return self.lname
    def set_lastName(self, lname):
        self.lname = lname
        
    def get_pin(self):
        return self.pin
    def set_pin(self, pin):
        self.pin = pin
        self.get_Employee(pin)
        
    def get_rid(self):
        return self.rid
    def set_rid(self, rid):
        self.rid = rid
        
    def get_status(self):
        return self.status
    def set_status(self, status):
        self.status = status    
        
    # From Times
    def get_timeIn(self):
        return self.timeIn
    def set_timeIn(self, timeIn):
        self.timeIn = timeIn
        
    def get_timeOut(self):
        return self.timeOut
    def set_timeOut(self, timeOut):
        self.timeOut = timeOut  
        
    def get_today(self):
        return self.today
    def set_totay(self, today):
        self.today = today
        
    def get_total(self):
        return self.total
    def set_total(self, total):
        self.total = total
       
    def get_Times(self):
        #conn.text_factory = str
        rid = self.rid
        c.execute('select * from Times where rowid=:rid', {"rid": rid})
        row = c.fetchone()
        
        if row is None:
            return
        else:         
        #assert type(row[0]) is str
        #pin = row[0]
            self.timeIn = row[1]
            self.timeOut = row[2]
            self.today = row[3]
            self.total = row[4]
        return
        
#def main():
    #a = Employee()
    #a.get_Employee(1111)
    #a.get_Times()
    
#main()