import json
from requests.models import Response
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint
from objdict import ObjDict
from collections import Counter
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="7c5e565854fe420ba58b7ec434a105e1",
                                                           client_secret="52364c23fd6c4c8788c48313c576895a"))

# id of the playlist 
# maybe use params to get the playlist (userfriendly)
pl_id = 'spotify:playlist:1JRDlOReeuUM28zjNTfq6f'

#night
# https://open.spotify.com/playlist/3STQdPYGFTroG0wZrlnzry?si=697a0fe164784c18
#best from the past
# https://open.spotify.com/playlist/1JRDlOReeuUM28zjNTfq6f?si=1eb20e1d905846c0

def getResponse(pl_id):

    """
   getResponse(pl_id) information about the playlist
    
   :param: pl_id: the playlist id 
   
   :returns: all information about the playlist as json object  
    
   """

    offset = 0
    jsonObj = {}

    while True:

        response = sp.playlist_items(pl_id,
                                    offset=offset,
                                limit=100,
                                    fields='items.track')
        jsonObj.update(response)
        # beaks if reaches end
        if len(response['items']) == 0:
            break

        offset += len(response['items'])
    
        # pprint(jsonObj)
        return jsonObj

        
def getArtistURL(res):
    """
    getArtistNames(res): names of artists
        
    :param: res: all information about the playlist  -> getResponse(pl_id)
    
    :returns: all names of artists in a list 
        
    """
    urlList = []
    # goes through all 100 songs (or less)
    for items in res['items']: 

        # iterates through all artists 
        for artist in items['track']['artists']:

            #prints the artist name
            # pprint(artist['name'])''
            urlList.append(artist['external_urls']['spotify'])

    pprint(urlList)       
    return urlList


response = getResponse(pl_id)
getArtistURL(response)
