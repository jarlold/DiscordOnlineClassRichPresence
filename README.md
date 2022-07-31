# DiscordOnlineClassRichPresence
Python script that shows your online class schedule through Discord Rich Presence.

# Setup
1. Download the executable file and the `schedule.txt`
2. Fill out the schedule, see below for how (but it's pretty obviouse)
3. Make sure `schedule.txt` and `OnlineClassRichPresence.exe` are in the same folder,
   and that `schedule.txt` is named `schedule.txt`.
4. Launch `OnlineClassRichPresence.exe`
5. You should see a console appear saying the program has launched, if it only appears for
   a moment, it means Python has crashed because I'm a bad developer.
   
## Schedule setup.

1. Create a file named `schedule.txt` if it doesn't already exist.
2. The first line should either say `AM` or `24` to indicate whether or not
   you'd like to use an AM/PM clock or a 24-hour clock.
3. Then add 1 line for each of your classes, in the following format

    `Class Name, day_of_week, start_time, end_time`
    so for example
    `PhysEd, monday, 9:30, 11:30`
    would schedule physed from 9:30 to 11:30 on a monday. It's pretty simple system.
    

## Why is the exectuable unsigned?
I didn't sign it, because I don't have a certificate to sign it with, and I'm not giving 
Microsoft money to get one. 

## Linux support
You're smart, you'll figure it out.

