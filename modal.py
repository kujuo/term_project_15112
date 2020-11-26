from cmu_112_graphics import *
from design import *

class WelcomeMode(Mode):
    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        canvas.create_text(mode.width//2,mode.height//3,text='yes.',fill=scheme.getAccent1(),font='Ubuntu 24')
        canvas.create_text(mode.width//2,mode.height//2,text='press enter to... you know... enter',fill=scheme.getAccent1(),font='Ubuntu 12')
    
    def keyPressed(mode,event):
        if event.key == 'Enter':
            mode.app.setActiveMode(mode.app.playerMode)
    
class PlayerMode(Mode):
    def appStarted(mode):
        # aaaaaaaaaaaa
        # use mode. instead of self.
        pass

    def timerFired(mode):
        pass

    def mousePressed(mode,event):
        pass

    def keyPressed(mode,event):
        pass

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())

class DataMode(Mode):
    def appStarted(mode):
        # aaaaaaaaaaaa
        # use mode. instead of self.
        pass

    def timerFired(mode):
        pass

    def mousePressed(mode,event):
        pass

    def keyPressed(mode,event):
        pass

    def redrawAll(mode,canvas):
        pass

class HelpMode(Mode):
    def appStarted(mode):
        # aaaaaaaaaaaa
        # use mode. instead of self.
        pass

    def timerFired(mode):
        pass

    def mousePressed(mode,event):
        pass

    def keyPressed(mode,event):
        pass

    def redrawAll(mode,canvas):
        pass

class MyApp(ModalApp):
    def appStarted(app):
        app.welcomeMode = WelcomeMode()
        app.playerMode = PlayerMode()
        app.helpMode = HelpMode()
        app.dataMode = DataMode()

        app.setActiveMode(app.welcomeMode)

app = MyApp(width=500, height=500)