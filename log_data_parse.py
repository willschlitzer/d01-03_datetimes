from datetime import datetime, timedelta
import os
import urllib.request

# Code supplied by course

SHUTDOWN_EVENT = "Shutdown initiated"

# prep: read in the logfile
tmp = os.getenv("TMP", "/tmp")
logfile = os.path.join(tmp, "log")
urllib.request.urlretrieve(
    "https://bites-data.s3.us-east-2.amazonaws.com/messages.log", logfile
)

with open(logfile) as f:
    loglines = f.readlines()


# for you to code:


def convert_to_datetime(line):
    """Extract timestamp from logline and convert it to a datetime object.
       For example calling the function with:
       INFO 2014-07-03T23:27:51 supybot Shutdown complete.
       returns:
       datetime(2014, 7, 3, 23, 27, 51)
    """
    date_length = 19
    if line[0:5] == "ERROR":
        start_pos = 6
    elif line[0:4] == "INFO":
        start_pos = 5
    elif line[0:7] == "WARNING":
        start_pos = 8
    end_pos = start_pos + date_length
    date_string = line[start_pos:end_pos]
    year = int(date_string[0:4])
    month = int(date_string[5:7])
    day = int(date_string[8:10])
    hour = int(date_string[11:13])
    minute = int(date_string[14:16])
    second = int(date_string[17:19])
    return datetime(year, month, day, hour, minute, second)


def time_between_shutdowns(loglines):
    """Extract shutdown events ("Shutdown initiated") from loglines and
       calculate the timedelta between the first and last one.
       Return this datetime.timedelta object.
    """
    shutdowns = []
    for line in loglines:
        if SHUTDOWN_EVENT in line:
            shutdown = convert_to_datetime(line)
            shutdowns.append(shutdown)
    first_shutdown = shutdowns[0]
    last_shutdown = shutdowns[-1]
    return last_shutdown - first_shutdown


if __name__ == "__main__":
    shutdown_time = time_between_shutdowns(loglines)
    print(shutdown_time)
