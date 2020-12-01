from cmu_112_graphics import *
# ----
from welcome import *
from checkin import *
from player import *
from data import *
from helpscreen import *
from settings import *


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