######### IN USE FOR PROJECT: not used after data collection, but gets birth place and date of artists


import musicbrainzngs as mbz
import config

# it works fine, I'm j a little dissapointed that they're not saying the origin of the people either
mbz.set_useragent(config.EMAIL, '0.1')

# get the birth date and where they grew up
def getOriginDetails(artist):
    artist_list = mbz.search_artists(query=artist)['artist-list'] 
    details = artist_list[0]
    return [getBirthDate(details), getHometown(details)]

# get the birth date of set of details
def getBirthDate(details):
    try: 
        return details['life-span']['begin']
    except Exception as e:
        return ''

# returns hometown of artist
def getHometown(details):
    try: 
        return details['begin-area']['name']
    except Exception as e:
        return ''