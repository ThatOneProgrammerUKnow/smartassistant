import random

class Playlist:
    
    _instances = []

    def __init__(self, name, id, uri, alias=[]):
        # Atttributes
        self.name = name
        self.id = id
        self.uri = uri
        self.alias = [self.name.upper(), self.id]
        
        if alias:
            self.alias.extend([str(a).upper() for a in alias])

        # Instances
        Playlist._instances.append(self)
    
    def get_uri(self):
        return self.uri
    
    def __str__(self):
        return f"{self.id}. {self.name}"


##-->> Other methods
# Add new playlists here
def load():
    Playlist._instances.clear()
    

    return [
    Playlist("Piano Covers", "1", "spotify:playlist:2EqfHxWJsJJWon2OuPE0Gm", ["covers"]),
    Playlist("Piano Blues", "2", "spotify:playlist:4dchdSr6IL2twY9EPWZtp0", ["blues"]),
    Playlist("Piano Jazz", "3", "spotify:playlist:1cGuko50vN3I4I3QndnguR", ["jazz"]),
    Playlist("Classical Piano", "4", "spotify:playlist:632WhLlq7UqkM3Qqp2xwLq", ["classical"]),
    Playlist("Boroque", "5", "spotify:playlist:4qJuDHMlm9SCMEZmVVO8AN"),
    Playlist("Mozart", "6", "spotify:playlist:5UcBffjK5Pzlo3S54jZfvz"),
    Playlist("Beethoven", "7", "spotify:playlist:303vag937UKki4PXhUGI85"),
    Playlist("Ludovico Einaudi", "8", "spotify:playlist:37i9dQZF1DWUofLlXqRWZz", ["ludovico", "einaudi"]),
    Playlist("Top 2025 songs", "9", "spotify:playlist:37i9dQZEVXcXHWVVT0lfDq", ["2025", "top 25", "top2025", "top 2025"]),
    Playlist("Medieval", "10", "spotify:playlist:4UucW6dxLMrTQUyZT3DVGL", ["medieval"]),
    Playlist("Gregorian Chant", "11", "spotify:playlist:3XctrCHJS1eeV1NbGOGvD3", ["gregorian", "chant"]),
]

def is_valid(query):
    for playlist in Playlist._instances:
        if any(a in query.upper() for a in playlist.alias)  or query.upper() == 'RANDOM':
            return True
    return False

def find(query):
    if query.upper() == "RANDOM":
        return random.choice(Playlist._instances)
    
    for playlist in Playlist._instances:
        if any(a in query.upper() for a in playlist.alias):
            return playlist
    return "Something went wrong"  
    
def all_playlists():
    return [str(playlist) for playlist in Playlist._instances]
        
def get_random():
    random_obj = random.choice(Playlist._instances)
    return random_obj.get_uri()