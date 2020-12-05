import xml.etree.ElementTree as ET
import os
import datetime

from playlist import *
# from lastfm import *

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
    
    def writeLastCloudSync(self,data):
        data = str(data)
        if self.getLastCloudSync() != data:
            self.tree.find('lastsync').text = data
        self.tree.write(self.filename)

    def getRootDir(self):
        return self.tree.find('rootdir').text
    
    def getLastFM(self):
        return self.tree.find('lastfm').text
    
    def getColorMode(self):
        return self.tree.find('colormode').text
    
    def getLastCloudSync(self):
        return self.tree.find('lastsync').text

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
            if child.attrib['path'] != '':
                songObject = Song(child.attrib['title'].strip(),
                                child.attrib['artist'].strip(),
                                child.attrib['album'].strip(),
                                child.attrib['path'].strip())
                self.allSongs.append(songObject)

    def getAllSongs(self):
        return self.allSongs
    
    def getAllAlbums(self):
        albums = set()
        for song in self.allSongs:
            albums.add((song.album,song.artist))
        albumList = list(albums)
        albumList.sort(key=(lambda L: L[0]))
        return albumList

    def getAllArtists(self):
        artists = set()
        for song in self.allSongs:
            artists.add(song.artist)
        artistsList = list(artists)
        artistsList.sort()
        return artistsList
    
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
        # albumPath = "/" + self.rootdir + "/" + artist + "/" + album + "/"
        for song in self.root.findall('./song/[@album="' + album + '"]'):
            if song.attrib['artist'] == artist:
                songObject = Song(song.attrib['title'],
                                artist,album,
                                song.attrib['path'])
                songs.append(songObject)
        return songs
    
    def getArtistSongs(self,artist):
        songs = []
        # artistPath = "/" + self.rootdir + "/" + artist + "/"
        # for song in self.root.findall('./song/[@path="' + artistPath + '"]'):
        for song in self.root.findall('./song/[@artist="' + artist + '"]'):
            songObject = Song(song.attrib['title'],
                              artist,song.attrib['album'],
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
    
    #TODO: test
    def refreshLibraryFromCloud(self,songDicts):
        for song in songDicts:
            songElem = self.root.find('./song[@title="'+song['title']+'"@album="'+song['album']+'"@artist="'+song['artist']+'"]')
            if songElem != None:
                count = songElem.attrib['playcount']
                songElem.attrib['playcount'] = count + 1
            else:
                songElem = ET.SubElement(self.root,'song')
                songElem.attrib['title'] = song['title']
                songElem.attrib['album'] = song['album']
                songElem.attrib['artist'] = song['artist']
                songElem.attrib['path'] = ''
                songElem.attrib['playcount'] = 1

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

    def getSong(self,songObj):
        return(self.root.find('./song[@path="'+songObj.path+'"]'))

    def getSongTitleMatches(self,songTitle):
        result = self.root.findall('./song[@title="'+songTitle+'"]')
        if result == []:
            print('song not found')
        else:
            return result

class PlaylistsXML(object):
    def __init__(self,filename):
        self.filename = filename
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
    
    def addPlaylist(self,playlist,usermade):
        if self.root.find('./playlist[@title="'+playlist.title+'"]') == None:
            playlistElem = ET.SubElement(self.root,'playlist')
            playlistElem.attrib['title'] = playlist.title
            playlistElem.attrib['length'] = playlist.getLength()
            if usermade:
                playlistElem.attrib['usermade'] = '1'
            else:
                playlistElem.attrib['usermade'] = '0'
        else:
            print('A playlist with that name already exists')

    def updatePlaylist(self,playlist):
        songs = playlist.getSongs()
        for song in songs:
            if self.root.find('./playlist[@title="'+playlist.title+'"]/song[@path="'+song.path+'"]') == None:
                pass
            #TODO:finish


class UserDataXML(object):
    def __init__(self,filename):
        self.filename = filename
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
    
    def setDayType(self,dayType,date):
        date = str(date)
        if date not in ET.tostring(self.root,encoding='utf8').decode('utf8'):
            day = ET.SubElement(self.root,'day')
            day.attrib['date'] = date
            day.attrib['type'] = dayType
        else:
            day = self.root.find('.day[@date="'+date+'"]')
            day.attrib['type'] = dayType
        self.tree.write(self.filename)
    
    def setDayTime(self,dayTime,date):
        date = str(date)
        if date not in ET.tostring(self.root,encoding='utf8').decode('utf8'):
            day = ET.SubElement(self.root,'day')
            day.attrib['date'] = date
            day.attrib['time'] = dayTime
        else:
            day = self.root.find('.day[@date="'+date+'"]')
            day.attrib['time'] = dayTime
        self.tree.write(self.filename)

    def addSongToDay(self,date,songObject):
        date = str(date)
        title = songObject.title
        path = songObject.path
        if self.tree.find('./day[@date="'+date+'"]') == None:
            print(ET.tostring(self.root,encoding='utf8').decode('utf8'))
            day = ET.SubElement(self.root,'day')
            day.attrib['date'] = date
            print(ET.tostring(self.root,encoding='utf8').decode('utf8'))
        if self.tree.find('./day[@date="'+date+'"]/song[@title="'+title+'"]') == None and self.tree.find('./day[@date="'+date+'"]/song[@path="'+path+'"]') == None:
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

    def getSongConsistencyScore(self,songObject):
        daysListened = self.root.findall('./day/song[@path="'+ songObject.path + '"]')
        return len(daysListened)

    def getOneHitWonders(self):
        pass

    def getConsistentFaves(self):
        pass # may need to put these in "songsXML"
    
    # TODO: implement "keep coming back to" songs and "on repeat one hit wonder" songs
    def getSongDayTypeScore(self,currTime,song):
        dHours = abs(int(currTime)//100 - int(song['time'])//100)
        dMinutes = abs(int(currTime)%100 - int(song['time'])%100)
        dTime = datetime.timedelta(
            days=0,
            hours=dHours,
            minutes=dMinutes
        )
        playcount = int(song['playcount'])
        print(playcount/(dTime.seconds+1))
        return playcount/(dTime.seconds+1)

    # TODO: this is uhh really inefficient O(n^2), must be a better way
    def getSongsForDayType(self,dayType,currTime):
        daySongs = []
        result = []
        for day in self.root.getchildren(): # child is a day
            if day.attrib['type'] == dayType:
                songs = day.getchildren()
                for song in songs:
                    song.attrib['time'] = day.attrib['time']
                    daySongs.append(song.attrib)
        i = 0
        while i <= len(daySongs) - 1:
            j = i + 1
            while j < len(daySongs):
                print(i,j)
                if daySongs[i]['path'] == daySongs[j]['path']:
                    print('in here')
                    iCount = int(daySongs[i]['playcount'])
                    iCount += int(daySongs[j]['playcount'])

                    iTime = int(daySongs[i]['time'])
                    jTime = int(daySongs[j]['time'])
                    avgTime = (iTime+jTime)//2
                    daySongs[i]['time'] = str(avgTime)
                    daySongs[i]['playcount'] = str(iCount)
                    daySongs.pop(j)
                else:
                    print('not in here')
                j += 1
            daySongs[i]['score'] = self.getSongDayTypeScore(currTime,daySongs[i])
            i += 1
        daySongs.sort(key=(lambda d: d['score']),reverse=True)
        return daySongs

settingsXML = SettingsXML('./xml_files/settings.xml')
songsXML = SongsXML('./xml_files/songdata.xml',settingsXML.getRootDir())
userXML = UserDataXML('./xml_files/userdata.xml')