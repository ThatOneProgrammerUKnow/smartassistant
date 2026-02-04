import os, sys, time, threading, subprocess, ctypes
import sounddevice as sd
import soundfile as sf

from dotenv import load_dotenv
from datetime import datetime

from packages.audio.audio import play_sound
from packages.audio.audio import get_text
from packages.apis.weather import get_weather_today
from packages.spotify_player.spotifyplayer import SpotifyPlayer
from packages.open import openmanager
from packages.add_ons.helper_methods import extract_number



#===================================================# Configuration #===================================================#
USERNAME = "Kobus"
EXIT_ALIAS = ["EXIT"]
BACK_ALIAS = ["BACK"]
LIST_COMMANDS = ["HELP", "LIST COMMANDS"]
LAST_WEATHER_REPORT = 8
RECORD_DURATION = 4

# Shut down
SHUT_DOWN = False
SHUT_DOWN_HOUR = 22
SHUT_DOWN_MINUTE = 00

# ALarm
ALARM = True
ALARM_HOUR = 22
ALARM_MINUTE = 25
ALARM_THREAD = None








#===================================================# Initialization #===================================================#
# Basic styles
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

# Colors
BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"

BRIGHT_BLACK   = "\033[90m"
BRIGHT_RED     = "\033[91m"
BRIGHT_GREEN   = "\033[92m"
BRIGHT_YELLOW  = "\033[93m"
BRIGHT_BLUE    = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN    = "\033[96m"
BRIGHT_WHITE   = "\033[97m"

TEAL = "\033[38;2;0;128;128m"
SOFT_TEAL = "\033[38;2;0;180;170m"
CALM_BLUE = "\033[38;2;80;140;200m"
TERMINAL_GREEN = "\033[38;2;0;200;70m"

## Theme

VSI_COLOR = WHITE
VSI_COLOR_TWO = BRIGHT_CYAN

SUCCESS_COLOR = TERMINAL_GREEN
ERROR_COLOR = RED
WARNING_COLOR = YELLOW

USER_COLOR = CYAN



# Packages and libraries
load_dotenv()
music = SpotifyPlayer()

#===================================================# Global Variables #===================================================#
#===================# Text #===================#
## Opening text
opening_text = f'''{VSI_COLOR}
Hello there! {USERNAME}\n
This is your vsi assistant. This text prompt is where you will give me commands. (I know, it doesnt look like much.. Yet!)\n
Its not entirely like a smart assistant yet, more like a user friendly command  prompt. 
Just type {BOLD}{SUCCESS_COLOR}help{RESET}{VSI_COLOR} or {BOLD}{SUCCESS_COLOR}list commands{RESET}{VSI_COLOR} for me to show you what you can do. \n
Enjoy!\n
    {RESET}'''

## Help
help_text = f'''{VSI_COLOR}
{VSI_COLOR_TWO}"> help"{VSI_COLOR}: Shows this list.\n
{VSI_COLOR_TWO}"> play music"{VSI_COLOR}: gives you a list of playlist options to choose from. You then choose your playlist.\n  
{VSI_COLOR_TWO}"> weather"{VSI_COLOR}: Gives you the current weather report.\n
{VSI_COLOR_TWO}"> list programs"{VSI_COLOR}: Gives you a list of all the available programs, files or websites I can open.\n  
{VSI_COLOR_TWO}"> open 'program'"{VSI_COLOR}: Opens the specified program, file, or website. Pretty cool right!\n
            {RESET}
'''

## Playlist options
playlist_options = f"{VSI_COLOR}Your playlist options are:\n\n{"\n".join(music.options())}\n{RESET}"

#===================================================# Ascync #===================================================#
#====================# Shutting down #====================#
# Shut down
def shutdown():
    subprocess.run(
    ["shutdown", "/s", "/t", "15"],
    shell=False
    )

    # Give apps time to respond
    time.sleep(10)

    # Step 2: Force-close remaining USER processes only
    subprocess.run(
        'taskkill /F /FI "USERNAME eq %USERNAME%"',
        shell=True
    )

    # Step 3: Immediate forced shutdown
    os.system("shutdown /s /f /t 0")

