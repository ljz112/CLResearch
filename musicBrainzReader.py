import musicbrainzngs as mbz
import config

# it works fine, I'm j a little dissapointed that they're not saying the origin of the people either
mbz.set_useragent(config.EMAIL, '0.1')

artist_list = mbz.search_artists(query='Central Cee')['artist-list'] 
red_sovine = artist_list[0] 
print(red_sovine)