from datetime import date
from datetime import datetime

today = date.today().strftime("%d_%m_%Y")
path = "./timetrackerdata/" + today + ".txt"

f = open(path, "a")
f = open(path, "r")
content = f.read()
if content == "":
    input = input("start tracking now? " + str(datetime.now()) + "\n")
    if input == "Y":
        f = open(path, "a")
        f.write("start --> " + str(datetime.now()))
f = open(path, "r")
print(f.read())