# Confirn shut down - Last chance
def confirm_shutdown():
    result = ctypes.windll.user32.MessageBoxW(
        0,
        "PC will shut down now.\nPress Cancel to abort.",
        "Shutdown Warning",
        1
    )
    return result == 1  # OK


# Countdown to shutdown
def shutdown_countdown():
    countdown = 10
    time.sleep(1)
    countdown -= 1
    print(WARNING_COLOR)

    os.system("cls")
    play_sound(f"Shutting down in {countdown}") # Audio

    while countdown > 0:
        if countdown == 5: print(ERROR_COLOR)
        os.system("cls")
        play_sound(f"{countdown}") # Audio
        print(f"Shutting down in {countdown}")
        time.sleep(1)
        countdown -= 1

    # Confirmation
    if not confirm_shutdown():
        print("Shutdown cancelled")
        play_sound("Shutdown cancelled")
        return
    
    shutdown()

#====================# Alarm #====================#
def alarm():
    # Wait for alarm to go off
    wake_up = False
    while not wake_up:
        now = datetime.now()
        if now.hour == ALARM_HOUR and now.minute == ALARM_MINUTE:
            wake_up = True
    
    # Alarm
    '''
    When the alarm goes of the following happens:
    1. Your "man of steel" playlist gets started at volume 30.
    2. You get greeted with the weather report for the day.
    3. Volume gets boosted to 100%
    '''
    music.play_playlist("wake up")
    music.alter_volume("set", 50)
    greet("wake_up")
    for counter in range(5, 10):
        music.alter_volume("increase", 10)
        time.sleep(1)
    

#====================# Time watcher #====================#
'''def time_watcher():
    while True:

        def time_is(hour, minute):
            now = datetime.now()
            return now.hour == hour and now.minute == minute

        if SHUT_DOWN:
            if time_is(SHUT_DOWN_HOUR, SHUT_DOWN_MINUTE):
                shutdown_countdown()
                time.sleep(60)  # prevent repeated calls
        elif ALARM:
            if time_is(ALARM_HOUR, ALARM_MINUTE):
                alarm()
        time.sleep(1)'''




#===================================================# Helper methods #===================================================#
#===================# Conversational #===================#
def greet(message):
    weather = ""

    now = datetime.now()
    hour = int(now.strftime("%H"))

    ## Time of day
    if now.strftime("%p") == "AM":
        time_of_day = "morning"
    else:
        time_of_day = "afternoon" if hour < 18 else "evening"

    # Last weather report before glbal variable (Configure at the top)
    if hour < LAST_WEATHER_REPORT:
        weather = get_weather_today()

    if message == "login":
        GREETING_MESSAGE = f"Good {time_of_day}, {USERNAME}.\n{weather}"
    elif message == "wake_up":
        GREETING_MESSAGE = f'''
        Good {time_of_day}, {USERNAME}, I hope you slept well. It is time to get up. 
        Think of the man you want to be. Dissaplined, hard working. \n\nNow get that bottom up and be than man.
        {weather}
        '''
    


    
    play_sound(GREETING_MESSAGE)

#===================# Sound related #===================#
def record_file(filename="input.wav", duration=RECORD_DURATION, samplerate=44100):
    print(f"{USER_COLOR}Listening...{RESET}")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    sf.write(filename, audio, samplerate)
    print(f"{VSI_COLOR_TWO}Saved input to {filename}")
    return filename



