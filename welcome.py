from cmu_112_graphics import *
from design import *
from xml_io import *

class WelcomeMode(Mode):
    def appStarted(mode):
        scheme.setColor(settingsXML.getColorMode())

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        canvas.create_text(mode.width//2,mode.height//3,text='attune.',fill=scheme.getAccent1(),font=fonts['title'])
        canvas.create_text(mode.width//2,mode.height//2,text='press enter to... you know... enter',fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//2+30,text='settings: s',fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//2+50,text='help: h',fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//2+70,text='my stats: d',fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//2+90,text='check in: space',fill=scheme.getAccent1(),font=fonts['accent'])
    
    def keyPressed(mode,event):
        if event.key == 'Enter':
            mode.app.setActiveMode(mode.app.playerMode)
        elif event.key == 's':
            mode.app.setActiveMode(mode.app.settingsMode)
        elif event.key == 'h':
            mode.app.setActiveMode(mode.app.helpMode)
        elif event.key == 'd':
            mode.app.setActiveMode(mode.app.dataMode)
        elif event.key == 'Space':
            mode.app.setActiveMode(mode.app.checkInMode)
