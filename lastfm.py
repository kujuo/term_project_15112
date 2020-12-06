import requests
from apikey import *
from playlist import *
import xml.etree.ElementTree as ET

# referenced these websites for help on syntax/methods
# https://www.dataquest.io/blog/last-fm-api-python/
# https://www.last.fm/api/

# all nusic-related images (album covers, artist thumbnails)
# from last.fm database, owe lots of credit to their API for this project!

class LastFMUser(object):
    url = 'http://ws.audioscrobbler.com/2.0'
    api_key = api_key
    def __init__(self,username):
        self.username = username
        self.headers = {
            'user-agent': self.username
        }

    def setUsername(self,username):
        self.username = username
    
    def lastFMGet(self,payload):
        payload['api_key'] = LastFMUser.api_key
        payload['format'] = 'xml'
        response = requests.get(LastFMUser.url,headers=self.headers,params=payload)
        return response.text

    def getAlbumInfo(self,album,artist):
        return self.lastFMGet({'method':'album.getInfo','artist':artist,'album':album})
    
    def getAlbumCoverURL(self,album,artist):
        albumInfo = str(self.getAlbumInfo(album,artist))
        tree = ET.fromstring(albumInfo)
        if tree.find('./album/image[@size="large"]') != None:
            if tree.find('./album/image[@size="large"]').text != None:
                return tree.find('./album/image[@size="large"]').text
            else:
                print('album cover not found for '+album)
                return 'default.png'
        else:
            print('album cover not found for '+album)
            return 'default.png'

    def getArtistInfo(self,artist):
        return self.lastFMGet({'method':'artist.getInfo','artist':artist})
    
    def getArtistImgURL(self,artist):
        artistInfo = str(self.getArtistInfo(artist))
        tree = ET.fromstring(albumInfo)
        if tree.find('./artist/image[@size="large"]') != None:
            if tree.find('./artist/image[@size="large"]').text != None:
                return tree.find('./album/image[@size="large"]').text
            else:
                print('artist img not found for '+artist)
                return 'default.png'
        else:
            print('artist img not found for '+artist)
            return 'default.png'

    def getArtistTopAlbums(self,artist):
        return self.lastFMGet({'method':'artist.getTopAlbums','artist':artist})

    def getArtistTrackCount(self,artist):
        numTracks = 0
        data = self.lastFMGet({'method':'artist.getToptracks','artist':artist})
        tree = ET.fromstring(data)
        tracks = tree.getchildren()[0].getchildren()
        for track in tracks:
            numTracks += 1
        return numTracks

    def getUserInfo(self):
        return self.lastFMGet({'method':'user.getInfo','user':self.username})
    
    def getUserLovedTracks(self):
        return self.lastFMGet({'method':'user.getLovedTracks','user':self.username})

    def getRecentTracks(self,lastSync):
        result = []
        data = self.lastFMGet({'method':'user.getRecentTracks','user':self.username,'from':lastSync})
        tree = ET.fromstring(data)
        recenttracks = tree.getchildren()[0].getchildren()
        for track in recenttracks:
            print(track.find('name').text)
            if track.attrib == {}:
                result.append({
                    'title':track.find('name').text,
                    'artist':track.find('artist').text,
                    'album':track.find('album').text,
                    'timestamp':track.find('date').attrib['uts']
                })
        return result
    
    def getTrackDurationSeconds(self,songDict):
        data = self.lastFMGet({'method':'track.getInfo','track':songDict['title'],'artist':songDict['artist'],'user':self.username})
        tree = ET.fromstring(data)
        if tree.getchildren()[0].find('./duration') != None and tree.getchildren()[0].find('./duration').text != None:
            duration = tree.getchildren()[0].find('./duration').text
            return int(duration)/1000
        else:
            return 0