#=====# Plays music #=====#
def play_music(user_choice):
    valid_option = False
    while not valid_option and not any(a in user_choice.upper() for a in BACK_ALIAS): # Lets the user choose a valid playlist
        if music.is_valid_playlist(user_choice):
            music.play_playlist(user_choice)
            valid_option = True
            playlist_name = music.get_name(user_choice)
            play_sound(f"Playing {playlist_name}.")
            os.system("cls")
            print(f"{SUCCESS_COLOR}Playing {playlist_name}{RESET}")

        else:
            play_sound("Playlist not found")
            user_choice = input(f"{BOLD}{WARNING_COLOR}Playlist not found.{RESET}{VSI_COLOR}\n\n{playlist_options}\nAvailable playlists are: {USER_COLOR}")
            if not user_choice:
                user_choice = record_command()
            print(RESET)

#===================================================# User input handling #===================================================#
def list_commands():
    print(help_text)

#=====# Spotify related #=====#
def play_music_command():
    print(f"{playlist_options}")
    user_input = input(f"Available music options:{USER_COLOR} ")

    if not user_input: 
        user_input = record_command()
        user_input = user_input.replace(".", "")

    if not any(a in user_input.upper() for a in BACK_ALIAS):
        play_music(user_input)
        print(RESET)

def play_playlist_command(input):
    choice = input.replace("PLAY ", "")
    play_music(choice)

def pause_music():
    music.pause()

def unpause_music():
    music.play()

def increase_volume():
    if music.playback_running():
        print(f"{SUCCESS_COLOR}Increasing volume{RESET}")
        music.alter_volume("increase")

def decrease_volume():
    if music.playback_running():
        print(f"{SUCCESS_COLOR}Decreasing volume{RESET}")
        music.alter_volume("decrease")

def set_volume(user_input):
    if music.playback_running():
        try:
            amount = extract_number(user_input)
            print(f"{SUCCESS_COLOR}Changing volume{RESET}")
            music.alter_volume("set", amount)
        except ValueError:
            print(f"{WARNING_COLOR}No valid numbers found{RESET}")

    

#=====# Audio related #=====#
def record_command():

    filename = record_file()
    user_input = get_text(filename).text.upper()

    os.system("cls")
    print(f"{USERNAME}: {USER_COLOR}{user_input.capitalize()}{RESET}")
    user_input = user_input.replace(".", "")

    return user_input

#=====# OpenManager related #=====#  
# List all available programs
def list_programs():
    print(VSI_COLOR + BOLD)

    print("Here are your options:")
    print(RESET + VSI_COLOR)
    options = sorted(openmanager.all_program_options(), key=lambda s: s.upper())
    # Print options in 3 columns
    if not options:
        print("(no options available)")
        print(RESET)
        return

    cols = 5
    col_width = max(len(o) for o in options) + 4
    rows = (len(options) + cols - 1) // cols

    for r in range(rows):
        row_items = []
        for c in range(cols):
            idx = c * rows + r
            if idx < len(options):
                row_items.append(f"- {options[idx]}")
            else:
                row_items.append("")
        print("".join(item.ljust(col_width) for item in row_items))

    print(RESET)

# Open a program or website url
def open_program(program):

    # If program objext exists
    if openmanager.exists(program): 
        print(SUCCESS_COLOR)
        restart = True if program == "RESTART ASSISTANT" else False # If system is restarting

        message = "Restarting" if restart else "Opening" # Message
        play_sound(f"{message} {openmanager.get_name(program)}") # Play message
        print(f"{message} {openmanager.get_name(program)}")
        openmanager.open(program) # Opening program
        print(RESET)


        if restart: sys.exit()
        print(f"{SUCCESS_COLOR}Succsesfully opened{RESET}\n")

    # If program object does not exist
    else:
        print(WARNING_COLOR)
        print(f"{program} not found")
        print(RESET)

