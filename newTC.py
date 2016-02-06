#updated 10/3
import os
import time
import shutil
import datetime
import numpy as np
import sys

#sys.path.insert(1, '/usr/local/lib/python2.7/site-packages')


import cv2
#camera_port = 0
#ramp_frames = 30
#camera = cv2.VideoCapture(0)

import sqlite3
conn = sqlite3.connect('TCTest2.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
#CF_Employees
c = conn.cursor()

import Employee

class newTC:
    def __init__(self, emp):
        self.emp = emp 

    def set_pin(self, pin):
        self.emp.get_Employee(pin)

    # get the current system time
    def get_time(self):
        now = datetime.datetime.now()
        return now
        
    # calculate and return the number of hours worked today
    def time_worked(self, cIn):
        cOut = self.get_time()
        #now = cOut
        #print type(cIn)
        #calculate time worked
        #cOut = self.emp.get_timeOut()
        #cIn = self.emp.get_timeIn()
        
        secs = (cOut-cIn).total_seconds()

        hours = round((secs)/3600, 2)
        hours = secs
        #hours = 1
        return hours      
        
    #takes the picture
    def get_image(self, camera):
        ret, im = camera.read()
        return im

    #code works fine without a camera, but it will open/save a window of colored bars
    def take_picture(self):
        ramp_frames = 15
        camera = cv2.VideoCapture(0)
        fname = self.emp.get_firstName()
        lname = self.emp.get_lastName()
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        for i in xrange(ramp_frames):
            temp = self.get_image(camera)

        picture = self.get_image(camera)
        cv2.imshow('pic', picture)
        folder = "pictures/" + fname + " " + lname
        file = fname + "_" + lname + " " + date + ".png"
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        cv2.imwrite(file, picture)
        shutil.move(file, folder)
        
        
        #cv2.imshow('pic', picture)
        #cv2.waitKey(1000)
        #cv2.destroyAllWindows()


        camera.release()
        #cv2.VideoCapture.release()
        cv2.destroyAllWindows()

    #determines whether employee is clocking in or clocking out by comparing the in/out times   
    def in_or_out(self):
        r = self.emp.get_rid()
        hours = self.emp.get_total()
        status = self.emp.get_status()
        tin = self.emp.get_timeIn()
        tout = self.emp.get_timeOut()
        # if r == 0:
            # print "Clocking in first time"
            # self.clock_in(0)
            # return
        # if tin == tout:
            # print "Clocking out"
            # self.clock_out()
        # else:
            # print "clocking in"
            # self.clock_in(hours)
            
        if r == 0:
            print "Clocking in first time"
            self.clock_in(0)
            return
        if status == 1:
            print "Clocking out"
            self.clock_out()
        else:
            print "clocking in"
            self.clock_in(hours)
        
    # gets user PIN and current system time and inserts these values in to the Times table
    # inserts current time as a place holder for clock out time
    def clock_in(self, hours):
        now = self.get_time()
        uId = self.emp.get_pin()
        # inserts None in timeIn and total hours slots. these will be updated later
        c.execute("INSERT INTO Times VALUES(?, ?, ?, ?, ?)",(uId, now, now, 0, hours))
        
        id = c.lastrowid
        c.execute("UPDATE Employees SET rid=?, status=? WHERE pin=?", (id, 1, uId))
        conn.commit()
        
        self.take_picture()
        print "you are clocked in"
        
        
                
    def clock_out(self):
        uId = self.emp.get_pin()
        now = self.get_time()
        
        rId = self.emp.get_rid()
        c.execute('select timeIn, hours from Times where rowid=:rId', {"rId": rId})
        row = c.fetchone()
        cIn = row[0]
        
        hours = self.time_worked(cIn)
        #now = self.get_time()
        #self.emp.set_timeOut(now)
        #hours = self.time_worked()
        
        print "You worked " + str(hours) + " hours today"
        if row[1] is None: #first time clocking in
            total = hours
        else:
            total = hours + row[1] #add today's hours to the total

        c.execute("UPDATE Times SET timeOut=?, today=?, hours=? WHERE rowid=?", (now, hours, total, rId))
        c.execute("UPDATE Employees SET status=? WHERE pin=?", (0, uId))
        conn.commit()
        
        print "you have worked " + str(total) + " hours total"
        self.take_picture()
        print "you are now clocked out. goodbye"
         
        
    def remove_employee(self):
        pin = self.emp.get_pin()
        #rid = self.emp.get_rid()
        c.execute('delete * from Employees where pin=:pin', {"pin": pin})
        ##c.execute('delete from Times where pin=:pin', {"rid: rid})                ##Add employee pin to Times     necessary?
        conn.commit()
        
    #returns true if pin is a 4 digit integer
    def check_pin(self, pin):
        #check if pin is an integer
        if self.is_int(pin) is False:
            print "is not integer"
            return False
        #check if pin is 4 digits
        if (len(str(pin)) != 4):
            print "is not 4 digits"
            return False
        
        return True
        
    #test if input is an integer    
    def is_int(self, input):
        try:
            int(input)
            return True
        except ValueError:
            return False        
        
    #returns true if pin already exists or false if it is not yet taken
    def pin_exists(self, pin):
        #c.execute('select pin from Employees where pin=:pin', {"pin": pin})
        #conn.commit
        #check if pin exists    
        #exist = c.fetchone() 
        self.emp.get_Employee(pin)
        exist = self.emp.get_pin()
        if exist is None:
            return False
        else:
            #print "is taken"
            return True
       
    def check_status(self):
        return self.emp.get_status()
        

    def add_new(self, first, last, pin):
        c.execute("insert into Employees values(?, ?, ?, ?, ?)",(first, last, pin, 0, 0))
        conn.commit()
        #elf.emp.get_Employee(pin)
        #self.in_or_out()
        #self.clock_out()
            
    def enter_pin(self):
        while True:
            while True:
            #check if pin is integer
                try:
                    pin = int(raw_input("Enter your 4 digit PIN: "))
                    break
                except ValueError:
                    print "try again"             
            #check if pin is 4 digits
            if(len(str(pin)) == 4):
                if self.pin_exists(pin) is True:
                    self.emp.set_pin(pin)
                    return pin
                else:
                    print "PIN does not exist"
            else:
                print "The PIN must be 4 digits"

    def change_a_time(self, pin, month, day, hour, min, timeVar, clockVar):   
        self.emp.get_Employee(pin)
        rid = self.emp.get_rid()
        #today = self.emp.get_today()
        #total = self.emp.get_total()
        
        if int(timeVar) == 1:   # 0 = AM, 1 = PM
            if int(hour) < 12:
                hour = int(hour) + 12
        else:
            if int(hour) == 12:
                hour = "00"
         
        
        time="2015-{}-{} {}:{}:00.000001".format(month, day, hour, min)
        new = datetime.datetime.strptime(time,  "%Y-%m-%d %H:%M:%S.%f")
        
        
        
        if int(clockVar) == 0:  # 0 = Clockin, 1 = Clockout
            print "change clock in time"
            #self.emp.set_timeIn(new)
            #self.time_worked()
            c.execute('update Times set timeIn=? where rowid=?', (new, rid))
        else:
            print "change clock out time"
            #self.emp.set_timeOut(new)
            c.execute('update Times set timeOut=? where rowid=?', (new, rid))
            
        #hours = self.get_time()
        #total 
        
        conn.commit()
        print time
        
        self.update_hours(pin)
        return
        
    def update_hours(self, pin):
        staff = []
        #pin = 1111
        total = 0
        for row in c.execute('select rowid, timeIn, timeOut from Times where pin=:pin', {"pin": pin}):
            rowid = row[0]
            cin = row[1]
            cout = row[2]
            #total = row[2]
            #pin = row[3]
            
            
            secs = (cout-cin).total_seconds()
            hours = secs
            #hours = round((secs)/3600, 2)
            #if total == hours:
                #total = total
            #else:
                #total += hours
            total += hours    
            print cin, cout, hours, total
            staff.append([rowid, total, hours])
                
        for ids in staff:
            #pin = ids[0]
            rowid = ids[0]
            total = ids[1]
            hours = ids[2]
            #print pin, hours
            c.execute('update Times set today=?, hours=? where rowid=?', (hours, total, rowid))          
       
        conn.commit()
        
    def print_hours(self):
        emps = []
        printed = "Time In\t\tTimeOut\t\tDaily\tTotal\n"
        pin = self.emp.get_pin()
        for row in c.execute('select timeIn, timeOut, today, hours from Times where pin=?', (str(pin),)):
            tIn = row[0]
            tOut = row[1]
            today = row[2]
            total = row[3]
        
            emps.append([tIn, tOut, today, total])
        
        for ids in emps:
            i = ids[0]
            o = ids[1]
            tod = ids[2]
            tot = ids[3]
            printed += str(i.strftime("%Y-%m-%d %H:%M:%S")[5:19]+ "\t" + o.strftime("%Y-%m-%d %H:%M:%S")[5:19] + "\t" + str(tod) + "\t" + str(tot) + "\n")
    
        return printed

def main():
    emp = Employee.Employee()
    tc = newTC(emp)
    test = tc.enter_pin()
    tc.update_hours(1111)
    #emp.get_Employee(test)
    #tc.get_hours()
    #tempPin = tc.enter_pin();
    
    #tc.printTime()
    #tc.in_or_out()
    #emp.get_Employee(test)
    #a = tc.enter_pin()
    #tc.check_status()
    #tc.clock_in()
    #hours = tc.time_worked()
    #print hours

#main()