from cmu_112_graphics import *

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

