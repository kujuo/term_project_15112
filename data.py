from cmu_112_graphics import *

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
