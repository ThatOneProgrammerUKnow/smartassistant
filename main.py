import os
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv
from datetime import datetime

from packages.audio.audio import play_sound
from packages.audio.audio import get_text
from packages.apis.weather import get_weather_today
from packages.spotify_player.spotifyplayer import SpotifyPlayer
from packages.open import openmanager


#===================================================# Configuration #===================================================#
USERNAME = "Kobus"
EXIT_ALIAS = ["EXIT"]
BACK_ALIAS = ["BACK"]
LIST_COMMANDS = ["HELP", "LIST COMMANDS"]
LAST_WEATHER_REPORT = 10
RECORD_DURATION = 4


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


#===================================================# Helper methods #===================================================#
#===================# Conversational #===================#
def greet():
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

  play_sound(f"Good {time_of_day}, {USERNAME}.\n{weather}")

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
        music.alter_volume("increase")

def decrease_volume():
    if music.playback_running():
        music.alter_volume("decrease")

def set_volume(user_input):
    if music.playback_running():
        music.alter_volume("set", amount)

    

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
def open_program(input):
    program = input.replace("OPEN ", "")

    # If program objext exists
    if openmanager.exists(program): 
        print(SUCCESS_COLOR)
        print(f"Opening {openmanager.get_name(program)}")
        play_sound(f"Opening {openmanager.get_name(program)}")
        openmanager.open(program)
        print(RESET)

    # If program object does not exist
    else:
        print(WARNING_COLOR)
        print(f"{program} not found")
        print(RESET)


#===================================================# Main method #===================================================#
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
        elif "UNPAUSE MUSIC" in user_input:
            unpause_music()

        elif "PAUSE MUSIC" in user_input:
            pause_music()

        # Specific playlist
        elif "PLAY MUSIC" in user_input:
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
            print("Open")
            open_program(user_input)


        
            
        
        

        user_input = input(f"{USERNAME}: {USER_COLOR}").upper()
        print(RESET)
        os.system("cls")
    

def main():
  greet()
  main_loop()

if __name__ == "__main__":
  main()