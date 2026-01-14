#===# Imports #===#
import os, spotipy, time, threading

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from packages.spotify_player import playlist

class SpotifyPlayer:
    #=====# Other classes #=====#


    # Initialization
    def __init__(self):
        ## Configuration
        self._shuffle_time = 25*60

        # Init & Load variables
        self.env_loaded = False 
        self.opened_spotify = False
        self.loaded_playlists = False

        # Global variables
        self.sp = None
        self.run_shuffle = True

        # Directories
        self.spotify_dir = "C:/Users/kobus/OneDrive/Desktop/Spotify.lnk"

        


    def _load_env(self):
        load_dotenv()
        self.env_loaded = True


    #=====# Private Methods #=====#

    #===# Getting spotify ready #===#
    # Authorising sp
    def _authorize(self):
        # Load and get enviroment variables 
        if self.env_loaded == False:
            self._load_env()
        
        # Authorize
        CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
        CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
        REDIRECT_URI = os.getenv("http://127.0.0.1:8888/callback")
        SCOPE = "user-modify-playback-state user-read-playback-state user-read-currently-playing"

        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id = CLIENT_ID,
                client_secret = CLIENT_SECRET,
                redirect_uri = REDIRECT_URI,
                scope = SCOPE
            ))
            return True
        except:
            return False
            
 
    # Getting sp device
    def _get_device_id(self):
        # Initial variables
        loop = True

        

        # If the authorization was succesfull
        if self.sp:
            while loop == True:
                devices = self.sp.devices()

                if devices["devices"]:
                    return devices["devices"][0]["id"]
                
                elif self.opened_spotify==False:
                    self._open_spotify()
                    self.opened_spotify= True
                    self._wait(10, "spotify")
                else:
                    print("No active devices were found.\nIf spotify is already open, please activate your device (Play and pause any song)")
                    self._wait(15, "spotify")
        else:
            self._authorize()

    #===# Helper methods #====#
    def _open_spotify(self):
        os.startfile(self.spotify_dir)
        self.opened_spotify = True

    def _wait(self, wait_time, wait_for):
        counter = 0
        dots = ["", ".", "..", "..."]
        for i in range(wait_time):
            self._clear()
            print(f"Waiting for: {wait_for}{dots[counter]}")
            counter+=1
            time.sleep(1)
            if counter == len(dots):
                counter = 0

    def _clear(self):
        os.system("cls")



    #=====# Public Methods #=====#
    """
    There are two diffirent choosing methods, but a third one will be added:
    1. Random
    2. The user gets to choose
    3. A playlist gets chosen depending on the day
    """
    def is_valid_playlist(self, choice):
        """Validate if a playlist choice is valid."""
        # Load playlist
        if self.loaded_playlists == False:
            playlist.load()
            self.loaded_playlists = True
        
        # Check if random
        if choice.upper() == "RANDOM":
            return True
        
        # Check if user playlist exists
        return playlist.is_valid(choice)

    def get_name(self, choice):
        obj = playlist.find(choice)
        return obj.name

    def play_playlist(self, choice):
        """Play the selected playlist."""
        # Get device id
        device_id = self._get_device_id()

        # Get playlist object and URI
        playlist_obj = playlist.find(choice)
        uri = playlist_obj.get_uri()

        try: 
            self.sp.start_playback(context_uri=uri, device_id=device_id)
        except:
            print("Something went wrong")
        return True
        
    # Pause music
    def pause(self):
        if not self.sp: self._authorize
        device_id = self._get_device_id()
        try:
            self.sp.pause_playback(device_id=device_id)
        except Exception as e:
            print(f"Cannot pause music: {e}")

    # Play music
    def play(self):
        if not self.sp: self._authorize

        device_id = self._get_device_id()
        try:
            self.sp.start_playback(device_id=device_id)
        except Exception as e:
            print(f"Cannot play music: {e}")

    def options(self):
        if self.loaded_playlists == False:
            playlist.load()

        return playlist.all_playlists()
    
    # Volume
    def playback_running(self):
        if not self.sp: self._authorize()
        
        pb = self.sp.current_playback()

        if pb is None:
            return False

        return pb.get("is_playing", False)


    def alter_volume(self, method, amount=10):
        if not self.sp:
            self._authorize()

        device_id = self._get_device_id()
        playback = self.sp.current_playback()

        if not playback or "device" not in playback:
            print("No active playback/device found. Cannot change volume.")
            return False

        current = playback["device"].get("volume_percent", 0)

        # Determine new volume
        if method == "set":
            new = amount
        elif method == "increase":
            new = current + amount
        elif method == "decrease":
            new = current - amount
        else:
            print(f"Unknown volume method: {method}")
            return False

        new = int(max(0, min(100, new)))
        try:
            self.sp.volume(new, device_id)
            return True
        except Exception as e:
            print(f"Cannot change volume: {e}")
            return False

            
        

    

    

        

    
