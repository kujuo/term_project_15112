from cmu_112_graphics import *
from lastfm import *
from design import *
from xml_io import *

class DataMode(Mode):
    def appStarted(mode):
        mode.images = []
        mode.homeScreen = True
        mode.currentMode = ''
        mode.currentModePos = 0
        mode.viewModes = {
            'top5':['track','artist','album'],
            'today':['playbackstats','listeningstats'],
            'week':['playbackstats','listeningstats'],
            'month':['playbackstats','listeningstats'],
            'faves':['track','artist','album'],
            'onehits':['track']
        }
        mode.homeButtons = {
            'top5':(mode.width//1.5-5,50,
                   mode.width//1.5+5,60),
            'today':(mode.width//1.5-5,70,
                      mode.width//1.5+5,80),
            'week':(mode.width//1.5-5,90,
                     mode.width//1.5+5,100),
            'month':(mode.width//1.5-5,110,
                        mode.width//1.5+5,120),
            'faves':(mode.width//1.5-5,130,
                     mode.width//1.5+5,140),
            'onehits':(mode.width//1.5-5,150,
                     mode.width//1.5+5,160),
        }
        # mode.currentPosition = 0

    def mousePressed(mode,event):
        pass

    def handleDigitKey(mode,key):
        if mode.homeScreen:
            mode.homeScreen = False
            if key == '1':
                mode.currentMode = 'top5'
                mode.loadTopSongImages()
            elif key == '2':
                mode.currentMode = 'today'
            elif key == '3':
                mode.currentMode = 'week'
            elif key == '4':
                mode.currentMode = 'month'
            elif key == '5':
                mode.currentMode = 'faves'
            elif key == '6':
                mode.currentMode = 'onehits'
    
    def handleLRKey(mode,key):
        if not mode.homeScreen:
            if key == 'Right':
                mode.currentModePos += 1
                print(mode.currentMode,mode.currentModePos)
            elif key == 'Left':
                mode.currentModePos -= 1
                print(mode.currentMode,mode.currentModePos)

    def keyPressed(mode,event):
        if event.key == 't': #TODO: delete after finished testing
            # print(mode.topSongs)
            print(userXML.getDayListeningTime('2020-12-04'))
        elif event.key == 'Right' or event.key == 'Left':
            mode.handleLRKey(event.key)
        elif event.key in '1234567890':
            mode.handleDigitKey(event.key)
        

    def loadTopSongImages(mode):
        mode.images = []
        topSongs = songsXML.getRankedSongs().getSongs()[:6]
        for song in topSongs:
            url = user.getAlbumCoverURL(song.album,song.artist)
            image = mode.loadImage(url)
            scale = (songsXML.getPlayCount(song))/(songsXML.getPlayCount(topSongs[0]))
            mode.images.append((mode.scaleImage(image,scale),song.title,song.artist))
    
    def loadTopAlbumImages(mode):
        mode.images = []
        topAlbums = songsXML.getRankedAlbums()[:6]
        topAlbumPlaycount = int(topAlbums[0]['playcount'])
        for element in topAlbums:
            url = user.getAlbumCoverURL(element['album'],element['artist'])
            image = mode.loadImage(url)
            scale = int(element['playcount'])/topAlbumPlaycount
            mode.images.append(mode.scaleImage(image,scale))
    
    def loadTopArtistImages(mode):
        mode.images = []
        topArtists = songsXML.getRankedArtists()[:6]
        topArtistPlaycount = int(topArtists[0]['playcount'])
        for element in topArtists:
            url = user.getArtistImgURL(element['artist'])
            image = mode.loadImage(url)
            scale = int(element['playcount'])/topArtistPlaycount
            mode.images.append(mode.scaleImage(image,scale))

    def drawHomePage(mode,canvas):
        canvas.create_text(50,(mode.homeButtons['top5'][1]+mode.homeButtons['top5'][3])//2,
                               text='top 5 stats ( 1 )',font=fonts['accent'],
                               fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.homeButtons['today'][1]+mode.homeButtons['today'][3])//2,
                               text="today's stats ( 2 )",font=fonts['accent'],
                               fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.homeButtons['week'][1]+mode.homeButtons['week'][3])//2,
                           text="this week's stats ( 3 )",font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.homeButtons['month'][1]+mode.homeButtons['month'][3])//2,
                           text="this month's stats ( 4 )",font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.homeButtons['faves'][1]+mode.homeButtons['faves'][3])//2,
                           text="favorites ( 5 )",font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.homeButtons['onehits'][1]+mode.homeButtons['onehits'][3])//2,
                           text="your one-hit wonders ( 6 )",font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')

    def drawDataPage(mode,canvas):
        if mode.currentMode == 'top5':
            mode.drawTop5(canvas)
        elif mode.currentMode == 'today':
            pass
        elif mode.currentMode == 'week':
            pass
        elif mode.currentMode == 'month':
            pass
        elif mode.currentMode == 'faves':
            pass
        elif mode.currentMode == 'onehits':
            pass
            # draw # of tracks listened to, 

    def drawTop5(mode,canvas):
        view = mode.viewModes[mode.currentMode][mode.currentModePos]
        mode.drawTop5Tracks(canvas) # TODO: comment out after testing
        # if  view == 'track':
        #     mode.drawTop5Tracks(canvas)
        # elif view == 'album':
        #     mode.drawTop5Albums(canvas)
        # elif view == 'artist':
        #     mode.drawTop5Artists(canvas)

    def drawTop5Tracks(mode,canvas):
        canvas.create_text(mode.width//2,50,text='Your top 5 songs',fill=scheme.getAccent1(),font=fonts['title'])
        image = mode.images[mode.currentModePos][0]
        title = mode.images[mode.currentModePos][1]
        # album = mode.topSongs[mode.currentModePos].album
        artist = mode.images[mode.currentModePos][2]
        # playcount = mode.topSongs[mode.currentPosition].playcount
        canvas.create_image(mode.width//2,mode.height//2,image=ImageTk.PhotoImage(image))
        canvas.create_text(mode.width//2,mode.height//2+100,text=title,fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//2+150,text=artist,fill=scheme.getAccent1(),font=fonts['accent'])
        # canvas.create_text(mode.width//2,mode.height//2+175,text=album)

    def drawTop5Albums(mode,canvas):
        canvas.create_text(mode.width//2,50,text='Your top 5 albums',fill=scheme.getAccent1(),font=fonts['title'])

    def drawTop5Artists(mode,canvas):
        canvas.create_text(mode.width//2,50,text='Your top 5 artists',fill=scheme.getAccent1(),font=fonts['title'])

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        if mode.homeScreen:
            mode.drawHomePage(canvas)
        else:
            mode.drawDataPage(canvas)
        # mode.drawTopSongs(canvas)
