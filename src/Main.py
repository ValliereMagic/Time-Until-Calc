# time libraries
from datetime import datetime, timedelta, time

# types
from typing import Union

# command line arguments
from argparse import ArgumentParser, Namespace


# grab CLI argument, parse into a time delta, calculate the time in that amount of time
# and print it out.
def main():

    arg_parser: ArgumentParser = ArgumentParser(description="Time until, and from calculation tool")

    arg_parser.add_argument('-t_f', dest="user_time_from", help="Specify the amount of time "
                                                                "in the format HH:MM:SS "
                                                                "to calculate what time it will be "
                                                                " at the time specified, from now.")

    arg_parser.add_argument('-t_u', dest="user_time_until", help="Specify the time in the format "
                                                                 "HH:MM:SS military time tomorrow "
                                                                 "to calculate the amount of time "
                                                                 "between then and now.")
    # retrieve user time string from argument parser
    parsed_args: Namespace = arg_parser.parse_args()

    # execute the option the user specified
    time_from: str = parsed_args.user_time_from
    time_until: str = parsed_args.user_time_until

    if time_from is not None:
        # parse the user provided into a timedelta
        parsed_user_time: Union[timedelta, None] = parse_input_time(time_from)

        # execute the action specified by the user
        execution_success: bool = calculate_time_from(parsed_user_time)

        # if the action fails, display the help message
        if not execution_success:
            arg_parser.print_help()

    elif time_until is not None:
        parsed_user_time: Union[timedelta, None] = parse_input_time(time_until)

        execution_success: bool = calculate_time_until(parsed_user_time)

        if not execution_success:
            arg_parser.print_help()


def calculate_time_from(user_time_arg: timedelta) -> bool:

    if user_time_arg is not None:
        # get the current time
        current_time: datetime = datetime.now()

        # calculate requested time
        print("Time " + str(user_time_arg) + " from now: " + str((current_time + user_time_arg).time()
                                                                 .strftime("%I:%M:%S %p")))
        return True

    return False


def calculate_time_until(user_time_arg: timedelta) -> bool:
    if user_time_arg is not None:

        right_now = datetime.now()
        tomorrow_midnight: datetime = datetime.combine(datetime.today().date(), time(0, 0)) + timedelta(days=1)

        amount_of_time: timedelta = (tomorrow_midnight + user_time_arg) - right_now

        print("Amount of time until " + str(user_time_arg) + " tomorrow: " + str(amount_of_time.seconds // 3600) +
              "H " + str((amount_of_time.seconds // 60) % 60) + "M")
        return True

    return False


# returns None on invalid input.
def parse_input_time(arg: str) -> Union[timedelta, None]:
    hours: str = "0"
    minutes: str = "0"
    seconds: str = "0"
    colon_counter: int = 0

    # Make sure that the string passed is iterable if not. return None.
    if arg is None:
        return None

    # look at what the user has passed, make sure that all contents are either
    # a digit or a colon. Parse the verified input into a timedelta and return
    for i in arg:
        digit: bool = str.isdigit(i)
        colon: bool = i == ":"

        if not digit and not colon:
            return None

        elif digit:
            if colon_counter == 0:
                hours += i

            elif colon_counter == 1:
                minutes += i

            elif colon_counter == 2:
                seconds += i

            elif colon_counter > 2:
                return None

        elif colon:
            colon_counter += 1

    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))


if __name__ == "__main__":
    main()
