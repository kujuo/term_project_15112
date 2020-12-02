from cmu_112_graphics import *
from xml_io import *
from design import *
from pygame import mixer
import random

# reference for pygame mixer: https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/

class PlayerMode(Mode):
    def appStarted(mode):
        mixer.init()
        songsXML.addAllSongs()

        mode.buttons = {
            'play': (mode.width//2-20,mode.height//1.5-20,
                     mode.width//2+20,mode.height//1.5+20),
        }
        
        mode.loaded = False
        mode.paused = False
        mode.shuffle = False
        mode.skipCount = 0
        mode.volume = 1
        mode.nowPlaying = None
        mode.sound = None
        mode.queuePos = 0
        mode.playlists = {
            # 'all local songs':mode.allSongs,
        }
        mode.queue = Playlist('queue',None)

    def togglePlay(mode):
        if mode.loaded:
            if mixer.music.get_busy():
                if mode.paused:
                    mixer.music.unpause()
                else:
                    mixer.music.pause()
                mode.paused = not mode.paused
            else:
                mixer.music.play()
        else:
            numsongs = mode.loadQueue(songsXML.getAllSongs())

    def handleNextSong(mode):
        songsXML.incrementPlayCount(mode.nowPlaying.title,mode.nowPlaying.path)
        userXML.addSongToDay(datetime.date.today(),mode.nowPlaying)
        mode.queuePos += 1
        mode.loadSong()

    def loadSong(mode):
        mode.nowPlaying = mode.queue.getSongs()[mode.queuePos]
        mixer.music.load(mode.nowPlaying.path)
        mixer.music.play()
        mode.sound = mixer.Sound(mode.nowPlaying.path)

    def loadQueue(mode,songs):
        mode.loaded = True
        mode.queue.addSongs(songs)
        mode.loadSong()
        return len(mode.queue.getSongs())
    
    def loadShuffledQueue(mode):
        songs = mode.queue.getSongs()
        mode.queue.removeAllSongs()
        alreadySeen = set()
        while len(mode.queue.getSongs()) < len(songs):
            songNum = random.randint(0,len(songs)-1)
            if songNum not in alreadySeen:
                mode.queue.addSong(songs[songNum])
                alreadySeen.add(songNum)
        mode.loadSong()
    
    def playClicked(mode,x,y):
        return (mode.buttons['play'][0] <= x <= mode.buttons['play'][2] and
                mode.buttons['play'][1] <= y <= mode.buttons['play'][3])

    def mousePressed(mode,event):
        if mode.playClicked(event.x,event.y):
            mode.togglePlay()

    def keyPressed(mode,event):
        if event.key == 'Space':
            mode.togglePlay()
        elif event.key == 'Left':
            mode.queuePos -= 1
            mode.loadSong()
        elif event.key == 'Right':
            mode.queuePos += 1
            mode.loadSong()
        elif event.key == 'Down':
            mode.volume -= 0.05
            mixer.music.set_volume(max(mode.volume,0))
        elif event.key == 'Up':
            mode.volume += 0.05
            mixer.music.set_volume(min(mode.volume,1))
        elif event.key == 's':
            mode.loadShuffledQueue()
            mode.queuePos = 0
            mode.loadSong()

    def timerFired(mode):
        if mode.sound != None:
            if mixer.music.get_pos() == -1:
                mode.handleNextSong()
        
    def drawQueue(mode,canvas):
        pass

    def drawStatusBar(mode,canvas):
        if mode.sound != None:
            canvas.create_rectangle(100,100,100+int(mode.sound.get_length()),105,fill='white')
            canvas.create_rectangle(100,100,100+mixer.music.get_pos()//1000,105,fill=scheme.getAccent2(),width=0)

    def drawButtons(mode,canvas):
        canvas.create_rectangle(mode.buttons['play'][0],mode.buttons['play'][1],
                                mode.buttons['play'][2],mode.buttons['play'][3],
                                fill=scheme.getAccent1(),width=0)

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        mode.drawButtons(canvas)
        mode.drawStatusBar(canvas)
