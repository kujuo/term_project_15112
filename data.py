from cmu_112_graphics import *
from lastfm import *
from design import *
from xml_io import *

class DataMode(Mode):
    def appStarted(mode):
        # aaaaaaaaaaaa
        # use mode. instead of mode.
        mode.topSongs = songsXML.getRankedSongs().getSongs()
        mode.images = []
        mode.loadImages()

    def timerFired(mode):
        pass

    def mousePressed(mode,event):
        pass

    def keyPressed(mode,event):
        if event.key == 'y':
            print(songsXML.getRankedSongs().getSongs())

    def loadImages(mode):
        for song in mode.topSongs:
            url = user.getAlbumCoverURL(song.album,song.artist)
            image = mode.loadImage(url)
            scale = (songsXML.getPlayCount(song))/(songsXML.getPlayCount(mode.topSongs[0]))
            mode.images.append(mode.scaleImage(image,scale))

    def drawTopSongs(mode,canvas):
        yPos = 50
        for image in mode.images:
            canvas.create_image(50,yPos,image=ImageTk.PhotoImage(image))
            yPos += 100

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        mode.drawTopSongs(canvas)
