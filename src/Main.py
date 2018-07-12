# time libraries
from datetime import datetime, timedelta

# types
from typing import Union

# command line arguments
from argparse import ArgumentParser, Namespace


# grab CLI argument, parse into a time delta, calculate the time in that amount of time
# and print it out.
def main():

    arg_parser: ArgumentParser = ArgumentParser(description="Calculate time in X Hrs : X Mins : X Secs from now.")

    arg_parser.add_argument('--time', dest="user_time_string", help="Specify the amount of time "
                                                                    "in the format HH:MM:SS "
                                                                    "from now to calculate that "
                                                                    "time.")
    # retrieve user time string from argument parser
    parsed_args: Namespace = arg_parser.parse_args()

    # verify and parse user specified string
    parsed_user_time: Union[timedelta, None] = parse_input_time(parsed_args.user_time_string)

    if parsed_user_time is not None:
        # get the current time
        current_time: datetime = datetime.now()

        # calculate requested time
        print("Time " + str(parsed_user_time) + " from now: " + str((current_time + parsed_user_time).time()
                                                                    .strftime("%I:%M:%S %p")))
    else:
        print("Error. Invalid time specified")
        arg_parser.print_help()


# returns None on invalid input.
def parse_input_time(arg: str) -> Union[timedelta, None]:
    hours: str = "0"
    minutes: str = "0"
    seconds: str = "0"
    colon_counter: int = 0

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
