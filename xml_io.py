import xml.etree.ElementTree as ET
import os

from playlist import *

# referenced the following websites for XML IO syntax,
# and tips on handling XML files. No code was copied.
# https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/
# https://docs.python.org/3/library/xml.etree.elementtree.html
# https://www.datacamp.com/community/tutorials/python-xml-elementtree
# https://www.tutorialspoint.com/python/python_xml_processing.htm

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
        self.allSongs = []

    def addAllSongs(self):
        # should be a list of song objects
        for child in self.root.iter('song'):
            songObject = Song(child.attrib['title'].strip(),
                              child.attrib['artist'].strip(),
                              child.attrib['album'].strip(),
                              child.attrib['path'].strip())
            self.allSongs.append(songObject)

    def getAllSongs(self):
        return self.allSongs

    def refreshLibrary(self,rootdir):
        existingSongs = ET.tostring(self.root,encoding='utf8').decode('utf8')
        self.refreshLibraryHelper(rootdir,existingSongs)

    def refreshLibraryHelper(self,rootdir,existingSongs):
        # modified from course notes: https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html
        # Base Case: a file. Just print the path name.
        if os.path.isfile(rootdir):
            extension = os.path.split(rootdir)[1].split('.')[1]
            if extension in self.filetypes:
                songTitle = os.path.split(rootdir)[1].split('.')[0].strip()
                splitPath = os.path.split(rootdir)[0].split('/')
                songArtist = splitPath[len(splitPath)-2]
                songAlbum = splitPath[len(splitPath)-1]
                songPath = rootdir.strip()
                # perhaps not the most elegant solution but it works.
                # converts the xml file to a string and makes sure the path and
                # title of the song aren't in the file's string
                if songTitle not in existingSongs and songPath not in existingSongs:
                    song = ET.SubElement(self.root,'song')
                    song.set('title',songTitle)
                    song.set('path',songPath)
                    song.set('artist',songArtist)
                    song.set('album',songAlbum)
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

class PlaylistsXML(object):
    def __init__(self,filename):
        self.filename = filename
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()


class UserDataXML(object):
    def __init__(self,filename):
        self.filename = filename
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
    
    # add check to make sure that can only check in once a day
    def setDayColor(self,color,date):
        if date not in ET.tostring(self.root,encoding='utf8').decode('utf8'):
            day = ET.SubElement(self.root,'day')
            day.attrib['date'] = date
            day.attrib['color'] = color
            self.tree.write(self.filename)

    def addSongToDay(self,date,songObject):
        # don't use f strings, but can make it work with first method
        # if self.tree.find(f"./day[@date='{date}'/song[@title='{songTitle}']") == None and self.tree.find(f"./day[@date='{date}'/song[@path='{songPath}']") == None:
        if songPath not in ET.tostring(self.root.getchildren()[len(self.root.getchildren())-1],encoding='utf8').decode('utf8'):
            song = ET.SubElement(self.tree.find(f"./day[@date='{date}']"),'song')
            song.set('title',songObject.title)
            song.set('artist',songObject.artist)
            song.set('album',songObject.album)
            song.set('path',songObject.path)
            if song.get('playcount') != None:
                song.set('playcount',song.get('playcount'))
            else:
                song.set('playcount','1')
        else:
            song = self.root.find(".day/song[@path='"+songPath+"']")
            count = int(song.attrib['playcount']) + 1
            song.attrib['playcount'] = str(count)
        self.tree.write(self.filename)


settingsXML = SettingsXML('./xml_files/settings.xml')
songsXML = SongsXML('./xml_files/songdata.xml')
userXML = UserDataXML('./xml_files/userdata.xml')