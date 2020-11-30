# For more mostly useless soykaf, please consider going to:
# http://jarlold.netai.net
# I'll make a Discord bot or something for you if you pay me.
# -Jarlold

from pypresence import Presence
import time
from datetime import datetime
import math

# This might not be recommended practice, but it makes the code so much easier to read
now = datetime.now

# Class Name, Day of Week, Starting Hour, Starting Minute, Finishing Hour, Finishing Minute
# Should use surrender units (24 hour clock).
cal = list()

client_id = '770693841740103690'  
RPC = Presence(client_id)  # Initialize the client class
RPC.connect() # Start the handshake loop

# The classical "press any key to quit" notice
def press_any_key_to_quit():
    input("Press any key to quit...")
    exit()

# Converts numbers 0-6 to days of week ("monday", "tuesday", etc)
def number_to_dow(num):
    assert (num > 6 or num < 0)
    dows = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    return dows[num]

# Converts day of week to number 0-6
def dow_to_number(dow):
    dows = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    return dows.index(dow.lower())

# Loads in the calendar from a text file
def load_calendar(path="./schedule.txt"):
    try:
        sched_file = open(path, "r")
    except ValueError:
        print(
            "Unable to find file {}, make sure it exists, and is in the same folder as this executable.".format(path)
            )
        press_any_key_to_quit()
    sched = [i.strip() for i in sched_file.readlines() ]
    sched_file.close()

    # Clean out any blank lines from the file.
    tmp = []
    for _, s in enumerate(sched):
        if not s == "":
            tmp.append(s)
    sched = tmp
    # Check if the clock is 24 hours or AM/PM
    Is24Hour = sched[0] == "24" 
    # Make a list with all the classes in it
    classes = []
    for i in sched[1:]:
        classes.append(load_class(i, Is24Hour=Is24Hour))
    return classes

# Loads a single line from the calendar file
def load_class(class_string, Is24Hour=True):
    # Get the name out first
    name = class_string.split(',')[0]
    # Then we can clear out spaces without screwing it up
    class_string = class_string.replace(" ", '').split(',')

    # Then get the day of the week
    try:
        day = int(class_string[1])
    except ValueError:
        day = dow_to_number(class_string[1])

    # Gets the starting time
    start_hr, start_min = class_string[2].split(":")
    # Gets the ending time
    end_hr, end_min = class_string[3].split(":")
    # Converts the starting and ending times if need be
    if not Is24Hour:
        if "pm" in start_min.lower() and not "12" in start_hr.lower():
            start_hr = int(start_hr) + 12
        if "pm" in end_min.lower() and not "12" in end_hr:
            end_hr = int(end_hr) + 12
        start_min = start_min.lower().strip("am").strip("pm")
        end_min = end_min.lower().strip("am").strip("pm")
    # Put them in a list, with the appropriate types.
    try:
        course = [name, int(day), int(start_hr), int(start_min), int(end_hr), int(end_min)]
    except ValueError:
        print("Error parsing the schedule file, make sure the day of week is a number 0-6, and the times are correct")
        press_any_key_to_quit()
        
    return course 

# Returns True if the class is currently in progress
def is_class_now(course):
    # If it's not the right weekday, screw off
    if not course[1] == now().weekday():
        return False

    hr1 = course[2] + course[3]/60.0
    hr2 = course[4] + course[5]/60.0
    hr3 = now().hour + now().minute/60.0

    return (hr1 <= hr3 and hr2 >= hr3)

# Return the length of a class in unix-epoch friendly seconds
def unix_class_time_left(course):
    tn = now().hour + now().minute/60.0
    te = course[4] + course[5]/60.0
    tl = te - tn 
    return tl * 60 * 60

# Updates the rich presence profile widget to say which class the user is in
# and for how long.
def update_rpc(course):
    RPC.update(
        details=course[0],
        end=time.time() + unix_class_time_left(course)
    )

# Updates the rich presence profile widget to say "not in class"
def update_rpc_done():
    RPC.update(
        details="No longer in class"
    )


# Checks if there's a class starting, and if the RPC needs updating
def check_for_class_update():
    in_class = False
    for course in cal:
        if is_class_now(course):
            update_rpc(course)
            in_class = True
    if not in_class:
        update_rpc_done()

# The main function loop
def main():
    global cal
    cal = load_calendar()
    print("You should now see your Discord status change to 'main.py' or 'Online Class'")
    while True:  
        check_for_class_update()
        time.sleep(30) # We only need to check every so often (< 1 minute)

# Calls the main function loop. I know some people hate this
# but those people are less likely to send me e-mails about it
# than the guys who like it.
main()
