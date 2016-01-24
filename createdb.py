import sqlite3
conn = sqlite3.connect('TCTest1.db')
c = conn.cursor()
# first name, last name, PIN, Row id number
c.execute('CREATE TABLE Employees(fname text, lname text, pin integer, rid integer, status boolean)')
# PIN, clock in time, clockout time, total hours
c.execute('CREATE TABLE Times(pin integer, timeIn timestamp, timeOut timestamp, today integer, hours integer)')

# Im inserting None into the row id spot. It will be updated when the employee clocks in

#c.execute("insert into employees values('Don', 'McAlister', '1111', '0')")
#c.execute("INSERT INTO employees VALUES('Amy', 'McAlister', '2222', '0')")
#c.execute("INSERT INTO employees VALUES('Lewis', 'McAlister', '3333', '0')")
#c.execute("INSERT INTO employees VALUES('David', 'McAlister', '4444', '0')")
conn.commit()