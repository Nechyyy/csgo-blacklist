import os
import time
import pydirectinput
import threading

# Note: enter 'con_logfile shutup.log' in console to begin

# Clear Chat Message - bind this to '/'
# ﷽﷽ ﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽ ﷽﷽﷽﷽

# desired blacklisted phrases here
bannedWords = ["Doodooface"]

# copy and paste player's name here
playerWhitelist = ["You"]
playerBlacklist = ["Someone else"]

# Probably best to not touch these
chatIndicator = "‎ : " # valve uses weird unicode spacing in messages
teamchatIndicator = " :  "
chatDelay = 0.8
hotkeyDelay = 0.15

# Path to console log - change to where your csgo is
path = "C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\csgo\shutup.log" 

## Reset logs upon start (optional to save space)
file = open(path, "w")
file.truncate()
file.close()
file = open(path, "r+", encoding="utf8")

# message function to account for delay in anti chat spam
def write(x):
    time.sleep(hotkeyDelay)
    pydirectinput.keyDown(x)
    time.sleep(hotkeyDelay)
    pydirectinput.keyUp(x)
    time.sleep(chatDelay)

madeBlackListMessage = False
madeProfanityMessage = False

# function to send message
def sendMessage():
    global madeBlackListMessage
    global madeProfanityMessage
    while True:
        if madeProfanityMessage == True:
            madeProfanityMessage = False
            write('/')
            #write(',') # bind a message to ',' to appear whenever a blacklisted phrase was used
        elif madeBlackListMessage == True:
            madeBlackListMessage = False
            write('/')
            #write('.') # bind a message to '.' to appear whenever a blacklisted player tried to speak
        else:
            time.sleep(0.2)
    
def main():
    global madeBlackListMessage
    global madeProfanityMessage
    thread2 = threading.Thread(target=sendMessage)
    thread2.start()
    # Initialize update
    oldfilesize = os.path.getsize(path)
    print(oldfilesize)
    while True: #main loop
        time.sleep(0.05)
        filesize = os.path.getsize(path)
        if filesize > oldfilesize: # Do stuff when file is updated
            lines = file.read().splitlines()
            last_line = lines[-1] # Get last line of log
            print(last_line) # Print line to python console
            oldfilesize = filesize
            # in the case that people put chatindicators in their names - if damage given or damage taken or connected is in the string, don't do anything about it

            # We now have last line of the console, lets do something with it
            # whitelisted player
            if any(element in last_line and (chatIndicator or teamchatIndicator) in last_line for element in playerWhitelist):
                    break

            # blacklisted player
            elif any(element in last_line and (chatIndicator or teamchatIndicator) in last_line for element in playerBlacklist):
                    print("[shutup] A player on the blacklist just spoke.")
                    madeBlackListMessage = True

            # blacklisted phrase
            elif any(element in "".join(last_line.lower().split()) and (chatIndicator or teamchatIndicator) in last_line for element in bannedWords): # removes all whitespace from a message, converts it to lowercase, and joins it back into a string
                    print("[shutup] A player has been detected using a blacklisted word.")
                    madeProfanityMessage = True
                    

thread1 = threading.Thread(target=main)
thread1.start()
# reasons for multithreading: we need to continually search the console even when sending a message, else blacklisted messages will get through as the program will be too busy accounting for chat delay

# ideas for future
    # if someone is trying to be tricky and change their name to avoid blacklist, make it so that the code notices that someone changed their name, look it up in the blacklist, and if there's a match then append it to array
    # ideally i would want it to be, if foundblacklistmessage = true, do this function, and repeat until it's false, then close the function/thread.
