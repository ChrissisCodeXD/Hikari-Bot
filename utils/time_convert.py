
import re
time_regex = re.compile(r"(?:(\d{1,5})(d|w|y|m|h))+?")
time_dict = {"d": 86400, "w": 604800, "y": 31556952, "m": 60, "h": 3600}


def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            return f"{value} is an invalid time key! d|w|y|m|h are valid arguments"

        except ValueError:
            return f"{key} is not a number!"
    if time == 0:
        return f"{args} is invalid! d|w|y|m|h are valid arguments"
    else:
        return round(time)
