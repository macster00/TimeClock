import sqlite3

#conn = sqlite3.connect('CF_Employees.db')
conn = sqlite3.connect('TCTest1.db')
c = conn.cursor()

c.execute("update Employees set rid=0")
c.execute('drop table Times')
c.execute('create table Times(pin integer, timeIn timestamp, timeOut timestamp, today integer, hours integer)')

conn.commit()