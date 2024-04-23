from datetime import date
from datetime import datetime

today = date.today().strftime("%d_%m_%Y")
path = "./timetrackerdata/" + today + ".txt"
divider = "--> "

f = open(path, "a")


def time_difference(start_timestamp):
    # Convert the start timestamp to a datetime object
    start_time = datetime.strptime(start_timestamp, "%Y-%m-%d %H:%M:%S.%f")

    # Get the current timestamp
    current_time = datetime.now()

    # Calculate the difference
    time_difference = current_time - start_time

    # Calculate hours and minutes
    hours = time_difference.seconds // 3600
    minutes = (time_difference.seconds % 3600) // 60

    return f"{hours}h {minutes}min"


def track(type):
    last_timestamp = ""
    with open(path, "r") as f:
        last_line = f.readlines()[-1]
        last_timestamp = last_line[last_line.find(divider) + len(divider) :]
    if type == "ticket":
        ticket_number = input("Ticket: \n")
        time_spend_input = input(
            "How much time to log? Press Enter for: " + time_difference(last_timestamp)
        )
        if time_spend_input == "":
            f = open(path, "a")
            f.write(
                "\n" + type + " " + ticket_number + " " + divider + str(datetime.now())
            )
            print("added: " + type + " " + ticket_number + " " + str(datetime.now()))
    if type == "meeting":
        meeting_topic = input("Topic: \n")


f = open(path, "r")
content = f.read()
if content == "":
    user_input = input("start tracking now? " + str(datetime.now()) + "\n")
    if user_input == "Y":
        f = open(path, "a")
        f.write("start " + divider + str(datetime.now()))
else:
    print("What do you want to track? \n")
    user_input = input(
        "\t[T]: Ticket\n\t[M]: Meeting\n\t[?]: Get tracked times\n\t[X]: End day\n"
    )
    if user_input == "T":
        track("ticket")
    elif user_input == "M":
        track("meeting")
    elif user_input == "?":
        output()
    elif user_input == "X":
        endDay()
f = open(path, "r")
print(f.read())
