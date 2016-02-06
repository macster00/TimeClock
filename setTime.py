from Tkinter import *
import Tkinter as tk
import time
time1 = ''

class updateTime(tk.Frame):
    def __init__(self, master):
        self.master = master
        master.title("Set Clock")
        self.content = tk.Frame(self.master)
        
        self.clock = Label(self.content, font=('times', 25, 'bold'))
        self.clock.pack(fill=BOTH, expand=1)
        
        self.datePt = Label(self.content, text="Enter the Date (DD-MM-YYYY)", font=('times', 25, 'bold'))
        self.timePt = Label(self.content, text="Enter the Time (HH:MM)", font=('times', 25, 'bold'))
        
        self.dateEt = Entry(self.content, font=('times', 25))
        self.dateEt.config(justify = CENTER)
        self.timeEt = Entry(self.content, font=('times', 25))
        self.timeEt.config(justify = CENTER)
        self.timeEt.bind("<Return>", self.changeTime)
        
        self.variable = StringVar(master)
        self.variable.set("Sunday") # default value

        self.w = OptionMenu(self.master, self.variable, "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
               
        self.datePt.pack()
        self.dateEt.pack()
        self.w.pack(side=tk.BOTTOM)
        self.timePt.pack()
        self.timeEt.pack()
        self.content.pack()
        self.dateEt.focus()
        
    def changeTime(self, *args):
        date = self.dateEt.get()
        time = self.timeEt.get()
        DoW = self.variable.get()[:3] #possible exception for thursday
        
        day = date[:2]
        month = date[3:5]
        year = date[6:10]
        
        
        #print DoW + " " + date + " " + time
        print day, month, year, DoW
        
        
    def tick(self):
        global time1
        time2 = time.strftime('%I:%M:%S')
        
        if time2 != time1:
            time1 = time2
            self.clock.config(text=time2)
        
        self.clock.after(200, self.tick)
    
        
def main():
    root = tk.Tk()
    app = updateTime(root)
    app.tick()

    root.mainloop()
    
main()