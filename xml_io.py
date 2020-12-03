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
    def __init__(self,filename,rootdir):
        self.filename = filename
        self.rootdir = rootdir
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
    
    # reference for lambda functions:
    # https://www.w3schools.com/python/python_lambda.asp
    def getRankedSongs(self):
        topSongs = []
        playlist = Playlist('Top Songs',None)
        for child in self.root.getchildren():
            if child.attrib['playcount'] != '0':
                topSongs.append(child.attrib)
        topSongs.sort(key=(lambda d: d['playcount']),reverse=True)
        playlist.addSongsDict(topSongs)
        return playlist

    def getAlbumSongs(self,album,artist):
        songs = []
        albumPath = "/" + self.rootdir + "/" + artist + "/" + album + "/"
        for song in self.root.findall('./song/[@path="' + albumPath + '"]'):
            songObject = Song(song.attrib['title'],
                              artist,album,
                              song.attrib['path'])
            songs.append(songObject)
        return songs
    
    def getArtistSongs(self,artist):
        songs = []
        artistPath = "/" + self.rootdir + "/" + artist + "/"
        for song in self.root.findall('./song/[@path="' + albumPath + '"]'):
            songObject = Song(song.attrib['title'],
                              artist,album,
                              song.attrib['path'])
            songs.append(songObject)
        return songs
    
    def getArtistAlbums(self,artist):
        albums = []


    def refreshLibrary(self):
        existingSongs = ET.tostring(self.root,encoding='utf8').decode('utf8')
        self.refreshLibraryHelper(self.rootdir,existingSongs)

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

    def incrementPlayCount(self,songPath):
        song = self.root.find('./song[@path="'+songPath+'"]')
        count = int(song.attrib['playcount']) + 1
        song.attrib['playcount'] = str(count)
        self.tree.write(self.filename)

    def getPlayCount(self,song):
        title = song.title
        path = song.path
        count = self.root.find('./song[@path="'+path+'"]').attrib['playcount']
        return int(count)

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
        date = str(date)
        if date not in ET.tostring(self.root,encoding='utf8').decode('utf8'):
            day = ET.SubElement(self.root,'day')
            day.attrib['date'] = date
            day.attrib['color'] = color
            self.tree.write(self.filename)

    def addSongToDay(self,date,songObject):
        date = str(date)
        title = songObject.title
        path = songObject.path
        # don't use f strings, but can make it work with first method
        # if self.tree.find(f"./day[@date='{date}'/song[@title='{songTitle}']") == None and self.tree.find(f"./day[@date='{date}'/song[@path='{songPath}']") == None:
        if self.tree.find('./day[@date="'+date+'"]') == None:
        # if date not in ET.tostring(self.root,encoding='utf8').decode('utf8'):
            print(ET.tostring(self.root,encoding='utf8').decode('utf8'))
            day = ET.SubElement(self.root,'day')
            day.attrib['date'] = date
            print(ET.tostring(self.root,encoding='utf8').decode('utf8'))
        if self.tree.find('./day[@date="'+date+'"]/song[@title="'+title+'"]') == None and self.tree.find('./day[@date="'+date+'"]/song[@path="'+path+'"]') == None:
        # if songObject.path not in ET.tostring(self.root.getchildren()[len(self.root.getchildren())-1],encoding='utf8').decode('utf8'):
            song = ET.SubElement(self.tree.find('./day[@date="'+date+'"]'),'song')
            song.set('title',songObject.title)
            song.set('artist',songObject.artist)
            song.set('album',songObject.album)
            song.set('path',songObject.path)
            if song.get('playcount') != None:
                song.set('playcount',song.get('playcount'))
            else:
                song.set('playcount','1')
        else:
            song = self.root.find('.day/song[@path="'+songPath+'"]')
            count = int(song.attrib['playcount']) + 1
            song.attrib['playcount'] = str(count)
        self.tree.write(self.filename)

    def getSongsForDayType(self,dayType):
        daySongs = []
        for day in self.root.getchildren(): # child is a day
            if day.attrib['type'] == dayType:
                songs = day.getchildren()
                for song in songs:
                    if song not in daySongs:
                        daySongs.append(song.attrib)
                    else:
                        daySongs
        daySongs.sort(key=(lambda d: d['playcount']),reverse=True)
        playlist.addSongsDict(topSongs)
        return playlist
                    
        


settingsXML = SettingsXML('./xml_files/settings.xml')
songsXML = SongsXML('./xml_files/songdata.xml',settingsXML.getRootDir())
userXML = UserDataXML('./xml_files/userdata.xml')