#=====# Time related #=====#
def set_alarm(user_input):
    global ALARM_HOUR, ALARM_MINUTE, ALARM_THREAD
    first_loop = True
    while True:
        try:
            # Check if input contains colon
            if ":" not in user_input:
                raise ValueError("Time format must be hh:mm")
            
            parts = user_input.split(":")
            if len(parts) != 2:
                raise ValueError("Time format must be hh:mm")
            
            hour = int(parts[0].strip())
            minute = int(parts[1].strip())
            
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Invalid time range")
            
            ALARM_HOUR = hour
            ALARM_MINUTE = minute
            formatted_time = f"{hour:02d}:{minute:02d}"
            
            # Kill existing alarm thread if it exists
            if ALARM_THREAD is not None and ALARM_THREAD.is_alive():
                print(f"{WARNING_COLOR}Replacing previous alarm{RESET}")
            
            # Start new alarm thread
            ALARM_THREAD = threading.Thread(target=alarm, daemon=True)
            ALARM_THREAD.start()
            print(f"{SUCCESS_COLOR}Alarm set for {formatted_time}{RESET}")
            play_sound(f"Alarm set for {formatted_time}")
            break
            
        except (ValueError, IndexError):
            if first_loop:
                print(f"{VSI_COLOR}Set alarm in the format hh:mm (e.g., 08:30){RESET}")
            else:
                print(f"{WARNING_COLOR}Invalid time format. Please use hh:mm (e.g., 08:30){RESET}")
            user_input = input(f"Enter alarm time:{USER_COLOR} ")
            if not user_input:
                user_input = record_command()
            print(RESET)


#===================================================# Main method #===================================================#
#=====# Aliases for calling methods #=====#
UNPAUSE_MUSIC = ["UNPAUSE MUSIC"]
PAUSE_MUSIC = ["PAUSE MUSIC"]
START_MUSIC = ["MUSIC OPTIONS", "AVAILABLE MUSIC", "START MUSIC", "PLAY SOME MUSIC", "START PLAYING MUSIC", "PLAY MUSIC"]


RELOAD_ASSISTANT = ["RELOAD ASSISTANT", "RESTART ASSISTANT", "RELOAD SMART ASSISTANT", "RESTART SMART ASSISTANT", "RESTART"]
SET_ALARM = ["SET ALARM"]

#=====# Method #=====#
def main_loop():
    os.system("cls")
    print(opening_text)
    user_input = input(f"{USERNAME}:{USER_COLOR} ").upper()
    print(RESET)
    while user_input not in EXIT_ALIAS:
        # Voice commands
        if not user_input:
            user_input = record_command()

        # Inputs
        if any(command in user_input for command in LIST_COMMANDS):
            list_commands()

        #=====# Music #=====#
        # Show options and choose one
        
        
        # Pause and play
        elif any(a in user_input for a in UNPAUSE_MUSIC):
            unpause_music()

        elif any(a in user_input for a in PAUSE_MUSIC):
            pause_music()

        # Specific playlist
        elif any(a in user_input for a in START_MUSIC):
            play_music_command()

        elif "PLAY" in user_input:
            play_playlist_command(user_input)

        # Volume
        elif "INCREASE VOLUME" in user_input:
            increase_volume()

        elif "DECREASE VOLUME" in user_input:
            decrease_volume()

        elif "SET VOLUME" in user_input:
            set_volume(user_input)

        #=====# Weather #=====#
        elif "WEATHER" in user_input:
            weather = get_weather_today()
            print(weather)
            play_sound(weather)

        #=====# Openmanager #=====#
        elif "LIST PROGRAMS" in user_input:
            list_programs()

        elif "OPEN" in user_input:
            open_program(user_input)

        elif any(a in user_input for a in RELOAD_ASSISTANT):
            open_program("RESTART ASSISTANT")

        #=====# Alarm #=====#
        elif any(a in user_input for a in SET_ALARM):
            set_alarm(user_input)
        user_input = input(f"{USERNAME}: {USER_COLOR}").upper()
        print(RESET)
        os.system("cls")
    

def main():
    greet("login")
    main_loop()

if __name__ == "__main__":
  main()