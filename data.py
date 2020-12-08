from cmu_112_graphics import *
from lastfm import *
from design import *
from xml_io import *
import random

class DataMode(Mode):
    def appStarted(mode):
        mode.images = []
        mode.homeScreen = True
        mode.currentMode = ''
        mode.currentModePos = 0
        mode.currentModeDisplayPos = 0
        mode.viewModes = {
            'top5':['','track','album','artist'],
            'today':['','playback'],
            'week':['playback','listening'],
            'month':['playback','listening'],
            'all time':['','playback'],
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
            'all time':(mode.width//1.5-5,130,
                     mode.width//1.5+5,140),
            'faves':(mode.width//1.5-5,150,
                     mode.width//1.5+5,160),
            'onehits':(mode.width//1.5-5,170,
                     mode.width//1.5+5,180),
        }
        mode.totalListeningTime = 0
        mode.totalSongsListened = 0

    def mousePressed(mode,event):
        pass

    def handleDigitKey(mode,key):
        if mode.homeScreen:
            mode.homeScreen = False
            if key == '1':
                mode.currentMode = 'top5'
            elif key == '2':
                mode.currentMode = 'today'
            elif key == '3':
                mode.currentMode = 'week'
            elif key == '4':
                mode.currentMode = 'month'
            elif key == '5':
                mode.currentMode = 'all time'
            elif key == '6':
                mode.currentMode = 'faves'
            elif key == '7':
                mode.currentMode = 'onehits'
    
    def handleLRKey(mode,key):
        if not mode.homeScreen:
            if key == 'Right':
                mode.currentModeDisplayPos += 1
                maxPos = len(mode.images)-1
                mode.currentModeDisplayPos = min(mode.currentModeDisplayPos,maxPos)
                print(mode.currentMode,mode.currentModeDisplayPos)
            elif key == 'Left':
                mode.currentModeDisplayPos -= 1
                mode.currentModeDisplayPos = max(mode.currentModeDisplayPos,0)
                print(mode.currentMode,mode.currentModeDisplayPos)

    def handleUDKey(mode,key):
        if not mode.homeScreen:
            if key == 'Up':
                mode.currentModePos -= 1
                mode.currentModePos = max(mode.currentModePos,0)
                print(mode.currentMode,mode.currentModePos)
            elif key == 'Down':
                mode.currentModePos += 1
                maxPos = len(mode.viewModes[mode.currentMode])-1
                mode.currentModePos = min(mode.currentModePos,maxPos)
                print(mode.currentMode,mode.currentModePos)
            view = mode.viewModes[mode.currentMode][mode.currentModePos]
            if mode.currentMode == 'top5':
                if  view == 'track':
                    mode.loadTopSongImages()
                elif view == 'album':
                    mode.loadTopAlbumImages()
                elif view == 'artist':
                    mode.loadTopArtistImages()
            elif mode.currentMode == 'today':
                if view == 'playback':
                    mode.loadDayTopSongImages()

    def keyPressed(mode,event):
        if event.key == 't':
            mode.loadWeekTopSongImages()
            # print(mode.images)
        elif event.key == 'x':
            mode.app.setActiveMode(mode.app.welcomeMode)
        elif event.key == 'Right' or event.key == 'Left':
            mode.handleLRKey(event.key)
        elif event.key == 'Up' or event.key == 'Down':
            mode.handleUDKey(event.key)
        elif event.key in '1234567890':
            mode.handleDigitKey(event.key)
        
    def loadAllTimeImages(mode):
        mode.images = []
        topSong = songsXML.getRankedSongs().getSongs()[0]
        topArtist = songsXML.getRankedArtists()[0]
        songUrl = user.getAlbumCoverURL(topSong.album,topSong.artist)
        songImage = mode.loadImage(songUrl)
        artistUrl = user.getArtistImgURL(topArtist)
        artistImage = mode.loadImage(artistUrl)
        mode.images += [songImage,artistImage]
        mode.totalSongsListened = songsXML.getTotalPlaycounts()
        mode.totalListeningTime = userXML.getTotalListeningTime()//60

    # def loadWeekTopSongImages(mode):
    #     mode.images = []
    #     topSongs = userXML.getWeekTopSongs(datetime.date.today())[:5]
    #     for song in topSongs:
    #         url = user.getAlbumCoverURL(song['album'],song['artist'])
    #         image = mode.loadImage(url)
    #         scale = 0.5
    #         mode.images.append((mode.scaleImage(image,scale),song['title'],song['artist'],song['playcount']))
            # mode.totalListeningTime = int(userXML.getWeekListeningTime(datetime.date.today()))//60

    def loadDayTopSongImages(mode):
        mode.images = []
        topSongs = userXML.getDayTopSongs(datetime.date.today())[:5]
        for song in topSongs:
            url = user.getAlbumCoverURL(song['album'],song['artist'])
            image = mode.loadImage(url)
            # scale = (songsXML.getPlayCount(song))/(songsXML.getPlayCount(topSongs[0]))
            scale = 0.5
            mode.images.append((mode.scaleImage(image,scale),song['title'],song['artist'],song['playcount']))
            mode.totalListeningTime = int(userXML.getDayListeningTime(datetime.date.today()))//60
            mode.totalSongsListened = int(userXML.getDayTotalSongs(datetime.date.today()))

    def loadTopSongImages(mode):
        mode.images = []
        topSongs = songsXML.getRankedSongs().getSongs()[:6]
        for song in topSongs:
            url = user.getAlbumCoverURL(song.album,song.artist)
            image = mode.loadImage(url)
            # scale = (songsXML.getPlayCount(song))/(songsXML.getPlayCount(topSongs[0]))
            scale = 1
            mode.images.append((mode.scaleImage(image,scale),song.title,song.artist,song.playcount))
    
    def loadTopAlbumImages(mode):
        mode.images = []
        topAlbums = songsXML.getRankedAlbums()[:6]
        topAlbumPlaycount = int(topAlbums[0]['playcount'])
        for element in topAlbums:
            url = user.getAlbumCoverURL(element['album'],element['artist'])
            image = mode.loadImage(url)
            # scale = int(element['playcount'])/topAlbumPlaycount
            scale = 1
            mode.images.append((mode.scaleImage(image,scale),element['album'],element['artist'],element['playcount']))
    
    def loadTopArtistImages(mode):
        mode.images = []
        topArtists = songsXML.getRankedArtists()[:6]
        topArtistPlaycount = int(topArtists[0]['playcount'])
        for element in topArtists:
            url = user.getArtistImgURL(element['artist'])
            image = mode.loadImage(url)
            # scale = int(element['playcount'])/topArtistPlaycount
            scale = 1
            mode.images.append((mode.scaleImage(image,scale),element['artist'],element['playcount']))

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
        canvas.create_text(50,(mode.homeButtons['all time'][1]+mode.homeButtons['all time'][3])//2,
                               text="all time stats ( 5 )",font=fonts['accent'],
                               fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.homeButtons['faves'][1]+mode.homeButtons['faves'][3])//2,
                               text="favorites ( 6 )",font=fonts['accent'],
                               fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.homeButtons['onehits'][1]+mode.homeButtons['onehits'][3])//2,
                               text="your one-hit wonders ( 7 )",font=fonts['accent'],
                               fill=scheme.getAccent1(),anchor='w')

    def drawDataPage(mode,canvas):
        if mode.currentMode == 'top5':
            mode.drawTop5(canvas)
        elif mode.currentMode == 'today':
            mode.drawToday(canvas)
        elif mode.currentMode == 'week':
            pass
        elif mode.currentMode == 'month':
            pass
        elif mode.currentMode == 'all time':
            mode.drawAllTime(canvas)
        elif mode.currentMode == 'faves':
            pass
        elif mode.currentMode == 'onehits':
            pass
            # draw # of tracks listened to, 

    def drawTop5(mode,canvas):
        view = mode.viewModes[mode.currentMode][mode.currentModePos]
        if view == '':
            canvas.create_text(mode.width//2,mode.height//2,text='your top 5s',fill=scheme.getAccent1(),font=fonts['title'])
            canvas.create_text(mode.width//2,mode.height-50,text='press down arrow to continue',fill=scheme.getAccent1(),font=fonts['accent'])
        else:
            if view == 'track':
                mode.drawTop5Tracks(canvas)
            elif view == 'album':
                mode.drawTop5Albums(canvas)
            elif view == 'artist':
                mode.drawTop5Artists(canvas)

    def drawTop5Tracks(mode,canvas):
        canvas.create_text(mode.width//2,50,text='your top 5 songs',fill=scheme.getAccent1(),font=fonts['title'])
        image = mode.images[mode.currentModeDisplayPos][0]
        title = mode.images[mode.currentModeDisplayPos][1]
        artist = mode.images[mode.currentModeDisplayPos][2]
        playcount = mode.images[mode.currentModeDisplayPos][3]
        canvas.create_image(mode.width//2,mode.height//2,image=ImageTk.PhotoImage(image))
        canvas.create_text(mode.width//2,mode.height//2+100,text=title,fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//2+150,text=artist,fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//2+200,text=str(playcount),fill=scheme.getAccent1(),font=fonts['accent'])

    def drawTop5Albums(mode,canvas):
        canvas.create_text(mode.width//2,50,text='your top 5 albums',fill=scheme.getAccent1(),font=fonts['title'])
        image = mode.images[mode.currentModeDisplayPos][0]
        album = mode.images[mode.currentModeDisplayPos][1]
        artist = mode.images[mode.currentModeDisplayPos][2]
        playcount = mode.images[mode.currentModeDisplayPos][3]
        canvas.create_image(mode.width//2,mode.height//2,image=ImageTk.PhotoImage(image))
        canvas.create_text(mode.width//2,mode.height//2+100,text=album,fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//2+150,text=artist,fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//2+200,text=str(playcount),fill=scheme.getAccent1(),font=fonts['accent'])

    def drawTop5Artists(mode,canvas):
        canvas.create_text(mode.width//2,50,text='your top 5 artists',fill=scheme.getAccent1(),font=fonts['title'])
        image = mode.images[mode.currentModeDisplayPos][0]
        artist = mode.images[mode.currentModeDisplayPos][1]
        playcount = mode.images[mode.currentModeDisplayPos][2]
        canvas.create_image(mode.width//2,mode.height//2,image=ImageTk.PhotoImage(image))
        canvas.create_text(mode.width//2,mode.height//2+150,text=artist,fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//2+200,text=str(playcount),fill=scheme.getAccent1(),font=fonts['accent'])

    def drawToday(mode,canvas):
        view = mode.viewModes[mode.currentMode][mode.currentModePos]
        if view == '':
            canvas.create_text(mode.width//2,mode.height//2,text="today's stats",fill=scheme.getAccent1(),font=fonts['title'])
            canvas.create_text(mode.width//2,mode.height//2+100,text=str(datetime.date.today()),fill=scheme.getAccent1(),font=fonts['accent'])
            canvas.create_text(mode.width//2,mode.height-50,text='press down arrow to continue',fill=scheme.getAccent1(),font=fonts['accent'])
        elif view == 'playback':
            canvas.create_text(10,20,text="today's top songs",fill=scheme.getAccent1(),font=fonts['title']+' underline',anchor='w')
            dHeight = 20
            for element in mode.images:
                canvas.create_text(10,40+dHeight*1.5,text=element[1]+ ': '+element[3],fill=scheme.getAccent2(),font=fonts['accent'],anchor='w')
                canvas.create_image(mode.width-dHeight*2.9,dHeight*2.9,image=ImageTk.PhotoImage(element[0]))
                dHeight += 30
            
            canvas.create_text(mode.width-10,mode.height-180,text=str(mode.totalSongsListened),fill=scheme.getAccent2(),font=fonts['title'],anchor='e')
            canvas.create_text(mode.width-10,mode.height-150,text='songs',fill=scheme.getAccent1(),font=fonts['accent2'],anchor='e')

            canvas.create_text(mode.width-10,mode.height-100,text='listening time',fill=scheme.getAccent1(),font=fonts['accent']+' underline',anchor='e')
            canvas.create_text(mode.width-10,mode.height-50,text=str(mode.totalListeningTime),fill=scheme.getAccent2(),font=fonts['title'],anchor='e')
            canvas.create_text(mode.width-10,mode.height-20,text='minutes',fill=scheme.getAccent1(),font=fonts['accent2'],anchor='e')
    
    # def drawWeek(mode,canvas):
    #     pass

    def drawAllTime(mode,canvas):
        view = mode.viewModes[mode.currentMode][mode.currentModePos]
        if view == '':
            canvas.create_text(mode.width//2,mode.height//2,text="your all-time stats",fill=scheme.getAccent1(),font=fonts['title'])
            canvas.create_text(mode.width//2,mode.height//2+100,text='listening for: '+ str(userXML.getTotalListeningDays())+' days',fill=scheme.getAccent1(),font=fonts['accent'])
            canvas.create_text(mode.width//2,mode.height-50,text='press down arrow to continue',fill=scheme.getAccent1(),font=fonts['accent'])
        elif view == 'playback':
            canvas.create_text(50,10,text=str(mode.totalSongsListened),fill=scheme.getAccent2(),font=fonts['title'],anchor='nw')
            canvas.create_text(50,60,text='songs',fill=scheme.getAccent1(),font=fonts['accent2'],anchor='nw')

            canvas.create_text(mode.width-50,10,text=str(mode.totalListeningTime),fill=scheme.getAccent2(),font=fonts['title'],anchor='ne')
            canvas.create_text(mode.width-50,60,text='minutes',fill=scheme.getAccent1(),font=fonts['accent2'],anchor='ne')

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        if mode.homeScreen:
            mode.drawHomePage(canvas)
        else:
            mode.drawDataPage(canvas)
