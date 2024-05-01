from datetime import datetime, timedelta
import os

TODAY = datetime.today().strftime("%d_%m_%Y")
PATH = f"./timetrackerdata/{TODAY}.txt"
DIVIDER = "--> "


class Colors:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def print_error(error):
    print(f"{Colors.RED}{error}{Colors.RESET}")


def print_sucess(status):
    print(f"{Colors.GREEN}{status}{Colors.RESET}")


def print_question(status):
    print(f"{Colors.YELLOW}{status}{Colors.RESET}")


def time_difference(start_time, end_time):
    start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
    end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
    time_delta = end - start
    hours, minutes = divmod(time_delta.seconds // 60, 60)
    return f"{hours}h {minutes}min"


from datetime import datetime, timedelta


def track(type, last_timestamp_str):
    try:
        last_timestamp = datetime.strptime(last_timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError as e:
        print_error(f"Error parsing last_timestamp: {e}")
        return

    try:
        with open(PATH, "r") as f:
            file_content = f.read()
    except IOError as e:
        print_error(f"Error reading file: {e}")
        return

    if file_content and file_content[-1] == "\n":
        prefix = ""
    else:
        prefix = "\n"

    if type == "ticket":
        try:
            ticket_number = input("Ticket: \n")
            time_spend_input = input(
                "How much time to log? Press Enter for: "
                + time_difference(str(last_timestamp), str(datetime.now()))
            )

            if time_spend_input.strip():  # Check if time_spend_input is not empty
                time_spend_minutes = int(time_spend_input)
                time_difference_past = timedelta(minutes=time_spend_minutes)
                new_timestamp = last_timestamp + time_difference_past

                with open(PATH, "a") as f:
                    f.write(
                        f"{prefix} {type} {ticket_number} {DIVIDER} {new_timestamp}\n"
                    )
                print_sucess(f"added: {type} {ticket_number} {new_timestamp}")
            else:
                current_time = datetime.now()

                with open(PATH, "a") as f:
                    f.write(
                        f"{prefix} {type} {ticket_number} {DIVIDER} {current_time}\n"
                    )
                print_sucess(f"added: {type} {ticket_number} {current_time}")
        except Exception as e:
            print_error(f"An error occurred while processing ticket: {e}")

    elif type == "meeting":
        try:
            meeting_topic = input("Topic: \n")
            time_spend_input = input(
                "How much time to log? Press Enter for: "
                + time_difference(str(last_timestamp), str(datetime.now()))
            )

            if time_spend_input.strip():  # Check if time_spend_input is not empty
                time_spend_minutes = int(time_spend_input)
                time_difference_past = timedelta(minutes=time_spend_minutes)
                new_timestamp = last_timestamp + time_difference_past

                with open(PATH, "a") as f:
                    f.write(
                        f"{prefix}{type} {meeting_topic} {DIVIDER} {new_timestamp}\n"
                    )
                print_sucess(f"added: {type} {meeting_topic} {new_timestamp}")
            else:
                current_time = datetime.now()

                with open(PATH, "a") as f:
                    f.write(
                        f"{prefix}{type} {meeting_topic} {DIVIDER} {current_time}\n"
                    )
                print_sucess(f"added: {type} {meeting_topic} {current_time}")
        except Exception as e:
            print_error(f"An error occurred while processing meeting: {e}")


def output():
    with open(PATH, "r") as file:
        lines = file.readlines()

    for i in range(1, len(lines)):
        start_time = lines[i - 1].split(DIVIDER)[1].strip()
        end_time = lines[i].split(DIVIDER)[1].strip()
        time_diff = time_difference(start_time, end_time)
        print(f"{i}. {lines[i].split(DIVIDER)[0]} {time_diff}\n")


def start_tracking():
    user_input = input("start tracking now? " + str(datetime.now()) + "\n")
    if user_input == "":
        try:
            with open(PATH, "a") as f:
                f.write(f"start {DIVIDER} {datetime.now()}")
            print_sucess(f"timetracking started at: {str(datetime.now())}")
        except Exception as e:
            print_error(f"An error occurred while writing to the file: {e}")


def delete_last_line():
    if os.path.exists(PATH) and os.path.getsize(PATH) > 0:
        with open(PATH, "r+") as file:
            lines = file.readlines()
            if len(lines) > 0:
                file.seek(0)
                file.truncate()
                file.writelines(lines[:-1])
        print("Last entry deleted.")
    else:
        print("File is empty or does not exist.")


def main():
    if not os.path.exists(PATH):
        start_tracking()
    else:
        print("What do you want to track? \n")
        user_input = input(
            "\t[T]: Ticket\n\t[M]: Meeting\n\t[?]: Get tracked times\n\t[X]: Delete last entry\n"
        ).upper()
        if user_input == "T":
            with open(PATH, "r") as f:
                last_line = f.readlines()[-1]
                last_timestamp = last_line.split(DIVIDER)[1].strip()
            track("ticket", last_timestamp)
        elif user_input == "M":
            with open(PATH, "r") as f:
                last_line = f.readlines()[-1]
                last_timestamp = last_line.split(DIVIDER)[1].strip()
            track("meeting", last_timestamp)
        elif user_input == "?":
            output()
        elif user_input == "X":
            delete_last_line()
            print("Last entry deleted.")


if __name__ == "__main__":
    main()
