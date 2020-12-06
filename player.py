from cmu_112_graphics import *
from xml_io import *
from lastfm import *
from design import *
from pygame import mixer
import time,random

# reference for time module: https://docs.python.org/3/library/time.html
class PlayerMode(Mode):
    def appStarted(mode):
        # playback settings
        mode.initializePlayer()
        mode.queue = Playlist('queue',None)
        mode.queuePos = 0
        mode.nowPlaying = None
        mode.nowPlayingImage = None
        mode.nowPlayingSound = None
        mode.paused = False
        mode.mixerLoaded = False
        mode.repeatCurrent = False
        mode.ignorePlay = False

        mode.volume = 1

        # mode identifiers
        mode.selectQueueMode = True
        # selection modes are: album, artist, or playlist
        mode.selectionMode = ''
        # =====================

        #TODO:edit button positions
        # buttons in the queue selection menu
        mode.qButtons = {
            'all':(mode.width//1.5-5,50,
                   mode.width//1.5+5,60),
            'artist':(mode.width//1.5-5,70,
                      mode.width//1.5+5,80),
            'album':(mode.width//1.5-5,90,
                     mode.width//1.5+5,100),
            'playlist':(mode.width//1.5-5,110,
                        mode.width//1.5+5,120),
            'today':(mode.width//1.5-5,130,
                     mode.width//1.5+5,140),
            'build':(mode.width//1.5-5,150,
                     mode.width//1.5+5,160),
        }
        # buttons in the player screen
        mode.pButtons = {
            'play': (mode.width//2-20,mode.height//1.5-20,
                     mode.width//2+20,mode.height//1.5+20),
            'ignore': (mode.width//3-20,mode.height//3-20,
                       mode.width//3+20,mode.height//3+20),
            'focus': (2*mode.width//3-20,mode.height//3-20,
                       2*mode.width//3+20,mode.height//3+20),
            'savequeue':(0,0,0,0)
        }

        # miscellaneous vars that need to be class-wide
        mode.allAlbumCovers = []
        mode.textSelectionPosition = 0
    
    def initializePlayer(mode):
        mixer.init()
        songsXML.addAllSongs()
        mode.lastSync = settingsXML.getLastCloudSync()
        settingsXML.writeLastCloudSync(int(time.time()))
        songsXML.refreshLibraryFromCloud(user.getRecentTracks(mode.lastSync)) #TODO: testing the other TODO
        userXML.addSongsFromCloud(user.getRecentTracks(mode.lastSync))

# mouse pressed functions
    def queueButtonClicked(mode,button,x,y):
        return (mode.qButtons[buttons][0] <= x <= mode.qButtons[buttons][2] and
                mode.qButtons[buttons][1] <= y <= mode.qButtons[buttons][3])

    # selection mode buttons
    def albumCoverClicked(mode,x,y):
        pass

    # def artistNameClicked(mode,x,y):
    #     pass

    # def playlistNameClicked(mode,x,y):
    #     pass

    def mousePressed(mode,event):
        pass
    # end of selection mode buttons

# end of mouse pressed functions

# key pressed functions
    def handleDownKey(mode):
        if mode.selectQueueMode:
            if mode.selectionMode in 'artist,playlist':
                mode.textSelectionPosition += 1
        else:
            mode.volume -= 0.05
            mixer.music.set_volume(max(mode.volume,0))

    def handleUpKey(mode):
        if mode.selectQueueMode:
            if mode.selectionMode in 'artist,playlist':
                mode.textSelectionPosition -= 1
        else:
            mode.volume += 0.05
            mixer.music.set_volume(min(mode.volume,1))

    def handleEnterKey(mode):
        if mode.selectQueueMode:
            if mode.selectionMode == 'artist':
                print(songsXML.getAllArtists()[mode.textSelectionPosition])
                mode.queueArtist(songsXML.getAllArtists()[mode.textSelectionPosition])
                for song in mode.queue.getSongs():
                    print(song.title)
            elif mode.selectionMode == 'playlist':
                # mode.queuePlaylist(play)
                pass
    
    def handleDigitKey(mode,key):
        if mode.selectQueueMode:
            if key == '1':
                mode.queueAllSongs()
            elif key == '2':
                mode.selectionMode = 'album'
            elif key == '3':
                mode.selectionMode = 'artist'
            elif key == '4':
                pass
            elif key == '5':
                mode.queueTodayPlaylist()
            elif key == '6':
                while True:
                    query = mode.getUserInput('enter song title, enter x when done')
                    if query == 'x':
                        mode.selectQueueMode = False
                        break
                    result = songsXML.getSongTitleMatches(query)
                    if result != None:
                        print(result)
                        if len(result) == 1:
                            mode.queue.addSong(result[0])
                        else:
                            selection = mode.getUserInput('choose song')
                            mode.queue.addSong(result[int(selection)])
        # else:
        #     mode.queuePos += int(key)
        #     mode.loadNowPlaying()
        #     mode.loadNowPlayingCover()
                # build queue mode
                # include save queue as playlist button
                # also write playlists to xml file

    def handleSpaceKey(mode):
        if not mode.selectQueueMode:
            mode.togglePlay()
    
    def handleXKey(mode):
        if not mode.selectQueueMode:
            mode.resetPlayer()
        else:
            mode.app.setActiveMode(mode.app.welcomeMode)

    def keyPressed(mode,event):
        if event.key == 'Down':
            mode.handleDownKey()
        elif event.key == 'Up':
            mode.handleUpKey()
        elif event.key == 'Left':
            mode.skipSong(True)
        elif event.key == 'Right':
            mode.skipSong(False)
        elif event.key == 'Enter':
            mode.handleEnterKey()
        elif event.key == 'Space':
            mode.handleSpaceKey()
        elif event.key in '1234567890':
            mode.handleDigitKey(event.key)
        elif event.key == 'x':
            mode.handleXKey()
        elif event.key == 's':
            if not mode.selectQueueMode:
                mode.shuffleQueue()
        elif event.key == 'r':
            mode.repeatCurrent = not mode.repeatCurrent
        elif event.key == 'i':
            mode.ignorePlay = True
        elif event.key == 'd':
            mode.app.setActiveMode(mode.app.dataMode)
# end of key pressed functions

    def resetPlayer(mode):
        mode.queue.removeAllSongs()
        mixer.music.unload()
        mode.mixerLoaded = False
        mode.queuePos = 0
        mode.nowPlaying = None
        mode.nowPlayingImage = None
        mode.nowPlayingSound = None
        mode.paused = False
        mode.repeatCurrent = False
        mode.selectQueueMode = True
        mode.selectionMode = ''
        mode.textSelectionPosition = 0

# player queue functions
    def queueAlbum(mode,album,artist):
        mode.queue.removeAllSongs()
        mode.queue.addSongs(songsXML.getAlbumSongs(album,artist))
        mode.selectQueueMode = False

    def queueArtist(mode,artist):
        mode.queue.removeAllSongs()
        mode.queue.addSongs(songsXML.getArtistSongs(artist))
        for song in songsXML.getArtistSongs(artist):
            print(song.title)
        mode.selectQueueMode = False
        mode.textSelectionPosition = 0

    def queuePlaylist(mode,playlist):
        mode.queue.removeAllSongs()
        mode.queue.addSongs(playlist.getSongs())
        mode.selectQueueMode = False

    def queueTodayPlaylist(mode):
        date = datetime.date.today()
        print(date)
        dayType = userXML.getDayType(date)
        dayTime = userXML.getDayTime(date)
        playlist = userXML.getSongsForDayType(dayType,dayTime)
        mode.queue.addSongsDict(playlist)
        mode.selectQueueMode = False

    def queueAllSongs(mode):
        mode.queue.removeAllSongs()
        mode.queue.addSongs(songsXML.getAllSongs())
        mode.selectQueueMode = False

    def shuffleQueue(mode):
        songs = mode.queue.getSongs()[mode.queuePos:]
        mode.queue.removeSongsAfterPosition(mode.queuePos)
        while len(songs) > 0:
            songNum = random.randint(0,len(songs)-1)
            mode.queue.addSong(songs[songNum])
            songs.pop(songNum)

    def togglePlay(mode):
        if mode.mixerLoaded:
            if mode.paused:
                mixer.music.unpause()
            else:
                mixer.music.pause()
            mode.paused = not mode.paused
        else:
            mode.loadNowPlaying()
            mode.loadNowPlayingCover()
            mode.mixerLoaded = True
            mixer.music.play()
    
    def skipSong(mode,reverse=False):
        if reverse: mode.queuePos -= 1
        else: mode.queuePos += 1
        mode.loadNowPlaying()
        mode.loadNowPlayingCover()

    def handleNextSong(mode):
        print(mode.nowPlaying.path)
        if not mode.ignorePlay:
            songsXML.incrementPlayCount(mode.nowPlaying.path)
            userXML.addSongToDay(datetime.date.today(),mode.nowPlaying)
        else:
            mode.ignorePlay = False
        if not mode.repeatCurrent:
            mode.queuePos += 1
        mode.loadNowPlaying()
        mode.loadNowPlayingCover()
    
    def loadNowPlaying(mode):
        if 0 <= mode.queuePos < mode.queue.getLength():
            mode.nowPlaying = mode.queue.getSongs()[mode.queuePos]
            mixer.music.load(mode.nowPlaying.path)
            mixer.music.play()
            mode.nowPlayingSound = mixer.Sound(mode.nowPlaying.path)
        else:
            print('end of queue, press x to return to selection')

    def loadNowPlayingCover(mode):
        coverURL = user.getAlbumCoverURL(mode.nowPlaying.album,mode.nowPlaying.artist)
        mode.nowPlayingImage = mode.loadImage(coverURL)

    def timerFired(mode):
        if mode.nowPlayingSound != None:
            if mixer.music.get_pos() == -1 and mode.queuePos < mode.queue.getLength():
                mode.handleNextSong()

    def getAllAlbumCovers(mode):
        allAlbums = songsXML.getAllAlbums()
        for info in allAlbums:
            album,artist = info
            imgURL = user.getAlbumCoverURL(album,artist)
            mode.allAlbumCovers.append(mode.loadImage(imgURL))

# draw functions
    # draw functions for queue selection mode
    def drawQueuesForSelection(mode,canvas):
        canvas.create_text(50,(mode.qButtons['all'][1]+mode.qButtons['all'][3])//2,
                           text='all my music ( 1 )',font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.qButtons['album'][1]+mode.qButtons['album'][3])//2,
                           text='choose album ( 2 )',font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.qButtons['artist'][1]+mode.qButtons['artist'][3])//2,
                           text='choose artist ( 3 )',font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.qButtons['playlist'][1]+mode.qButtons['playlist'][3])//2,
                           text='choose playlist ( 4 )',font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.qButtons['today'][1]+mode.qButtons['today'][3])//2,
                           text="today's playlist ( 5 )",font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.qButtons['build'][1]+mode.qButtons['build'][3])//2,
                           text="build queue ( 6 )",font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
    
    def drawQueuesForSelectionButtons(mode,canvas):
        canvas.create_rectangle(mode.qButtons['all'][0],mode.qButtons['all'][1],
                                mode.qButtons['all'][2],mode.qButtons['all'][3],
                                fill=scheme.getAccent1(),width=0)
        canvas.create_rectangle(mode.qButtons['album'][0],mode.qButtons['album'][1],
                                mode.qButtons['album'][2],mode.qButtons['album'][3],
                                fill=scheme.getAccent1(),width=0)
        canvas.create_rectangle(mode.qButtons['artist'][0],mode.qButtons['artist'][1],
                                mode.qButtons['artist'][2],mode.qButtons['artist'][3],
                                fill=scheme.getAccent1(),width=0)
        canvas.create_rectangle(mode.qButtons['playlist'][0],mode.qButtons['playlist'][1],
                                mode.qButtons['playlist'][2],mode.qButtons['playlist'][3],
                                fill=scheme.getAccent1(),width=0)
        canvas.create_rectangle(mode.qButtons['today'][0],mode.qButtons['today'][1],
                                mode.qButtons['today'][2],mode.qButtons['today'][3],
                                fill=scheme.getAccent1(),width=0)

    def drawSelectionMode(mode,canvas):
        if mode.selectionMode == '':
            mode.drawQueuesForSelection(canvas)
        elif mode.selectionMode == 'album':
            mode.drawAllAlbums(canvas)
        elif mode.selectionMode == 'artist':
            mode.drawAllArtists(canvas)
        elif mode.selectionMode == 'playlist':
            pass

    def drawAllAlbums(mode,canvas):
        for albumCover in mode.allAlbumCovers:
            # canvas.create_image()
            pass
    
    def drawAllArtists(mode,canvas):
        artists = songsXML.getAllArtists()
        mode.drawTextItemSelection(canvas,artists,mode.textSelectionPosition)

    # L is a list containing the items that the user can select between
    # (like songs in an album, all artists, etc)
    # TODO: make this more user-friendly
    def drawTextItemSelection(mode,canvas,L,pos=0):
        # display 17 items at most
        length = len(L)
        displayBegin = max(pos-8,0)
        displayEnd = min(pos+9,length)
        topY = 100
        for i in range(displayBegin,displayEnd):
            yPos = topY + 20*(i%17)
            if i == pos:
                canvas.create_text(mode.width//2,yPos,text=L[i],fill=scheme.getAccent2())
            else:
                canvas.create_text(mode.width//2,yPos,text=L[i],fill=scheme.getAccent1())
    # end of draw functions for queue selection mode


    # draw functions for player mode
    def drawPlayerMode(mode,canvas):
        mode.drawNowPlaying(canvas)
        # TODO: draw buttons
    
    def drawNowPlaying(mode,canvas):
        if mode.nowPlayingImage != None:
            canvas.create_image(mode.width//2,mode.height//2,image=ImageTk.PhotoImage(mode.nowPlayingImage))
        if mode.nowPlaying != None:
            canvas.create_text(mode.width//2,mode.height//2+100,text=mode.nowPlaying.title,fill=scheme.getAccent1(),font=fonts['accent'])
            canvas.create_text(mode.width//2,mode.height//2+175,text=mode.nowPlaying.artist,fill=scheme.getAccent1(),font=fonts['accent'])
        if mode.repeatCurrent:
            canvas.create_text(mode.width//2,mode.height//2+200,text='repeat current',fill=scheme.getAccent1(),font=fonts['accent2'])
        if mode.nowPlayingSound != None:
            length = 200*((mixer.music.get_pos()//1000)/mode.nowPlayingSound.get_length())
            canvas.create_rectangle(mode.width//2-100,mode.height//1.5,mode.width//2+100,mode.height//1.5+10,fill='white',width=0)
            canvas.create_rectangle(mode.width//2-100,mode.height//1.5,mode.width//2-100+int(length),mode.height//1.5+10,fill=scheme.getAccent2(),width=0)
    
    # def drawQueue(mode,canvas):


    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        canvas.create_text(mode.width//2,mode.height,text='press x to return to selection',fill=scheme.getAccent1(),font=fonts['accent'],anchor='s')
        if mode.selectQueueMode:
            if mode.selectionMode == '':
                mode.drawQueuesForSelection(canvas)
            else:
                mode.drawSelectionMode(canvas)
        else:
            mode.drawPlayerMode(canvas)