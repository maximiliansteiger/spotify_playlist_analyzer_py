from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint
from collections import Counter
import re

from werkzeug.wrappers import response

#implement id and secret from spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="---",
                                                           client_secret="---"))


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


def getGenreOfPlaylist(artistUrlList):
    """
    getGenreOfPlaylist(urlList): genres of playlist

    :param: artistUrlList: list of URLs to the artists

    :returns: list of genres from the artists in the playlist 

    """
    genres = []

    for url in artistUrlList:
        for genre in sp.artist(url)['genres']:
            genres.append(genre)

    # pprint(genres)
    return genres


def getArtistNames(res):
    """
    getArtistNames(res): names of artists

    :param: res: all information about the playlist  -> getResponse(pl_id)

    :returns: all names of artists in a list 

    """
    nameList = []
    # goes through all 100 songs (or less)
    for items in res['items']:

        # iterates through all artists
        for artist in items['track']['artists']:

            # prints the artist name
            # pprint(artist['name'])''
            nameList.append(artist['name'])

    # pprint(nameList)
    return nameList


def getSongImage(res):
    """
    getSongImage(res): Image of songs

    :param: res: all information about the playlist  -> getResponse(pl_id)

    :returns: list of all images to each song

    """
    imagesList = []
    # goes through all 100 songs (or less)
    for track in res['items']:

        imagesList.append(track['track']['album']['images'][1]['url'])

    return imagesList

def getTopThreeSongImages(res):
    """
    getSongImage(res): Image of songs

    :param: res: all information about the playlist  -> getResponse(pl_id)

    :returns: list of all images to each song

    """
    imagesList = []
    # goes through all 100 songs (or less)
    
    imagesList.append(res['items'][0]['track']['album']['images'][1]['url'])
    imagesList.append(res['items'][1]['track']['album']['images'][1]['url'])
    imagesList.append(res['items'][2]['track']['album']['images'][1]['url'])

    return imagesList 


def getArtistURL(res):
    """
    getArtistNames(res): names of artists

    :param: res: information about the playlist  -> getResponse(pl_id)

    :returns: all names of artists in a list 

    """
    urlList = []
    # goes through all 100 songs (or less)

    #TODO: fix this (more than 100 songs should be possible) it only takes the first 100 songs because of a Spotify limit
    for items in res['items']:

        # iterates through all artists
        for artist in items['track']['artists']:

            # prints the artist name
            # pprint(artist['name'])''
            urlList.append(artist['external_urls']['spotify'])

    return urlList


def getNameOfPlaylist(res):
    # TODO
    res


def getDurationOfPlaylist(res):
    # TODO
    res


def getLinkToSong(res):
    """
    getLinkToSong(res): link to all songs 

    :param: res: information about the playlist  -> getResponse(pl_id)

    :returns: list of links to each song

    """
    return res['items'][0]['track']['external_urls']['spotify']


def calcTopOfList(inputlist):
    """
    calcTopOfList(inputlist): most common elements of list

    :param: inputlist: list of numbers / strings

    :returns: the 10 most common elements in a list

    """
    return Counter(inputlist).most_common(10)


def calcPopularity(res):
    """
    calcPopularity(res): the popularity of the playlist's songs

    :param: res: all information about the playlist  -> getResponse(pl_id)

    :returns: list of all images to each song

    """
    popularityList = []
    # goes through all 100 songs (or less)
    for track in res['items']:
        popularityList.append(track['track']['popularity'])

    total = sum(popularityList)
    length = len(popularityList)
    return total/length  # use // for round number

    # most seen album??? 



def getPlaylistInformation(playlistURL):

    playlistURL = playlistURL.replace('?', '/')
    playlistURL = re.split("/", playlistURL)
    playlistURL = "spotify:playlist:"+ playlistURL[4]

    # this in one line 
    # playlistURL = "spotify:playlist:"+ re.split("/", playlistURL.replace('?', '/'))


    # get response / object
    response = getResponse(playlistURL)

    # all artists names /list
    artistNames = getArtistNames(response)

    # top artists names and numbers /object
    topArtist = calcTopOfList(artistNames)

    # all artists URL
    urlList = getArtistURL(response)

    # all genres of atists in the playlist
    genres = getGenreOfPlaylist(urlList)

    # top genres of artists in the playlist
    topGenres = calcTopOfList(genres)

    # gets image for song
    images = getSongImage(response)

    # popularity of playlist songs
    popularity = calcPopularity(response)

    # topThreeSongImages = getTopThreeSongImages(response)

    # test output
    # pprint(response)
    # pprint(artistNames)
    # pprint(topArtist) 
    # pprint(playlistURL)
    # pprint(urlList)
    # pprint(genres)
    # pprint(topGenres)
    # pprint(images)
    # pprint(popularity)
    # pprint(topThreeSongImages)

    strArtists = """
    <table>
    <thead>
        <tr>
        <th>Artist</th>
        <th>Nummer</th>
        </tr>
    </thead>
    <tbody>
       
     """

    for artist in topArtist:
        strArtists += '<tr><td>' + \
            str(artist[0])+'</td><td>'+str(artist[1])+'</td><tr>'

    strArtists += """
  
    </tbody>
    </table>
    """

    strGenres = """
    <table>
    <thead>
    <tr>
    <th>Genre</th>
    <th>Nummer</th>
    </tr>
    </thead>
    <tbody>
    """

    for genre in topGenres:
        strGenres += '<tr><td>' + \
            str(genre[0])+'</td><td>'+str(genre[1])+'</td></tr>'

    strGenres += """
    </tbody>
    </table>
    """


    strImages = """
    <div class="images">
    """
    for image in images:
        strImages += '<img src="'+image+'">'


    strImages += """ </div> """


    # maybe html
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>analizer</title>
        <link rel="stylesheet" href="stylesheet.css">

    <style>
 * {
    font-family: Helvetica;
    cursor: pointer;

}


body {
    background-color: #2C2C2C;
    text-align: center;

}

table,
td,
th {
    background-color: #121212;
    text-align: left;
    color: #FFFFFF;
    border-radius: 15px;
    padding: 2vh;
    margin: 5vh;
}

table:hover,
td:hover,
th:hover {

    color: #1DB954;

}

table {
    display: inline-block;
    left: auto;
    right: auto;
    border-collapse: collapse;
  
    background-color: #121212;
    margin: 0vh 5vh 0vh vh;
}

.centerDiv {
    display: block;
    justify-content: center;
    align-items: center;
    text-align: center;
    margin-top: 5vh;
}


th,
td {
    padding: 15px;
}

#popularity {
    color: #1DB954;
    margin-bottom: 10vh;
    font-size: 6vh;
}

#popularity.h1 {

    border-radius: 25px;
    border: 1px solid #1DB954;

}

#topThreeSongs{
    margin-top: 5vh;
    color: #1DB954;
}

#topThreeSongs.h1 {

    margin-bottom: 25vh;

    }

    .images{
        overflow-y = scroll;
        display: inline;
    }


    h2{
        font-size: 3vh;
        color: #1DB954;
    }

    </style>



    </style>
    </head>
    <body>

    
    <div class="centerDiv">

        <div id="popularity" title="popularity score" >
            <h2> popularityscore <h2>
            <h1>"""+str(int(popularity)) +"""<h1>
        </div>

        <h2> artists genre artists</h2>
        <div>
        """ + strArtists + strGenres + strArtists + """
        </div>

        <h2> songs </h2>
        """+strImages+"""

    </div>


    </body>
    </html>
    """
