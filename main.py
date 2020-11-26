from cmu_112_graphics import *
from playlist import *
from lastfm import *
from pygame import mixer
import os

class MainScreen(App):
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
        elif event.key == 't':
            pass
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

MainScreen(width=600, height=600)