# Main file. This is the one to run! Integrates all other files.

from cmu_112_graphics import *
# ----
from welcome import *
from checkin import *
from player import *
from data import *
from helpscreen import *
from settings import *

# referenced course notes: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
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