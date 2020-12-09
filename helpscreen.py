from cmu_112_graphics import *
from design import *

class HelpMode(Mode):
    def appStarted(mode):
        mode.modePos = 0

    def timerFired(mode):
        pass

    def mousePressed(mode,event):
        pass

    def keyPressed(mode,event):
        if event.key == 'x':
            mode.modePos = 0
            mode.app.setActiveMode(mode.app.welcomeMode)
        elif event.key == 'Right':
            mode.modePos += 1
        elif event.key == 'Left':
            mode.modePos -= 1
        elif event.key in '1234':
            mode.modePos = int(event.key)

    def drawMainPage(mode,canvas):
        canvas.create_text(mode.width//2,30,text='welcome to attune.',fill=scheme.getAccent1(),font=fonts['title'])
        canvas.create_text(50,100,text='1. overview',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(50,200,text='2. player screen',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(50,300,text='3. checking in',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(50,400,text='4. stats page',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(50,450,text='press right arrow to continue',fill=scheme.getAccent1(),font=fonts['accent2'],anchor='w')

    def drawOverviewPage(mode,canvas):
        canvas.create_text(mode.width//2,30,text='overview',fill=scheme.getAccent1(),font=fonts['title'])
        canvas.create_text(10,100,text='when you enter attune. for the first time,',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,120,text='the first thing you should do is',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,140,text='set your last.fm username and the',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,160,text='path to your local music in settings',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')

        canvas.create_text(10,200,text='next, check in using the spacebar.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,220,text='you can set custom types of days',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,240,text='and colors in the settings page,',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,260,text='similar to a bullet journal.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')

        canvas.create_text(10,300,text='next, enter the app and play an album,',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,320,text='artist, playlist, or build your own queue.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,340,text='you can build your own queue by typing in song titles.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')

        canvas.create_text(10,370,text='finally, to analyze your listening data, select',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,390,text='the data page. you can navigate using your arrow keys.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')

    def drawPlayerPage(mode,canvas):
        canvas.create_text(mode.width//2,30,text='player',fill=scheme.getAccent1(),font=fonts['title'])
        canvas.create_text(10,100,text='there are a few queues to choose from in the player,',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,120,text='which you can do using the number keys in parentheses.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,140,text='once you have selected a queue, press the spacebar to play.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,160,text='skip/rewind - LR arrow keys, +/- volume - UD arrow keys.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')

        canvas.create_text(10,200,text='shuffle the queue - "s"',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,220,text='save a queue as a playlist - "S"',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,240,text='repeat the current song - "r"',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,260,text='repeat the current queue - "R"',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,280,text="don't track the current song in data = \"i\"",fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')

    def drawCheckinPage(mode,canvas):
        canvas.create_text(mode.width//2,30,text='checking in',fill=scheme.getAccent1(),font=fonts['title'])
        canvas.create_text(10,100,text='attune. users should check in every day.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,120,text='this allows the app to generate customized playlists.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,140,text='you can customize these days in the settings page.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,160,text='press the corresponding digit key to check in.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')

    def drawStatsPage(mode,canvas):
        canvas.create_text(mode.width//2,30,text='your stats',fill=scheme.getAccent1(),font=fonts['title'])
        canvas.create_text(10,100,text='attune. tracks the music you listen to, storing it locally.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,120,text='you can see this data on the data screen.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,140,text='choose which option you want to view, and navigate',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,160,text='through the pages using the arrow keys.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')

        canvas.create_text(10,200,text='it takes a while to load most pages, ',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,220,text='as the album art needs to be pulled from an API.',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')
        canvas.create_text(10,240,text='be patient with it and try not to spam the keys!',fill=scheme.getAccent1(),font=fonts['accent'],anchor='w')

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=scheme.getFill())
        canvas.create_text(mode.width//2,mode.height,text='press x to return',fill=scheme.getAccent1(),font=fonts['accent'],anchor='s')
        if mode.modePos == 0:
            mode.drawMainPage(canvas)
        elif mode.modePos == 1:
            mode.drawOverviewPage(canvas)
        elif mode.modePos == 2:
            mode.drawPlayerPage(canvas)
        elif mode.modePos == 3:
            mode.drawCheckinPage(canvas)
        elif mode.modePos == 4:
            mode.drawStatsPage(canvas)