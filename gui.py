#updated 10/3
from Tkinter import *
import Tkinter as tk
import time
import datetime
import Queue

import Employee
from Employee import Employee
import newTC
from newTC import *
import mkTxt

time1 = ''

class clockView(tk.Frame):
    def __init__(self, master, model, control):
        #some shit
        self.master = master
        self.model = model
        self.control = control
        master.title("Time Clock")
        self.content = tk.Frame(self.master)
         
        #clock text
        self.clock = Label(self.content, font=('times', 300, 'bold'), bg='green')
        self.clock.pack(fill=BOTH, expand=1)
        
        #variable text for prompt label and welcome labels
        self.welcomeText = StringVar()
        self.promptText = StringVar()
        #set prompt to default
        self.promptText.set("Enter PIN")
        
        #build main window widgets
        self.prompt = Label(self.content, textvariable=self.promptText, font=('time', 50, 'bold'))
        self.welcomeLable = tk.Label(self.content, textvariable=self.welcomeText)
        
        self.entry = Entry(self.content, font=('times', 25))
        self.entry.config(justify = CENTER)

        #build admin buttons
        self.add = Button(self.content, text ="Add Employees", command=self.enterEmpData)
        self.quit = Button(self.content, text ="Exit Program", command=self.exitProgram)
        self.add.bind("<Return>", self.enterEmpData)
        #self.remove = Button(self.content, text = "Remove Employee", command = self.removeEmployee)
        #self.remove.bind("<Return>", self.removeEmployee)
        self.logoff = Button(self.content, text="Logout Admin", command=self.adminLogOut)
        self.lookup = Button(self.content, text="Search Employees", command=self.searchEmployee)
        self.change = Button(self.content, text="Update Employee Time", command=self.changeTimes)
                
        #place widgets
        self.content.grid()        
        self.prompt.pack(side = tk.TOP)
        self.welcomeLable.pack(side=tk.BOTTOM)
        self.entry.pack()
        self.entry.focus()
        
        #pressing enter calls getText
        self.entry.bind("<Return>", self.getText)
        #self.normal()
    
    def normal(self):
        self.clock.config(bg='green')
        self.promptText.set("Enter PIN")
        self.entry.pack()
        #self.entry.delete(0, 'end')
        #self.entry.focus()
        print "normal"
    
    # read/interpret the text
    def getText(self, *args):
        text = self.entry.get()
        
        if text == 'admin':
            self.entry.delete(0, 'end')
            self.enterPassword()
            return

        if self.control.check_pin(text) is False:
            self.clock.config(bg='red')
            self.promptText.set("")
            self.redclock()
            return
        elif self.control.pin_exists(text) is False:
            self.promptText.set("")
            self.redclock()
            return
        else:
            self.model.get_Employee(text)
            fname = self.model.get_firstName()
            lname = self.model.get_lastName()
            self.entry.delete(0, 'end')
            self.confirmLogin(fname, lname, text)
            return
            
    def enterPassword(self):
        self.password = Toplevel(self.master)
        self.password.title("Password")
        self.pwLabel = Label(self.password, text = "Enter Admin Password", font=('time', 30))
        self.pwEntry = Entry(self.password, font=('times', 25))
        self.pwLabel.pack()
        self.pwEntry.pack()
        self.pwEntry.config(show='*')
        self.pwEntry.focus()
        self.pwEntry.config(justify = CENTER)
        self.pwEntry.bind("<Return>", self.checkPassword)
        
    #--------------------------------------------------------------------------------------------------------------------------------------------
    def confirmLogin(self, fname, lname, pin):
        self.pin = pin
        self.confLog = Toplevel(self.master)
        self.confLog.title("Log In")
        #self.nameVar = StringVar()
        self.nameLabel = Label(self.confLog, text = fname + " " + lname, font=('time', 55))
        self.login = Button(self.confLog, text = "Log In/Out", font=('time', 30), command = self.logMeIn)
        self.cancel = Button(self.confLog, text = "Cancel", font=('time', 30), command = self.destroyConfLogin)
        self.nameLabel.pack()
        self.login.pack()
        self.login.focus()
        self.login.bind("<Return>", self.logMeIn)
        self.cancel.pack()
        
    def destroyConfLogin(self):
        self.confLog.destroy()
        
    def logMeIn(self, *args):
        statusIn = "You are clocked in"
        statusOut = "Your are clocked out. Goodbye!\n"
        self.control.in_or_out()
        
        if self.control.check_status() == 0:
            self.promptText.set(self.model.get_firstName() + " " + self.model.get_lastName()  + "\n" + statusIn)
            #self.showTimes()
        elif self.control.check_status() == 1:
            self.promptText.set(self.model.get_firstName() + " " + self.model.get_lastName()  + "\n" + statusOut + "Total Hours: " + str(self.myTotal()))
            self.showTimes()
             
        self.destroyConfLogin()
        self.greenclock()
       
    def myTotal(self):
        self.model.get_Employee(self.pin)
        total = self.model.get_total()
        return total
        
    def showTimes(self):
        self.destroyConfLogin()
        self.model.get_Employee(self.pin)
        self.showMyTimes = Toplevel(self.master)
        self.showMyTimes.title("Your Times")
        self.toExit = Label(self.showMyTimes, text="Press Enter To Print Your Time Sheet", font=('time', 50))
        self.timeMessage = Message(self.showMyTimes, text=self.control.print_hours(), font=('time', 15), width=1000)
        self.toExit.pack()
        self.timeMessage.pack()
        self.showMyTimes.focus()
        self.showMyTimes.bind("<Key>", self.destroyTimes)
        self.showMyTimes.after(20000, self.destroyTimes)

    def destroyTimes(self, *args):
        #self.confLog.destroy()
        
        #self.control.write_times()
        self.showMyTimes.destroy()
        
    def testEnter(self, *args):
        print "a;dflkas;dlfa;sdfj;lasdkjf"
        
    def checkPassword(self, *args):
        pword = self.pwEntry.get()
        if pword == "password":
            self.promptText.set("Admin Settings")
            self.entry.forget()
            self.add.pack()
            self.lookup.pack()
            self.change.pack()
            #self.remove.pack()
            self.logoff.pack()
            self.quit.pack()
            self.add.focus()
         
        else:
            self.redclock()
        self.password.destroy()
        

    def enterEmpData(self, *args):
        self.empData = Toplevel(self.master)
        self.empData.title("Admin Settings")
        self.fnLable = Label(self.empData, text="First Name", font=('time', 30))
        self.lnLable = Label(self.empData, text="Last Name", font=('time', 30))
        self.pnLable = Label(self.empData, text="PIN", font=('time', 30))
        
        self.fnEnter = Entry(self.empData, font=('times', 25))
        self.lnEnter = Entry(self.empData, font=('times', 25))
        self.pnEnter = Entry(self.empData, font=('times', 25))
        
        self.addButton = Button(self.empData, text=("Add Employee"), command = self.addEmployee)
        self.confirmButton = Button(self.empData, text=("Confirm"), command = self.confirmEmployee)
        self.clearButton = Button(self.empData, text=("Clear"), command = self.clearData)
        
        
        self.fnLable.pack()
        self.fnEnter.pack()
        self.lnLable.pack()
        self.lnEnter.pack()
        self.pnLable.pack()
        self.pnEnter.pack()
        self.addButton.pack()
        self.fnEnter.focus()

        
    def addEmployee(self, *args):
        pn = self.pnEnter.get()
        self.warning = Toplevel(self.master)
        self.warning.title("Error")
        self.warnText = StringVar()
        self.message = Label(self.warning, textvariable = self.warnText, font=('time', 25))
        self.ok = Button(self.warning, text=("Enter a new PIN"), command = self.destroywarning)
        self.ok.bind("<Return>", self.destroywarning)
        self.ok.focus()
        
        if self.control.check_pin(pn) is False:
            self.warnText.set("This PIN is may not be entered correctly")
            self.message.pack()
            self.ok.pack()
        elif self.control.pin_exists(pn) is True:
            self.warnText.set("This PIN is already taken")
            self.message.pack()
            self.ok.pack() 
        else:
            self.warning.destroy()
            self.addButton.forget()
            self.confirmButton.pack()
            self.clearButton.pack()

    def confirmEmployee(self):
        fname = self.fnEnter.get()
        lname = self.lnEnter.get()
        pin = self.pnEnter.get()
        self.control.add_new(fname, lname, pin)
        #self.confEmp = Toplevel(self.master)
        #self.confEmp.title("Confirm New Employee")
        #self.newEmpLable = Label(self.confEmp, text = (fname + " " + lname + "\n" + "PIN: " + pin), font=('time', 50))
        #self.newEmpButton = Button(self.confEmp, text = "Confirm", command = self.newEmployee(fn, ln, pn))
        #self.newEmpLable.pack()
        #self.newEmpButton.pack()
        self.clearData()

    def newEmployee(self):
        #fn = self.fnEnter.get()
        #ln = self.lnEnter.get()
        #pn = self.pnEnter.get()
        print fn, ln, pn
        self.control.add_new(fn, ln, pn)
        self.confEmp.destroy()
        
    def searchEmployee(self):
        self.empSearch = Toplevel(self.master)
        self.lookPrompt = Label(self.empSearch, text = "Enter PIN")
        self.query = Entry(self.empSearch, font=('times', 25))
        self.lookPrompt.pack()
        self.query.pack()
        self.query.config(justify = CENTER)
        self.query.focus()
        self.query.bind("<Return>", self.employeeSelect)
        
        #search = self.quere.get()
        #if(self.control.is_integer(search) is True):
        
    def changeTimes(self):
        self.enterTimes = Toplevel(self.master)
        self.enterTimes.title("Change Times")
        self.timeVar = IntVar()
        self.clockVar = IntVar()
        self.empPinLabel = Label(self.enterTimes, text="Employee PIN", font=('times', 20))
        self.hourLabel = Label(self.enterTimes, text="Hour", font=('times', 20))
        self.minLabel = Label(self.enterTimes, text="Minute", font=('times', 20))
        self.dayLabel = Label(self.enterTimes, text="Day", font=('times', 20))
        self.monthLabel = Label(self.enterTimes, text="Month", font=('times', 20))
        self.searchPin = Entry(self.enterTimes, font=('times', 20))
        self.hour = Entry(self.enterTimes, font=('times', 20))
        self.minute = Entry(self.enterTimes, font=('times', 20))
        self.day = Entry(self.enterTimes, font=('times', 20))
        self.month = Entry(self.enterTimes, font=('times', 20))
        self.am = Radiobutton(self.enterTimes, text="AM", variable=self.timeVar, value=0)
        self.pm = Radiobutton(self.enterTimes, text="PM", variable=self.timeVar, value=1)
        self.tIn = Radiobutton(self.enterTimes, text="Change Clock In Time", variable=self.clockVar, value=0)
        self.tOut = Radiobutton(self.enterTimes, text="Change Clock Out Time", variable=self.clockVar, value=1)
        self.updateButton = Button(self.enterTimes, text="Update", font=('times', 20), command=self.updateTimes)
        
        self.empPinLabel.pack()
        self.searchPin.pack()
        self.searchPin.config(justify=CENTER)
        self.hourLabel.pack()
        self.hour.pack()
        self.hour.config(justify=CENTER)
        self.minLabel.pack()
        self.minute.pack()
        self.minute.config(justify=CENTER)
        self.dayLabel.pack()
        self.day.pack()
        self.day.config(justify=CENTER)
        self.monthLabel.pack()
        self.month.pack()
        self.month.config(justify=CENTER)
        self.month.insert(0,"10")
        self.am.pack()
        self.pm.pack()
        self.tIn.pack()
        self.tOut.pack()
        self.updateButton.pack()
        
    def updateTimes(self):
        pin = self.searchPin.get()
        hour = self.hour.get()
        min = self.minute.get()
        day = self.day.get()
        month = self.month.get()
        time = self.timeVar.get()
        clock = self.clockVar.get()
        
        hour = self.formatTime(hour)
        min = self.formatTime(min)
        day = self.formatTime(day)
        month = self.formatTime(month)

        self.control.change_a_time(pin, month, day, hour, min, time, clock)
        #self.destroyChangeTimes()
        return
        
    def formatTime(self, time):
        if int(time) < 10:
            if len(time) < 2:
                time = "0" + str(time)
        return time
    
    def destroyChangeTimes(self):
        self.enterTimes.destroy()
        self.changeTimes()
    
    def employeeSelect(self, *args):
        search = self.query.get()
        if self.control.check_pin(search) is True:
            if self.control.pin_exists(search) is True:
                self.model.get_Employee(search)
                self.displayEmployee()
                #print self.model.fname + " " + self.model.lname + " " + str(self.model.total)
        else:
            self.query.delete(0, 'end')
            
    def displayEmployee(self):
        self.display = Toplevel(self.master)
        self.foundLabel = Label(self.display, text = (self.model.fname + " " + self.model.lname + "\n" + str(self.model.total) + " total hours"), font=('times', 25))
        self.foundLabel.pack()
        
    def clearData(self):
        self.empData.destroy()
        self.enterEmpData()
   
    def removeEmployee(self):
        print "test"
        #enter pin and confirm/remove employee from db
    
    def adminLogOut(self):
        self.add.forget()
        #self.remove.forget()
        self.logoff.forget()
        self.quit.forget()
        self.lookup.forget()
        self.change.forget()
        self.entry.delete(0, 'end')
        self.normal()
    
    def destroywarning(self, *args):
        self.pnEnter.delete(0, 'end')
        self.warning.destroy()

        
    def redclock(self):
        self.entry.delete(0, 'end')
        self.clock.config(bg = 'red')
        self.clock.after(1500, self.normal)
        
    def greenclock(self):
        self.entry.delete(0, 'end')
        self.clock.config(bg = 'green')
        self.clock.after(1500, self.normal)

    #this is the clock at the top
    def tick(self):
        global time1
        time2 = time.strftime('%I:%M:%S')
        
        if time2 != time1:
            time1 = time2
            self.clock.config(text=time2)
        
        self.clock.after(200, self.tick)
        
    def exitProgram(self):
        self.master.destroy()
   

def main():
    model = Employee.Employee()
    root = tk.Tk()
    #control = TimeClock(model)
    control = newTC(model)
    app = clockView(root, model, control)
    app.tick()
    #root.attributes('-fullscreen', True)
    root.mainloop()
    #app.start()


main()
