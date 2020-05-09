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
    arg_parser.add_argument('-s', '--sleep-for', dest="user_sleep_length", help="How long you want to sleep in hours:minutes, "
                                                                                "and when you need to wake up.")
    arg_parser.add_argument('-w', '--wake-up', dest="user_wake_time",
                            help="When you want to wake up, in military time")
    # retrieve user time string from argument parser
    parsed_args: Namespace = arg_parser.parse_args()
    # execute the option the user specified
    time_from: str = parsed_args.user_time_from
    time_until: str = parsed_args.user_time_until
    time_to_sleep: str = parsed_args.user_sleep_length
    time_wake_up: str = parsed_args.user_wake_time
    # Calculating amount of time from now
    if time_from is not None:
        # execute the action specified by the user
        execution_success: bool = calculate_time_from(
            parse_input_time(time_from))
        # if the action fails, display the help message
        if not execution_success:
            arg_parser.print_help()
    # Calculating when to go to bed
    elif (time_to_sleep is not None) or (time_wake_up is not None):
        # Make sure that both arguments have been considered.
        if (time_to_sleep is not None) and (time_wake_up is not None):
            execution_success: bool = calculate_bedtime(parse_input_time(time_to_sleep),
                                                        parse_input_time(time_wake_up))
            if not execution_success:
                arg_parser.print_help()
        # User did not supply the required arguments
        else:
            print("Error. Both --sleep-for and --wake-up need to be defined "
                  "to calculate when to wake up.")
            arg_parser.print_help()

    # Calculating between then and now
    elif time_until is not None:
        # execute the action specified by the user
        execution_success: bool = calculate_time_until(
            parse_input_time(time_until))
        # if the action fails, display the help message
        if not execution_success:
            arg_parser.print_help()
    else:
        arg_parser.print_help()


def calculate_bedtime(sleep_length: timedelta, wake_up_time: timedelta) -> bool:
    """
    Calculate when you need to go to bed
    """
    if (sleep_length is None) or (wake_up_time is None):
        return False
    # The time we want to wake up, less the length of time to sleep
    bedtime: timedelta = wake_up_time - sleep_length
    # We don't care about crossing days, if we have reset the days to 0
    if bedtime.days < 0:
        bedtime += timedelta(days=1)
    # Show the user when to go to bed
    print("Bed Time: " + str(bedtime))
    return True


def calculate_time_from(user_time_arg: timedelta) -> bool:
    """
    Calculate the amount of time that is timedelta from now.
    """
    if user_time_arg is None:
        return False
    # get the current time
    current_time: datetime = datetime.now()
    # calculate requested time
    print("Time " + str(user_time_arg) + " from now: " + str((current_time + user_time_arg).time()
                                                             .strftime("%I:%M:%S %p")))
    return True


def calculate_time_until(user_time_arg: timedelta) -> bool:
    """
    Calculate the amount of time until timedelta.
    If the function is executed before 3AM it will use today to calculate.
    If after 3AM it will use tomorrow.
    """
    if user_time_arg is None:
        return False
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
        # Make sure the string we are parsing is valid
        if not digit and not colon:
            return None
        # Parse the current character
        if digit:
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
