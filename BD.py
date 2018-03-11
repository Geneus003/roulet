import sqlite3

db = sqlite3.connect("test.db")

cursorTask = db.execute("SELECT position,red,black,green, id from TASK")

for row in cursorTask:
    print(row[0],":",row[1],":", row[2],":", row[3],":", row[4])


db.close()