import xml.etree.ElementTree as ET
import os

from playlist import *

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

class SongsXML(object):
    def __init__(self,filename):
        self.filename = filename
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
        self.filetypes = ['flac','ogg']
        self.allSongs = set()

    def addAllSongs(self):
        # should be a list of song objects
        for child in self.root.iter('song'):
            songObject = Song(child.getchildren()[0].text.strip(),child.getchildren()[1].text.strip())
            self.allSongs.add(songObject)

    def getAllSongs(self):
        return list(self.allSongs)

    def refreshLibrary(self,rootdir):
        existingSongs = ET.tostring(self.root,encoding='utf8').decode('utf8')
        self.refreshLibraryHelper(rootdir,existingSongs)

    def refreshLibraryHelper(self,rootdir,existingSongs):
        # copied from course notes: https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html
        # Base Case: a file. Just print the path name.
        if os.path.isfile(rootdir):
            extension = os.path.split(rootdir)[1].split('.')[1]
            if extension in self.filetypes:
                songTitle = os.path.split(rootdir)[1].split('.')[0].strip()
                songPath = rootdir.strip()
                # perhaps not the most elegant solution but it works.
                # converts the xml file to a string and makes sure the path and
                # title of the song aren't in the file's string
                if songTitle not in existingSongs and songPath not in existingSongs:
                    song = ET.SubElement(self.root,'song')
                    song.set('title',songTitle)
                    song.set('path',songPath)
                    if song.get('playcount') != None:
                        song.set('playcount',song.get('playcount'))
                    else:
                        song.set('playcount','0')
                    self.tree.write(self.filename)
        else:
            # Recursive Case: a folder. Iterate through its files and folders.
            for filename in os.listdir(rootdir):
                self.refreshLibraryHelper(rootdir + '/' + filename,existingSongs)

    def incrementPlayCount(self,songTitle,songPath):
        song = self.root.find("./song[@path='"+songPath+"']")
        count = int(song.attrib['playcount']) + 1
        song.attrib['playcount'] = str(count)
        self.tree.write(self.filename)


class UserDataXML(object):
    def __init__(self,filename):
        self.filename = filename
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
    
    def setDayColor(self,color):
        pass

    def addSongToDay(self,data):
        pass


settingsXML = SettingsXML('settings.xml')
songsXML = SongsXML('songdata.xml')