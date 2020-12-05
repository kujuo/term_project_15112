import requests
from apikey import *
from xml_io import *
from playlist import *
import xml.etree.ElementTree as ET

# referenced these websites for help on syntax/methods
# https://www.dataquest.io/blog/last-fm-api-python/
# https://www.last.fm/api/

# all nusic-related images (album covers, artist thumbnails)
# from last.fm database

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

    # def getAlbumSearchInfo(self,album,artist)
    
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

    def getArtistTopAlbums(self,artist):
        return self.lastFMGet({'method':'artist.getTopAlbums','artist':artist})

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

username = settingsXML.getLastFM()
user = LastFMUser(username)