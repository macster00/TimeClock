import sqlite3
conn = sqlite3.connect('TCTest2.db')
c = conn.cursor()
conn.text_factory = str
emps = []
for row in c.execute('select * from Employees'):
    assert type(row[0]) is str
    fname = row[0]
    lname = row[1]
    pin = row[2]
    rid = row[3]
    if rid > 0:
        emps.append([pin, fname, lname])
    
for ids in emps:
    pin = ids[0]
    name = ids[1] + " " + ids[2]
    f = open("timelist.txt", 'w')
    f.write(name + "\n")
    f.write("     Time In                    Time Out             Today       Total\n")
    #f.write("\n")
    for row in c.execute('select * from times where pin=:pin', {"pin": pin}):
        assert type(row[1]) is str
        f.write(str(row[1][5:19]+ "\t" + row[2][5:19] + "\t" + str(("%.2f" % row[3])) + "\t" + str(("%.2f" % row[4])) + "\n"))
    f.write("\n")
    f.close()
    
