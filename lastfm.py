import requests
from apikey import *

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

    def getAlbumInfo(self,artist,album):
        return self.lastFMGet({'method':'album.getInfo','artist':artist,'album':album})

    def getArtistTopAlbums(self,artist):
        return self.lastFMGet({'method':'artist.getTopAlbums','artist':artist})

    def getUserInfo(self):
        return self.lastFMGet({'method':'user.getInfo','user':self.username})
    
    def getUserLovedTracks(self):
        return self.lastFMGet({'method':'user.getLovedTracks','user':self.username})

    def getRecentTracks(self):
        return self.lastFMGet({'method':'user.getRecentTracks','user':self.username})

user = LastFMUser('')