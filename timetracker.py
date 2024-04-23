from datetime import date

today = date.today().strftime("%d_%m_%Y")

f = open("./timetrackerdata/" + today + ".txt", "w")
