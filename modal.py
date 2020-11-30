from cmu_112_graphics import *
from design import *
from lastfm import *
from xml_io import *
from pygame import mixer
import math,datetime

fonts = {
    'title':'Ubuntu 24',
    'accent':'Ubuntu 12'
}

class WelcomeMode(Mode):
    def appStarted(mode):
        scheme.setColor(settingsXML.getColorMode())

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        canvas.create_text(mode.width//2,mode.height//3,text='Welcome to Hell.',fill=scheme.getAccent1(),font=fonts['title'])
        canvas.create_text(mode.width//2,mode.height//2,text='press enter to... you know... enter',fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//1.8,text='settings: s',fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//1.65,text='help: h',fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height//1.5,text='check in: space',fill=scheme.getAccent1(),font=fonts['accent'])
    
    def keyPressed(mode,event):
        if event.key == 'Enter':
            mode.app.setActiveMode(mode.app.playerMode)
        elif event.key == 's':
            mode.app.setActiveMode(mode.app.settingsMode)
        elif event.key == 'h':
            mode.app.setActiveMode(mode.app.helpMode)
        elif event.key == 'Space':
            mode.app.setActiveMode(mode.app.checkInMode)

class CheckInMode(Mode):
    def appStarted(mode):
        mode.date = datetime.date.today()

    def timerFired(mode):
        pass

    def mousePressed(mode,event):
        pass

    def keyPressed(mode,event):
        if event.key == 'x':
            mode.app.setActiveMode(mode.app.welcomeMode)

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        canvas.create_text(mode.width//2,mode.height//3,text=mode.date,fill=scheme.getAccent1(),font=fonts['accent'])

    
class PlayerMode(Mode):
    def appStarted(mode):
        mode.allSongs = songsXML.getAllSongs()

    def timerFired(mode):
        pass

    def mousePressed(mode,event):
        print(mode.allSongs)

    def keyPressed(mode,event):
        pass

    def drawQueue(mode,canvas):
        pass

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())

class DataMode(Mode):
    def appStarted(mode):
        # aaaaaaaaaaaa
        # use mode. instead of mode.
        pass

    def timerFired(mode):
        pass

    def mousePressed(mode,event):
        pass

    def keyPressed(mode,event):
        pass

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())

class HelpMode(Mode):
    def appStarted(mode):
        # aaaaaaaaaaaa
        # use mode. instead of mode.
        pass

    def timerFired(mode):
        pass

    def mousePressed(mode,event):
        pass

    def keyPressed(mode,event):
        if event.key == 'x':
            mode.app.setActiveMode(mode.app.welcomeMode)


    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        canvas.create_text(mode.width//2,mode.height,text='press x to return',fill=scheme.getAccent1(),font=fonts['accent'],anchor='s')


class SettingsMode(Mode):
    # change path to music directory
    # enter last.fm username
    def appStarted(mode):
        mode.buttons = {
            'root': (mode.width//1.5-5,mode.height//4-5,
                           mode.width//1.5+5,mode.height//4+5),
            'last.fm': (mode.width//1.5-5,mode.height//2-5,
                               mode.width//1.5+5,mode.height//2+5),
            'color': (mode.width//1.5-5,3*mode.height//4-5,
                               mode.width//1.5+5,3*mode.height//4+5),
            'refresh': (mode.width//1.5-5,3*mode.height//3.5-5,
                               mode.width//1.5+5,3*mode.height//3.5+5),
        }
        mode.rootDir = settingsXML.getRootDir()
        mode.lastfmUser = settingsXML.getLastFM()

    def rootClicked(mode,x,y):
        return (mode.buttons['root'][0] <= x <= mode.buttons['root'][2] and
                mode.buttons['root'][1] <= y <= mode.buttons['root'][3])
    
    def lastfmClicked(mode,x,y):
        return (mode.buttons['last.fm'][0] <= x <= mode.buttons['last.fm'][2] and
                mode.buttons['last.fm'][1] <= y <= mode.buttons['last.fm'][3])

    def colorClicked(mode,x,y):
        return (mode.buttons['color'][0] <= x <= mode.buttons['color'][2] and
                mode.buttons['color'][1] <= y <= mode.buttons['color'][3])

    def refreshClicked(mode,x,y):
        return (mode.buttons['refresh'][0] <= x <= mode.buttons['refresh'][2] and
                mode.buttons['refresh'][1] <= y <= mode.buttons['refresh'][3])

    def mousePressed(mode,event):
        if mode.rootClicked(event.x,event.y):
            mode.rootDir = mode.getUserInput('enter path to root music directory')
        elif mode.lastfmClicked(event.x,event.y):
            mode.lastfmUser = mode.getUserInput('enter last.fm username')
        elif mode.colorClicked(event.x,event.y):
            if scheme.getColor() == 'dark':
                scheme.setColor('light')
            elif scheme.getColor() == 'light':
                scheme.setColor('dark')
        elif mode.refreshClicked(event.x,event.y):
            mode.handleChange()

    def handleChange(mode):
        settingsXML.writeRootDir(mode.rootDir)
        settingsXML.writeLastFM(mode.lastfmUser)
        settingsXML.writeColorMode(scheme.getColor())
        # songsXML.addAllSongs()
        songsXML.refreshLibrary(mode.rootDir)

    def keyPressed(mode,event):
        if event.key == 'x':
            mode.handleChange()
            mode.app.setActiveMode(mode.app.welcomeMode)
        elif event.key == 'p':
            mode.rootDir = mode.getUserInput('enter path to root music directory')
        elif event.key == 'l':
            mode.lastfmUser = mode.getUserInput('enter last.fm username')
        elif event.key == 'd':
            if scheme.getColor() == 'dark':
                scheme.setColor('light')
            elif scheme.getColor() == 'light':
                scheme.setColor('dark')
        elif event.key == 'r':
            mode.handleChange()


    def drawButtons(mode,canvas):
        canvas.create_rectangle(mode.buttons['root'][0],mode.buttons['root'][1],
                                mode.buttons['root'][2],mode.buttons['root'][3],
                                fill=scheme.getAccent1(),width=0)
        canvas.create_rectangle(mode.buttons['last.fm'][0],mode.buttons['last.fm'][1],
                                mode.buttons['last.fm'][2],mode.buttons['last.fm'][3],
                                fill=scheme.getAccent1(),width=0)
        canvas.create_rectangle(mode.buttons['color'][0],mode.buttons['color'][1],
                                mode.buttons['color'][2],mode.buttons['color'][3],
                                fill=scheme.getAccent1(),width=0)
        canvas.create_rectangle(mode.buttons['refresh'][0],mode.buttons['refresh'][1],
                                mode.buttons['refresh'][2],mode.buttons['refresh'][3],
                                fill=scheme.getAccent1(),width=0)
    
    def drawText(mode,canvas):
        canvas.create_text(50,(mode.buttons['root'][1]+mode.buttons['root'][3])//2,
                           text='set path to music directory ( p )',font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.buttons['last.fm'][1]+mode.buttons['last.fm'][3])//2,
                           text='sync last.fm account ( l )',font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(50,(mode.buttons['color'][1]+mode.buttons['color'][3])//2,
                           text='toggle dark mode ( d )',font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        canvas.create_text(mode.width//2,mode.height,text='press x to return',fill=scheme.getAccent1(),font=fonts['accent'],anchor='s')
        mode.drawButtons(canvas)
        mode.drawText(canvas)



class MyApp(ModalApp):
    def appStarted(app):
        app.welcomeMode = WelcomeMode()
        app.playerMode = PlayerMode()
        app.helpMode = HelpMode()
        app.settingsMode = SettingsMode()
        app.dataMode = DataMode()
        app.checkInMode = CheckInMode()

        app.setActiveMode(app.welcomeMode)

app = MyApp(width=500, height=500)