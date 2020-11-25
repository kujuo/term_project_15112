# Deetya Iyer
# file for tech demo: 2020-11-23
# modules to demo:
    # pygame mixer
    # last.fm api
    # HTTP requests
# other modules (included w python, not external modules):
    # date/time
    # ElementTree
# resources referenced:
    # last.fm API:
        # https://www.dataquest.io/blog/last-fm-api-python/
        # https://www.last.fm/api/
    # pygame mixer:
        # https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/
    # XML file IO (not being demo-ed):
        # https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/
    # CMU 112 graphics:
        # course notes (https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html)
    # HTTP requests:
        # my old code from high school (AP research class)
        # same resource as last.fm API


from cmu_112_graphics import *
from pygame import mixer
import requests
import os
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

class LastFMUser(object):
    api_key = '43a1115a43350f02986daf50d4e99a9a'
    url = 'http://ws.audioscrobbler.com/2.0'
    def __init__(self,username):
        self.username = username
        self.headers = {
            'user-agent': self.username
        }

    def setUsername(self,username):
        self.username = username
    
    def lastFMGet(self,payload):
        payload['api_key'] = LastFMUser.api_key
        payload['format'] = 'xml'
        response = requests.get(LastFMUser.url,headers=self.headers,params=payload)
        return response.text

    def getAlbumInfo(self,artist,album):
        return self.lastFMGet({'method':'album.getInfo','artist':artist,'album':album})

    def getArtistTopAlbums(self,artist):
        return self.lastFMGet({'method':'artist.getTopAlbums','artist':artist})

    def getUserInfo(self):
        return self.lastFMGet({'method':'user.getInfo','user':self.username})
    
    def getUserLovedTracks(self):
        return self.lastFMGet({'method':'user.getLovedTracks','user':self.username})

    

class MyApp(App):
    def appStarted(self):

        # pygame mixer stuff
        mixer.init()
        self.rootDir = '/home/dee/code/schoolwork/15112/term_project/trial_runs/music_examples/'
        self.loaded = False
        self.paused = False
        self.skipCount = 0

        # UI stuff
        self.buttons = {
            'play': (self.width//2-20,self.height//1.5-20,
                           self.width//2+20,self.height//1.5+20),
            'playlist': (self.width//4-20,self.height//1.5-20,
                               self.width//4+20,self.height//1.5+20),
            'dataImport': (self.width//1.2-20,self.height//1.5-20,
                               self.width//1.2+20,self.height//1.5+20),
        }

        # playlist stuff
        self.examplePlaylist = Playlist('Example Playlist',None) # standalone
        
        # last.fm API stuff
        self.lastfmUser = LastFMUser('')

    def appStopped(self):
        mixer.quit()

    def togglePlay(self):
        if self.loaded:
            if mixer.music.get_busy():
                if self.paused:
                    mixer.music.unpause()
                else:
                    mixer.music.pause()
                self.paused = not self.paused
            else:
                mixer.music.play()
        else:
            print('load queue first, press q')
    
    def loadQueue(self,pos=0):
        self.loaded = True
        for track in os.listdir(self.rootDir):
            title = os.path.split(track)[1].split('.')[0] # gets song title
            song = Song(title=title,path=self.rootDir+track)
            self.examplePlaylist.addSong(song)
        mixer.music.load(self.examplePlaylist.getSongs()[pos].path)
        for song in self.examplePlaylist.getSongs()[pos+1:]:
            mixer.music.queue(song.path)
        return len(self.examplePlaylist.getSongs())

    def keyPressed(self,event):
        if event.key == 'Space':
            self.togglePlay()
        elif event.key == 'q':
            numSongs = self.loadQueue()
            print(f'queueing {numSongs} songs.')
        elif event.key == 'Left':
            self.skipCount -= 1
            mixer.music.unload()
            self.loadQueue(self.skipCount)
            mixer.music.play()
        elif event.key == 'Right':
            self.skipCount += 1
            mixer.music.unload()
            self.loadQueue(self.skipCount)
            mixer.music.play()

    def playClicked(self,x,y):
        return (self.buttons['play'][0] <= x <= self.buttons['play'][2] and
                self.buttons['play'][1] <= y <= self.buttons['play'][3])
    
    def playlistClicked(self,x,y):
        return (self.buttons['playlist'][0] <= x <= self.buttons['playlist'][2] and
                self.buttons['playlist'][1] <= y <= self.buttons['playlist'][3])
    
    def importClicked(self,x,y):
        return (self.buttons['dataImport'][0] <= x <= self.buttons['dataImport'][2] and
                self.buttons['dataImport'][1] <= y <= self.buttons['dataImport'][3])

    def mousePressed(self,event):
        if self.playClicked(event.x,event.y):
            self.togglePlay()
        elif self.playlistClicked(event.x,event.y):
            print('Your playlist:')
            for song in self.examplePlaylist.getSongs():
                print(song.title)
        elif self.importClicked(event.x,event.y):
            self.lastfmUser.setUsername(self.getUserInput('enter last.fm username:'))
            print(self.lastfmUser.getUserLovedTracks())
            

    def drawButtons(self,canvas):
        # play button
        canvas.create_rectangle(self.buttons['play'][0],self.buttons['play'][1],
                                self.buttons['play'][2],self.buttons['play'][3],
                                fill='grey')
        canvas.create_text(self.buttons['play'][0],self.buttons['play'][1],
                                text='play',anchor='s')
        # playlist button
        canvas.create_rectangle(self.buttons['playlist'][0],self.buttons['playlist'][1],
                                self.buttons['playlist'][2],self.buttons['playlist'][3],
                                fill='grey')
        canvas.create_text(self.buttons['playlist'][0],self.buttons['playlist'][1],
                                text='print playlist',anchor='s')
        # last.fm data import button
        canvas.create_rectangle(self.buttons['dataImport'][0],self.buttons['dataImport'][1],
                                self.buttons['dataImport'][2],self.buttons['dataImport'][3],
                                fill='grey')
        canvas.create_text(self.buttons['dataImport'][0],self.buttons['dataImport'][1],
                                text='get last.fm data',anchor='s')

    def redrawAll(self,canvas):
        self.drawButtons(canvas)

MyApp(width=600, height=600)