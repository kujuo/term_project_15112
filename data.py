from cmu_112_graphics import *
from lastfm import *
from design import *
from xml_io import *

class DataMode(Mode):
    def appStarted(mode):
        mode.topSongs = songsXML.getRankedSongs().getSongs()[:11]
        mode.images = []
        mode.loadImages()
        mode.currentPosition = 0

    def timerFired(mode):
        pass

    def mousePressed(mode,event):
        pass

    def keyPressed(mode,event):
        if event.key == 'y':
            # print(mode.topSongs)
            print(userXML.getConsistentFaves().getSongs())

    def loadImages(mode):
        for song in mode.topSongs:
            url = user.getAlbumCoverURL(song.album,song.artist)
            image = mode.loadImage(url)
            scale = (songsXML.getPlayCount(song))/(songsXML.getPlayCount(mode.topSongs[0]))
            mode.images.append(mode.scaleImage(image,scale))

    def drawTopSongs(mode,canvas):
        image = mode.images[mode.currentPosition]
        title = mode.topSongs[mode.currentPosition].title
        album = mode.topSongs[mode.currentPosition].album
        artist = mode.topSongs[mode.currentPosition].artist
        playcount = mode.topSongs[mode.currentPosition].playcount
        canvas.create_image(mode.width//2,mode.height//2,image=ImageTk.PhotoImage(image))
        # canvas.create_text(mode.width//2,mode.height//2,text=)
    
    def drawTopSongsText(mode,canvas):
        pass
    # TODO: finish after last.fm integration


    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        mode.drawTopSongs(canvas)
