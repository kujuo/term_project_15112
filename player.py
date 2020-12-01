from cmu_112_graphics import *
from xml_io import *
from design import *
from pygame import mixer

# reference for pygame mixer: https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/

class PlayerMode(Mode):
    def appStarted(mode):
        mixer.init(channels=1)
        # mode.channel = mixer.Channel(0)
        songsXML.addAllSongs()

        mode.buttons = {
            'play': (mode.width//2-20,mode.height//1.5-20,
                     mode.width//2+20,mode.height//1.5+20),
        }
        mode.allSongs = songsXML.getAllSongs()
        mode.loaded = False
        mode.paused = False
        mode.shuffle = False
        mode.skipCount = 0
        mode.volume = 1
        mode.nowPlaying = None
        mode.playlists = {
            'all local songs':mode.allSongs,
        }
        mode.queue = Playlist('queue',None)

    def togglePlay(mode):
        if mode.loaded:
            if mixer.music.get_busy():
                if mode.paused:
                    # mode.channel.unpause()
                    mixer.music.unpause()
                else:
                    # mode.channel.pause()
                    mixer.music.pause()
                mode.paused = not mode.paused
            else:
                mixer.music.play()
                # mode.channel.play()
        else:
            numsongs = mode.loadQueue(mode.allSongs)
            print(f'loaded {numsongs} songs')

    def loadQueue(mode,songs,pos=0):
        mode.loaded = True
        mode.queue.addSongs(songs)
        mode.nowPlaying = mode.queue.getSongs()[pos]
        mixer.music.load(mode.nowPlaying.path)
        # mode.channel.(something for loading)
        for song in mode.queue.getSongs()[pos+1:]:
            mixer.music.queue(song.path)
        return len(mode.queue.getSongs())
    
    def loadShuffledQueue(mode,songs):
        mode.queue.removeAllSongs()
        alreadySeen = set()
        while len(mode.queue.getSongs()) < len(songs):
            songNum = random.randint(0,len(songs)-1)
            if songNum not in alreadySeen:
                mode.queue.addSong(songs[songNum])
                alreadySeen.add(songNum)
        mode.loadQueue(mode.queue.getSongs())
    
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
            mode.skipCount -= 1
            mixer.music.unload()
            mode.loadQueue(mode.queue.getSongs(),mode.skipCount)
            mixer.music.play()
        elif event.key == 'Right':
            mode.skipCount += 1
            mixer.music.unload()
            mode.loadQueue(mode.queue.getSongs(),mode.skipCount)
            mixer.music.play()
        elif event.key == 'Down':
            mode.volume -= 0.05
            mixer.music.set_volume(max(mode.volume,0))
        elif event.key == 'Up':
            mode.volume += 0.05
            mixer.music.set_volume(min(mode.volume,1))
        elif event.key == 's':
            mixer.music.unload()
            mode.loadShuffledQueue(mode.allSongs)

    def drawQueue(mode,canvas):
        pass

    def drawButtons(mode,canvas):
        canvas.create_rectangle(mode.buttons['play'][0],mode.buttons['play'][1],
                                mode.buttons['play'][2],mode.buttons['play'][3],
                                fill=scheme.getAccent1(),width=0)

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        mode.drawButtons(canvas)
        canvas.create_text(50,50,text=str(mixer.get_num_channels()))
