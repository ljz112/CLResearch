import musicbrainzngs as mbz
import config

# it works fine, I'm j a little dissapointed that they're not saying the origin of the people either
mbz.set_useragent(config.EMAIL, '0.1')

# get the birth date and where they grew up
def getOriginDetails(artist):
    artist_list = mbz.search_artists(query=artist)['artist-list'] 
    details = artist_list[0]
    return [details['life-span']['begin'], details['begin-area']['name']]