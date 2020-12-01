from dataclasses import make_dataclass


# Song = make_dataclass('Song',['title','path'])
class Song(object):
    def __init__(self,title,path):
        self.title = title
        self.path = path
    
    def __hash__(self):
        return hash((self.title,self.path))

class Playlist(object):
    numPlaylists = 0
    def __init__(self,title,parent):
        self.title = title
        self.parent = parent
        self.songs = []

    def addSong(self,song):
        self.songs.append(song)
    
    def addSongs(self,songs):
        self.songs += songs
    
    def incrementPlaylists():
        Playlist.numPlaylists += 1

    def getSongs(self):
        if self.parent != None:
            return self.parent.getSongs() + self.songs
        else:
            return self.songs
    
    def addParent(self,parent):
        self.parent = parent
    
    def removeAllSongs(self):
        self.songs = []