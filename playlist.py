from dataclasses import make_dataclass


Song = make_dataclass('Song',['title','path'])

class Playlist(object):
    numPlaylists = 0
    def __init__(self,title,parent):
        self.title = title
        self.parent = parent
        self.songs = []

    def addSong(self,song):
        self.songs.append(song)
    
    def incrementPlaylists():
        Playlist.numPlaylists += 1

    def getSongs(self):
        if self.parent != None:
            return self.parent.getSongs() + self.songs
        else:
            return self.songs
    
    def addParent(self,parent):
        self.parent = parent