# Classes for song and playlist objects. Simplifies user experience and
# makes code more clean.
class Song(object):
    def __init__(self,title,artist,album,path,playcount=0):
        self.title = title
        self.artist = artist
        self.album = album
        self.path = path
        self.playcount = playcount
    
    def __hash__(self):
        return hash((self.title,self.artist,self.album,self.path))

    def __repr__(self):
        return self.title + ", " + self.path

    # I think this is dead code
    # TODO: delete
    def getDict(self):
        return {'title': self.title,
                'artist': self.artist,
                'album': self.album,
                'playcount': self.playcount}


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
    
    def addSongsDict(self,songDicts):
        for songDict in songDicts:
            self.songs.append(Song(songDict['title'],songDict['artist'],
                                   songDict['album'],songDict['path'],songDict['playcount']))

    def inPlaylist(self,song):
        return song in self.songs
    
    def incrementPlaylists():
        Playlist.numPlaylists += 1

    def getSongs(self):
        if self.parent != None:
            return self.parent.getSongs() + self.songs
        else:
            return self.songs
    
    def getLength(self):
        return len(self.songs)
    
    def addParent(self,parent):
        self.parent = parent
    
    def removeAllSongs(self):
        self.songs = []
    
    def removeSongsAfterPosition(self,position):
        self.songs = self.songs[:position+1]