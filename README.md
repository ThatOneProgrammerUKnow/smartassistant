# Overview
I didn't start this project for my portofolio. I started it because I wanted to see if it is posible to play music, on Spotify, with python. And I could!
Since then, I continued digging around in API's and started making my life a little bit easier with this assistant. 

# How to use
## API's
### General
I used my personal API keys and saved them is a .env file. Anyone using this program would have to use their own. 

### Speech to text & Text to speech
In the audio package, there is a global boolean variable to enable or dissable these features (I disable them when I debug other issues or want to save credits.

To use the speech to text feature, you can press "enter" and you will have 5 seconds to speak your command. (I made it 5 seconds so I don't use up too many
credits 

### Weather
In the main.py file, there is a global variable "LAST_WEATHER_REPORT". It takes up an hour in 24 hour time to say until which time it will retrieve the weather. 
If the variable is equal to 8, then if you start the assistant before 8 in the morning, it will read the weather report for you, if you start it after, it won't. 


## Command line
You can type out any commands from the "command list" and the assistant will provide you with all your commands. 

### Command line colors.
In the start of the main.py file, you can see the global variables used for the command colors, I configure them there. 

## Spotify and opening programs/files
I have two similar packages: "spotify_player" and "open". Both of them has two files. One for public methods used in main.py, configering any api keys etc, and one
for configuring any available options like available playlists or programs and files to open. 

As of yet, the spotify_player can only play, pause and play a specefic playlist configured in the package. (Again, this is not a comercial or portofolio project)
So to add a playlist, you have to go to the playlist.py file and to the load() method. This method creates and returns all the playlist objects. You just add a new
one in this format. 

Playlist("name of playlist", "number of playlist", "playlist uri", ["alias one", "alias two"]),

You should be able to replicate it according to how I've done it. 

The same princeple follows with opening programs and files. There is a bit more and diffirent logic, but creating the instance stayes the same. 

# Thank you
Thank you for looking at my project. Feel free to make adjustments or reach out and give feedback!













