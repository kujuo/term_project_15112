import xml.etree.ElementTree as ET
import os
import datetime,time

from playlist import *
from lastfm import *

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
        if self.allSongs == []:
            self.addAllSongs()
        albums = set()
        for song in self.allSongs:
            albums.add((song.album,song.artist))
        albumList = list(albums)
        albumList.sort(key=(lambda L: L[0]))
        return albumList

    def getAllArtists(self):
        if self.allSongs == []:
            self.addAllSongs()
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

    def getRankedArtists(self):
        allArtists = self.getAllArtists()
        topArtists = [] # list of dicts, artist:playcount
        for artist in allArtists:
            playcount = self.getArtistPlayCount(artist)
            topArtists.append({
                'artist':artist,
                'playcount':playcount
            })
        topArtists.sort(key=(lambda d: d['playcount']),reverse=True)
        return topArtists

    def getRankedAlbums(self):
        allAlbums = self.getAllAlbums()
        topAlbums = [] # list of dicts, album:playcount
        for album in allAlbums:
            playcount = self.getAlbumPlayCount(album[0])
            topAlbums.append({
                'album':album[0],
                'artist':album[1],
                'playcount':playcount
            })
        topAlbums.sort(key=(lambda d: d['playcount']),reverse=True)
        return topAlbums

    def getAlbumSongs(self,album,artist):
        songs = []
        # albumPath = "/" + self.rootdir + "/" + artist + "/" + album + "/"
        for song in self.root.findall('./song/[@album="' + album + '"]'):
            if song.attrib['artist'] == artist and song.attrib['path'] != '':
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
            if song.attrib['path'] != '':
                songObject = Song(song.attrib['title'],
                                artist,song.attrib['album'],
                                song.attrib['path'])
                songs.append(songObject)
        return songs
    
    def getArtistAlbums(self,artist):
        albums = []
        # TODO: finish implementation

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
    
    def refreshLibraryFromCloud(self,songDicts):
        for song in songDicts:
            title = song['title']
            album = song['album']
            artist = song['artist']
            songElem = self.root.find('./song[@title="'+title+'"]')
            if (songElem != None and 
                songElem.attrib['album'] == album and 
                songElem.attrib['artist'] == artist):
                    count = songElem.attrib['playcount']
                    songElem.attrib['playcount'] = str(int(count) + 1)
            else:
                songElem = ET.SubElement(self.root,'song')
                songElem.attrib['title'] = song['title']
                songElem.attrib['album'] = song['album']
                songElem.attrib['artist'] = song['artist']
                songElem.attrib['path'] = ''
                songElem.attrib['playcount'] = '1'
        self.tree.write(self.filename)

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
    
    def getArtistPlayCount(self,artist):
        count = 0
        for song in self.root.findall('./song/[@artist="' + artist + '"]'):
            count += int(song.attrib['playcount'])
        return count

    def getAlbumPlayCount(self,album):
        count = 0
        for song in self.root.findall('./song/[@album="' + album + '"]'):
            count += int(song.attrib['playcount'])
        return count

    def getSong(self,songObj):
        return(self.root.find('./song[@path="'+songObj.path+'"]'))

    def getSongTitleMatches(self,songTitle):
        result = []
        songs = self.root.findall('./song[@title="'+songTitle+'"]')
        for child in songs:
            if child.attrib['path'] != '':
                result.append(Song(child.attrib['title'].strip(),
                                   child.attrib['artist'].strip(),
                                   child.attrib['album'].strip(),
                                   child.attrib['path'].strip()))
        if result == []:
            print('song not found')
        else:
            return result

    def getTotalPlaycounts(self):
        total = 0
        if self.allSongs == []:
            self.addAllSongs()
        for song in self.allSongs:
            total += self.getPlayCount(song)
        return total
        

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
        self.daysListened = len(self.root.getchildren())
    
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
    
    def getDayType(self,date):
        date = str(date)
        if date not in ET.tostring(self.root,encoding='utf8').decode('utf8'):
            print("check in before getting today's playlist")
            return ''
        # TODO: check for day type existence here
        # elif (self.root.find('./day[@date="'+date+'"]'). == None or
        #       self.root.find('./day[@date="'+date+'"]').attrib['type'] == ''):
        #     print("check in before getting today's playlist")
        #     return ''
        else:
            element = self.root.find('./day[@date="'+date+'"]')
            return element.attrib['type']
    
    def getDayTime(self,date):
        date = str(date)
        if date not in ET.tostring(self.root,encoding='utf8').decode('utf8'):
            print("check in before getting today's playlist")
            return ''
        else:
            element = self.root.find('./day[@date="'+date+'"]')
            return element.attrib['time']

    def addSongToDay(self,date,songObject):
        date = str(date)
        title = songObject.title
        path = songObject.path
        artist = songObject.artist
        album = songObject.album
        if self.tree.find('./day[@date="'+date+'"]') == None:
            day = ET.SubElement(self.root,'day')
            day.attrib['date'] = date
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
        elif self.tree.find('./day[@date="'+date+'"]/song[@title="'+title+'"]').attrib['path'] == '':
            song = self.root.find('.day[@date="'+date+'"]/song[@title="'+title+'"]')
            if song.attrib['artist'] == artist and song.attrib['album'] == album:
                count = int(song.attrib['playcount']) + 1
                song.attrib['playcount'] = str(count)
        else:
            song = self.root.find('.day[@date="'+date+'"]/song[@path="'+path+'"]')
            count = int(song.attrib['playcount']) + 1
            song.attrib['playcount'] = str(count)
        self.tree.write(self.filename)
    
    def addSongsFromCloud(self,songsDict):
        for song in songsDict:
            title = song['title']
            album = song['album']
            artist = song['artist']
            d = time.localtime(int(song['timestamp']))
            year,month,day = str(d[0]),str(d[1]),str(d[2])
            # convert uts seconds to local date using tuple access
            # account for single digit months and dates
            if len(month) == 1:
                month = '0' + month
            if len(day) == 1:
                day = '0' + day
            date = year+'-'+month+'-'+day
            if self.tree.find('./day[@date="'+date+'"]') == None:
                day = ET.SubElement(self.root,'day')
                day.attrib['date'] = date
            songElem = self.root.find('./day[@date="'+date+'"]/song[@title="'+title+'"]')
            if (songElem != None and 
                songElem.attrib['album'] == album and 
                songElem.attrib['artist'] == artist):
                    count = songElem.attrib['playcount']
                    songElem.attrib['playcount'] = str(int(count) + 1)
            else:
                songElem = ET.SubElement(self.tree.find('./day[@date="'+date+'"]'),'song')
                songElem.attrib['title'] = song['title']
                songElem.attrib['album'] = song['album']
                songElem.attrib['artist'] = song['artist']
                songElem.attrib['path'] = ''
                songElem.attrib['playcount'] = '1'
        self.tree.write(self.filename)

    # how often user plays this song across days
    # TODO: modify this to include streamed songs
    def getSongConsistencyScore(self,songObject):
        count = 0
        for song in self.root.findall('./day/song[@title="'+ songObject.title + '"]'):
            if song.attrib['artist'] == songObject.artist:
                count += 1

        return count/self.daysListened

    # songs with high playcounts but low consistency score
    def getOneHitWonders(self):
        result = []
        playlist = Playlist('One Hit Wonders',None)
        topSongs = songsXML.getRankedSongs()
        for song in topSongs.getSongs():
            consistency = self.getSongConsistencyScore(song)
            if consistency != 0:
                score = int(song.playcount)/consistency
                if score != 0:
                    result.append({
                        'title':song.title,
                        'artist':song.artist,
                        'album':song.album,
                        'path':song.path,
                        'playcount':song.playcount,
                        'score':str(score)
                    })
        result.sort(key=(lambda d: d['score']),reverse=True)
        playlist.addSongsDict(result)
        return playlist

    def getConsistentFaves(self):
        result = []
        playlist = Playlist('Feel-good Faves',None)
        topSongs = songsXML.getRankedSongs()
        for song in topSongs.getSongs():
            score = int(song.playcount)*self.getSongConsistencyScore(song)
            if score != 0:
                result.append({
                    'title':song.title,
                    'artist':song.artist,
                    'album':song.album,
                    'path':song.path,
                    'playcount':song.playcount,
                    'score':str(score)
                })
        result.sort(key=(lambda d: d['score']),reverse=True)
        playlist.addSongsDict(result)
        return playlist
    
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
        return playcount/(dTime.seconds+1)

    # TODO: this is uhh really inefficient O(n^2), must be a better way
    def getSongsForDayType(self,dayType,currTime):
        daySongs = []
        result = []
        for day in self.root.getchildren(): # child is a day
            if day.attrib['type'] != None and day.attrib['type'] == dayType:
                songs = day.getchildren()
                for song in songs:
                    if song.attrib['path'] != '':
                        song.attrib['time'] = day.attrib['time']
                        daySongs.append(song.attrib)
        i = 0
        while i <= len(daySongs) - 1:
            j = i + 1
            while j < len(daySongs):
                if daySongs[i]['path'] == daySongs[j]['path']:
                    iCount = int(daySongs[i]['playcount'])
                    iCount += int(daySongs[j]['playcount'])

                    iTime = int(daySongs[i]['time'])
                    jTime = int(daySongs[j]['time'])
                    avgTime = (iTime+jTime)//2
                    daySongs[i]['time'] = str(avgTime)
                    daySongs[i]['playcount'] = str(iCount)
                    daySongs.pop(j)
                j += 1
            daySongs[i]['score'] = self.getSongDayTypeScore(currTime,daySongs[i])
            i += 1
        daySongs.sort(key=(lambda d: d['score']),reverse=True)
        for song in daySongs:
            del song['score']
        return daySongs

    def getDayTopSongs(self,date):
        topSongs = []
        date = str(date)
        if self.tree.find('./day[@date="'+date+'"]') != None:
            for song in self.tree.find('./day[@date="'+date+'"]/song'):
                topSongs.append(song.attrib)
        topSongs.sort(key=(lambda d: d['playcount']),reverse=True)
        return topSongs

    def getDayTotalSongs(self,date):
        total = 0
        date = str(date)
        if self.tree.find('./day[@date="'+date+'"]') != None:
            for song in self.tree.findall('./day[@date="'+date+'"]/song'):
                total += int(song.attrib['playcount'])
        return total
    
    # returns the amount of time listened in one day in seconds
    def getDayListeningTime(self,date):
        time = 0
        date = str(date)
        if self.tree.find('./day[@date="'+date+'"]') != None:
            for song in self.tree.findall('./day[@date="'+date+'"]/song'):
                # print(total,song.attrib['playcount'])
                time += (user.getTrackDurationSeconds(song.attrib))*int(song.attrib['playcount'])
        return int(time)

    # def getWeekTopSongs(self,date):
    #     topSongsSet = set()
    #     topSongs = []
    #     date = str(date)
    #     if self.tree.find('./day[@date="'+date+'"]') != None:
    #         days = self.root.getchildren()
    #         for i in range(8):
    #             for song in days[i].getchildren():
    #                 if (song.attrib['title'],song.attrib['artist']) in topSongsSet:
    #                     topSongs.append(song.attrib)
    #                     # HERE!
    #     topSongs.sort(key=(lambda d: d['playcount']),reverse=True)
    #     return topSongs

    def getTotalListeningTime(self):
        total = 0
        for day in self.root.findall('./day'):
            date = day.attrib['date']
            total += self.getDayListeningTime(date)
        return total
    
    def getTotalListeningDays(self):
        return len(self.root.findall('./day'))

settingsXML = SettingsXML('./xml_files/settings.xml')
songsXML = SongsXML('./xml_files/songdata.xml',settingsXML.getRootDir())
userXML = UserDataXML('./xml_files/userdata.xml')

username = settingsXML.getLastFM()
user = LastFMUser(username)