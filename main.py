import os, textwrap
from dotenv import load_dotenv
from datetime import datetime
from packages.audio.audio import play_sound
from packages.apis.weather import get_weather_today
from packages.spotify_player.spotifyplayer import SpotifyPlayer

#===================================================# Configuration #===================================================#
USERNAME = "Kobus"
EXIT_ALIAS = ["EXIT"]
LIST_COMMANDS = ["HELP", "LIST COMMANDS"]
LAST_WEATHER_REPORT = 10


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
Its not entirely like a smart assistant yet, more like a user friendly commad  prompt. 
Just type {BOLD}{SUCCESS_COLOR}help{RESET}{VSI_COLOR} or {SUCCESS_COLOR}list commands{RESET}{VSI_COLOR} for me to show you what you can do. \n
Enjoy!\n
    {RESET}'''

## Help
help_text = f'''{VSI_COLOR}
{VSI_COLOR_TWO}"> help"{VSI_COLOR}: Shows this list.\n
{VSI_COLOR_TWO}"> play music"{VSI_COLOR}: gives you a list of playlist options to choose from. You then choose your playlist.\n  
{VSI_COLOR_TWO}"> weather"{VSI_COLOR}: Gives you the current weather report.
            {RESET}
'''

## Playlist options
playlist_options = f"{VSI_COLOR}Your playlist options are:\n\n{"\n".join(music.options())}\n{RESET}"


#===================================================# Helper methods #===================================================#
#===================# Conversational #===================#
def greet():
  weather = ""

  now = datetime.now()

  ## Time of day
  if now.strftime("%p") == "AM":
    time_of_day = "morning"

  else:
    hour = int(now.strftime("%H"))
    time_of_day = "afternoon" if hour < 18 else "evening"

  # Last weather report before glbal variable (Configure at the top)
  if hour < LAST_WEATHER_REPORT:
       weather = get_weather_today()

  play_sound(f"Good {time_of_day}, {USERNAME}.\n{weather}")

#===================# Music related #===================#



#=====# Plays music #=====#
def play_music(user_choice):
    valid_option = False
    while not valid_option and user_choice.upper() not in[EXIT_ALIAS]: # Lets the user choose a valid playlist
        if music.is_valid_playlist(user_choice):
            music.play_playlist(user_choice)
            valid_option = True
            playlist_name = music.get_name(user_choice)
            play_sound(f"Playing {playlist_name}.")
            os.system("cls")
            print(f"{VSI_COLOR_TWO}Playing {playlist_name}{RESET}")

        else:
            os.system("cls")
            play_sound("Playlist not found")
            user_choice = input(f"{BOLD}{WARNING_COLOR}Playlist not found.{RESET}{VSI_COLOR}\n\n{playlist_options}\nYour choice: {USER_COLOR}")
            print(RESET)

#===================================================# User input handling #===================================================#
def list_commands():
    print(help_text)

def play_music_command():
    print(f"{playlist_options}")
    play_music(input(f"Your choice:{USER_COLOR} "))
    print(RESET)

def play_playlist_command(input):
    choice = input.replace("PLAY ", "")
    play_music(choice)
    

#===================================================# Main methods #===================================================#
def main_loop():
    os.system("cls")
    print(opening_text)
    user_input = input(f"{USERNAME}:{USER_COLOR} ").upper()
    print(RESET)
    while user_input not in EXIT_ALIAS:
        # List commands
        if user_input in LIST_COMMANDS:
            list_commands()
        ## Music
        # Show options and choose one
        elif "PLAY MUSIC" in user_input:
            play_music_command()
        
        # Play a playlist
        elif "PLAY" in user_input:
            play_playlist_command(user_input)

        elif "WEATHER" in user_input:
            weather = get_weather_today()
            print(weather)
            play_sound(weather)

        user_input = input(f"{USERNAME}: {USER_COLOR}").upper()
        print(RESET)
        os.system("cls")
    

def main():
  greet()
  main_loop()

  

if __name__ == "__main__":
  main()