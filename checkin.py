from cmu_112_graphics import *
from design import *
from xml_io import *
import datetime

# reference for python datetime module:
# https://www.w3schools.com/python/python_datetime.asp
# https://docs.python.org/3/library/datetime.html

class CheckInMode(Mode):
    def appStarted(mode):
        mode.buttons = {
            'type1': (mode.gridBounds(0,0)[0],mode.gridBounds(0,0)[1],
                      mode.gridBounds(0,0)[2],mode.gridBounds(0,0)[3]),
            'type2': (mode.gridBounds(1,0)[0],mode.gridBounds(1,0)[1],
                      mode.gridBounds(1,0)[2],mode.gridBounds(1,0)[3]),
            'type3': (mode.gridBounds(2,0)[0],mode.gridBounds(2,0)[1],
                      mode.gridBounds(2,0)[2],mode.gridBounds(2,0)[3]),
            'type4': (mode.gridBounds(3,0)[0],mode.gridBounds(3,0)[1],
                      mode.gridBounds(3,0)[2],mode.gridBounds(3,0)[3]),
            'type5': (mode.gridBounds(4,0)[0],mode.gridBounds(4,0)[1],
                      mode.gridBounds(4,0)[2],mode.gridBounds(4,0)[3]),
            'type6': (mode.gridBounds(5,0)[0],mode.gridBounds(5,0)[1],
                      mode.gridBounds(5,0)[2],mode.gridBounds(5,0)[3]),
        }
        mode.date = datetime.date.today()
        mode.sessionTime = (datetime.datetime.now().strftime('%H') +
                            datetime.datetime.now().strftime('%M'))

    def gridBounds(mode,row,col):
        buttonWidth = mode.width//15
        buttonHeight = mode.height//15
        gridWidth = 1*buttonWidth
        gridHeight = 6*buttonHeight
        
        x0 = mode.width//3 + buttonWidth * col
        x1 = x0 + buttonWidth
        y0 = mode.height//2 + buttonHeight * row
        y1 = y0 + buttonHeight
        return (x0,y0,x1,y1)


    def timerFired(mode):
        pass

    def mousePressed(mode,event):
        pass

    def keyPressed(mode,event):
        if event.key == 'x':
            mode.app.setActiveMode(mode.app.welcomeMode)
        elif event.key in '123456':
            userXML.setDayType('type'+event.key,mode.date)
            userXML.setDayTime(mode.sessionTime,mode.date)

    def drawButtons(mode,canvas):
        canvas.create_rectangle(mode.buttons['type1'][0],mode.buttons['type1'][1],
                                mode.buttons['type1'][2],mode.buttons['type1'][3],
                                fill=scheme.getTypeColor(1),width=0)
        canvas.create_rectangle(mode.buttons['type2'][0],mode.buttons['type2'][1],
                                mode.buttons['type2'][2],mode.buttons['type2'][3],
                                fill=scheme.getTypeColor(2),width=0)
        canvas.create_rectangle(mode.buttons['type3'][0],mode.buttons['type3'][1],
                                mode.buttons['type3'][2],mode.buttons['type3'][3],
                                fill=scheme.getTypeColor(3),width=0)
        canvas.create_rectangle(mode.buttons['type4'][0],mode.buttons['type4'][1],
                                mode.buttons['type4'][2],mode.buttons['type4'][3],
                                fill=scheme.getTypeColor(4),width=0)
        canvas.create_rectangle(mode.buttons['type5'][0],mode.buttons['type5'][1],
                                mode.buttons['type5'][2],mode.buttons['type5'][3],
                                fill=scheme.getTypeColor(5),width=0)
        canvas.create_rectangle(mode.buttons['type6'][0],mode.buttons['type6'][1],
                                mode.buttons['type6'][2],mode.buttons['type6'][3],
                                fill=scheme.getTypeColor(6),width=0)

    def drawText(mode,canvas):
        canvas.create_text(mode.buttons['type1'][2]+10,(mode.buttons['type1'][1]+mode.buttons['type1'][3])//2,
                           text=settingsXML.getDayType(1),font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(mode.buttons['type2'][2]+10,(mode.buttons['type2'][1]+mode.buttons['type2'][3])//2,
                           text=settingsXML.getDayType(2),font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(mode.buttons['type3'][2]+10,(mode.buttons['type3'][1]+mode.buttons['type3'][3])//2,
                           text=settingsXML.getDayType(3),font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(mode.buttons['type4'][2]+10,(mode.buttons['type4'][1]+mode.buttons['type4'][3])//2,
                           text=settingsXML.getDayType(4),font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(mode.buttons['type5'][2]+10,(mode.buttons['type5'][1]+mode.buttons['type5'][3])//2,
                           text=settingsXML.getDayType(5),font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')
        canvas.create_text(mode.buttons['type6'][2]+10,(mode.buttons['type6'][1]+mode.buttons['type6'][3])//2,
                           text=settingsXML.getDayType(6),font=fonts['accent'],
                           fill=scheme.getAccent1(),anchor='w')

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        mode.drawButtons(canvas)
        mode.drawText(canvas)
        canvas.create_text(mode.width//2,mode.height//3,text=mode.date,fill=scheme.getAccent1(),font=fonts['accent'])
        canvas.create_text(mode.width//2,mode.height,text='press x to return',fill=scheme.getAccent1(),font=fonts['accent'],anchor='s')
