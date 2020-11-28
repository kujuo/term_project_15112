import xml.etree.ElementTree as ET

class SettingsXML(object):
    def __init__(self,filename):
        self.filename = filename
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()

    def writeRootDir(self,data):
        if self.getRootDir() != data:
            self.tree.find('rootdir').text = data
        self.tree.write(self.filename)

    def writeLastFM(self,data):
        if self.getLastFM() != data:
            self.tree.find('lastfm').text = data
        self.tree.write(self.filename)

    def writeColorMode(self,data):
        if self.getColorMode() != data:
            self.tree.find('colormode').text = data
        self.tree.write(self.filename)

    def getRootDir(self):
        return self.tree.find('rootdir').text
    
    def getLastFM(self):
        return self.tree.find('lastfm').text
    
    def getColorMode(self):
        return self.tree.find('colormode').text

settingsXML = SettingsXML('settings.xml')