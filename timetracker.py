from datetime import datetime, timedelta
import os


class TimeTracker:
    def __init__(self):
        self.today = datetime.today().strftime("%d_%m_%Y")
        self.path = f"./timetrackerdata/{self.today}.txt"
        self.divider = "--> "

    def print_error(self, error):
        print(f"\033[31m{error}\033[0m")

    def print_success(self, status):
        print(f"\033[32m{status}\033[0m")

    def print_status(self, status):
        print(f"\033[33m{status}\033[0m")

    def print_message(self, status):
        print(f"\033[35m{status}\033[0m")

    def print_user_input_message(self, message):
        return input(f"\033[36m{message}\033[0m")

    def time_difference(self, start_time, end_time):
        start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
        end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
        time_delta = end - start
        hours, minutes = divmod(time_delta.seconds // 60, 60)
        return f"{hours}h {minutes}min"

    def parse_timestamp(self, last_timestamp_str):
        try:
            return datetime.strptime(last_timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError as e:
            self.print_error(f"Error parsing last_timestamp: {e}")
            return None

    def read_file_content(self, file_path):
        try:
            with open(file_path, "r") as f:
                return f.read()
        except IOError as e:
            self.print_error(f"Error reading file: {e}")
            return None

    def determine_prefix(self, file_content):
        return "" if file_content and file_content[-1] == "\n" else "\n"

    def process_ticket(self, last_timestamp, prefix):
        try:
            ticket_number = self.print_user_input_message("Ticket: \n")
            time_spend_input = self.print_user_input_message(
                "How much time to log? Press Enter for: "
                + self.time_difference(str(last_timestamp), str(datetime.now()))
            )

            if time_spend_input.strip():
                time_spend_minutes = int(time_spend_input)
                time_difference_past = timedelta(minutes=time_spend_minutes)
                new_timestamp = last_timestamp + time_difference_past
            else:
                new_timestamp = datetime.now()

            with open(self.path, "a") as f:
                f.write(
                    f"{prefix} ticket {ticket_number} {self.divider} {new_timestamp}\n"
                )
            self.print_success(f"Added: ticket {ticket_number} {new_timestamp}")
        except Exception as e:
            self.print_error(f"An error occurred while processing ticket: {e}")

    def process_meeting(self, last_timestamp, prefix):
        try:
            meeting_topic = self.print_user_input_message("Topic: \n")
            time_spend_input = self.print_user_input_message(
                "How much time to log? Press Enter for: "
                + self.time_difference(str(last_timestamp), str(datetime.now()))
            )

            if time_spend_input.strip():
                time_spend_minutes = int(time_spend_input)
                time_difference_past = timedelta(minutes=time_spend_minutes)
                new_timestamp = last_timestamp + time_difference_past
            else:
                new_timestamp = datetime.now()

            with open(self.path, "a") as f:
                f.write(
                    f"{prefix} meeting {meeting_topic} {self.divider} {new_timestamp}\n"
                )
            self.print_success(f"Added: meeting {meeting_topic} {new_timestamp}")
        except Exception as e:
            self.print_error(f"An error occurred while processing meeting: {e}")

    def track(self, type, last_timestamp_str):
        last_timestamp = self.parse_timestamp(last_timestamp_str)
        if last_timestamp is None:
            return

        file_content = self.read_file_content(self.path)
        prefix = self.determine_prefix(file_content)

        if type == "ticket":
            self.process_ticket(last_timestamp, prefix)
        elif type == "meeting":
            self.process_meeting(last_timestamp, prefix)
        else:
            self.print_error("Invalid type provided.")

    def output(self):
        try:
            with open(self.path, "r") as file:
                lines = file.readlines()
        except IOError as e:
            self.print_error(f"Error reading file: {e}")
            return

        for i in range(1, len(lines)):
            try:
                start_time = lines[i - 1].split(self.divider)[1].strip()
                end_time = lines[i].split(self.divider)[1].strip()
                time_diff = self.time_difference(start_time, end_time)
                self.print_status(
                    f"{i}. {lines[i].split(self.divider)[0]} {time_diff}\n"
                )
            except IndexError as e:
                self.print_error(f"Error parsing line {i}: {e}")
            except ValueError as e:
                self.print_error(f"Error converting time: {e}")
            except Exception as e:
                self.print_error(f"An unexpected error occurred: {e}")

    def start_tracking(self):
        try:
            user_input = self.print_user_input_message(
                "Enter number of minutes to start tracking from now: "
            )
            if user_input.isdigit():
                minutes = int(user_input)
                start_time = datetime.now() - timedelta(minutes=minutes)
            else:
                start_time = datetime.now()

            with open(self.path, "a") as f:
                f.write(f"start {self.divider} {start_time}")
            self.print_success(f"Timetracking started at: {start_time}")
        except Exception as e:
            self.print_error(f"An error occurred while writing to the file: {e}")

    def delete_last_line(self):
        try:
            if os.path.exists(self.path) and os.path.getsize(self.path) > 0:
                with open(self.path, "r+") as file:
                    lines = file.readlines()
                    if len(lines) > 0:
                        file.seek(0)
                        file.truncate()
                        file.writelines(lines[:-1])
                self.print_message("Last entry deleted.")
            else:
                print("File is empty or does not exist.")
        except Exception as e:
            self.print_error(f"An unexpected error occurred: {e}")

    def main(self):
        if not os.path.exists(self.path):
            self.start_tracking()
        else:
            self.print_message("What do you want to track? \n")
            user_input = self.print_user_input_message(
                "\t[T]: Ticket\n\t[M]: Meeting\n\t[?]: Get tracked times\n\t[X]: Delete last entry\n"
            ).upper()
            action_mapping = {
                "T": lambda: self.track("ticket", self.get_last_timestamp()),
                "M": lambda: self.track("meeting", self.get_last_timestamp()),
                "?": self.output,
                "X": self.delete_last_line,
            }
            action = action_mapping.get(user_input)
            if action:
                action()

    def get_last_timestamp(self):
        try:
            with open(self.path, "r") as f:
                last_line = f.readlines()[-1]
                return last_line.split(self.divider)[1].strip()
        except Exception as e:
            self.print_error(f"An error occurred while getting last timestamp: {e}")
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


if __name__ == "__main__":
    tracker = TimeTracker()
    tracker.main()
