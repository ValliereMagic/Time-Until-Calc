# time libraries
from datetime import datetime, timedelta, time

# command line arguments
from argparse import ArgumentParser, Namespace


def main():
    """
    grab CLI argument, parse into a time delta, calculate the time in that amount of time
    and print it out.
    """

    arg_parser: ArgumentParser = ArgumentParser(
        description="Time, (until and from) calculation tool")

    arg_parser.add_argument('-f', '--time-from', dest="user_time_from", help="Specify an amount of time "
                                                                             "in the format HH:MM:SS "
                                                                             "to calculate what time it will be "
                                                                             "in that amount of time (from now).")

    arg_parser.add_argument('-u', '--time-until', dest="user_time_until", help="Specify a time in the format "
                                                                               "HH:MM:SS in military time "
                                                                               "to calculate the amount of time "
                                                                               "between then and now. "
                                                                               "If this command is executed before 3 "
                                                                               "in the morning, it will calculate "
                                                                               "Using today at midnight. After 3, "
                                                                               "The calculation will be done using "
                                                                               "tomorrow.")

    # retrieve user time string from argument parser
    parsed_args: Namespace = arg_parser.parse_args()

    # execute the option the user specified
    time_from: str = parsed_args.user_time_from
    time_until: str = parsed_args.user_time_until

    if time_from is not None:
        # parse the user provided into a timedelta
        parsed_user_time: timedelta or None = parse_input_time(time_from)

        # execute the action specified by the user
        execution_success: bool = calculate_time_from(parsed_user_time)

        # if the action fails, display the help message
        if not execution_success:
            arg_parser.print_help()

    elif time_until is not None:
        parsed_user_time: timedelta or None = parse_input_time(time_until)

        execution_success: bool = calculate_time_until(parsed_user_time)

        if not execution_success:
            arg_parser.print_help()

    else:
        arg_parser.print_help()


def calculate_time_from(user_time_arg: timedelta) -> bool:
    """
    Calculate the amount of time that is timedelta from now.
    """
    if user_time_arg is not None:
        # get the current time
        current_time: datetime = datetime.now()

        # calculate requested time
        print("Time " + str(user_time_arg) + " from now: " + str((current_time + user_time_arg).time()
                                                                 .strftime("%I:%M:%S %p")))
        return True

    return False


def calculate_time_until(user_time_arg: timedelta) -> bool:
    """
    Calculate the amount of time until timedelta.
    If the function is executed before 3AM it will use today to calculate.
    If after 3AM it will use tomorrow.
    """
    if user_time_arg is not None:

        # using current time for starting point.
        right_now = datetime.now()

        # If before 3AM on current day, calculate using today at midnight instead.
        # Otherwise user tomorrow at midnight.
        if right_now.hour <= 3:
            # today at midnight
            until_time: datetime = datetime.combine(
                datetime.today().date(), time(0, 0))

        else:
            # tomorrow at midnight
            until_time: datetime = datetime.combine(
                datetime.today().date(), time(0, 0)) + timedelta(days=1)

        amount_of_time: timedelta = (until_time + user_time_arg) - right_now

        print("Amount of time until " + str(user_time_arg) + " " + str(amount_of_time.seconds // 3600) +
              "H " + str((amount_of_time.seconds // 60) % 60) + "M")
        return True

    return False


def parse_input_time(arg: str) -> timedelta or None:
    """
    parse the string the user has inputted in the format HH:MM:SS 
    into a timedelta.
    If the user enters an invalid string None will be returned.
    """
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
