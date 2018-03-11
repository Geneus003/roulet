from selenium import webdriver
import datetime, time, sys
import os.path
import sqlite3


def createDB():
    rouletDB = sqlite3.connect('test.db')
    rouletDB.execute('''CREATE TABLE TASK
                    (POSITION         TEXT    NOT NULL,
                    RED           INT     NOT NULL,
                    BLACK       INT    NOT NULL,
                    GREEN       INT    NOT NULL,
                    ID           INT    NOT NULL);''''')
    rouletBD.close()


def createNewRow(prev_game,red, green, black):
    rouletDB = sqlite3.connect("test.db")

    lastIDTaskOpen = open("taskID.txt")
    lastIDTask = lastIDTaskOpen.read()
    lastIDTask = int(lastIDTask)
    lastIDTaskOpen.close()

    idtask = lastIDTask + 1
    lastIDTask += 1

    lastIDTaskStr = str(lastIDTask)

    lastIDTaskOpen = open("taskID.txt", "w")
    lastIDTaskOpen.write(lastIDTaskStr)
    lastIDTaskOpen.close()

    rouletDB = sqlite3.connect('test.db')

    if red == True:
        params = (prev_game,1,0,0, idtask)
    if black == True:
        params = (prev_game, 0, 1, 0, idtask)
    if green == True:
        params = (prev_game, 0, 0, 1, idtask)

    print(params)

    rouletDB.execute("INSERT INTO TASk VALUES (?, ?, ?, ?, ?)", params)

    rouletDB.commit()
    rouletDB.close()


def findElementById(prev_game):
    rouletDB = sqlite3.connect("test.db")

    cursorTask = rouletDB.execute("SELECT position, id from TASK")

    for row in cursorTask:
        if prev_game == row[0]:
            rouletDB.close()
            return row[1]

    rouletDB.close()
    return False


def appendIt(nowIdm,prev_game,red,black,green):
    rouletDB = sqlite3.connect('test.db')

    if red == True:
        cursorTask = rouletDB.execute("SELECT red, id from TASK")

        for row in cursorTask:
            if nowIdm == row[1]:
                params = (row[0]+1, nowIdm)

        rouletDB.execute("UPDATE TASK set RED = ? where ID= ?", params)
    if black == True:

        cursorTask = rouletDB.execute("SELECT black, id from TASK")

        for row in cursorTask:
            if nowIdm == row[1]:
                params = (row[0]+1, nowIdm)

        rouletDB.execute("UPDATE TASK set BLACK = ? where ID= ?", params)
    if green == True:
        cursorTask = rouletDB.execute("SELECT green, id from TASK")

        for row in cursorTask:
            if nowIdm == row[1]:
                params = (row[0]+1, nowIdm)


        rouletDB.execute("UPDATE TASK set GREEN = ? where ID= ?", params)


    rouletDB.commit()
    rouletDB.close()


if os.path.isfile('test.db') == False:
    createDB()


prev_game = ""
mas_chisel = []
i = 0
while True:
    driver = webdriver.PhantomJS()
    driver.get("https://www.csgostrong.com/")
    last_game = driver.find_element_by_class_name("previous-numbers-block-wrap")

    last_game = last_game.text

    driver.close()

    if last_game == prev_game:
        continue
    else:
        if i == 0:
            prev_game = last_game


        if last_game[19] == " ":
            new_int = int(last_game[18])
        else:
            new_int = int(last_game[18] + last_game[19])

        print(new_int, last_game)

        green = False
        red = False
        black = False
        if new_int == 0:
            green = True
        elif new_int <= 7:
            red = True
        elif new_int >= 8:
            black = True

        if findElementById(prev_game) == False:
            createNewRow(prev_game,red,green,black)
        else:
            appendIt(findElementById(prev_game),prev_game,red,black,green)

        prev_game = last_game
        i = 1
        time.sleep(5)




