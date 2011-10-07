#!/usr/bin/python
import sys
import os
import syslog
import twitter,tinyurl
from my_password import (p_tvdb, p_twitter)
from tvnamer.utils import (FileParser,EpisodeInfo)
from tvdb_api import (tvdb_error, tvdb_shownotfound, tvdb_seasonnotfound, tvdb_episodenotfound, tvdb_attributenotfound, tvdb_userabort,Tvdb)

# tvdb instance
tvdb_instance = Tvdb(apikey=p_tvdb.key)

# specify our log file, here local0 !
syslog.openlog('torrent_ended.py', 0, syslog.LOG_LOCAL0)

api = twitter.Api(consumer_key=p_twitter.consumer_key,consumer_secret=p_twitter.consumer_secret, access_token_key=p_twitter.access_token_key, access_token_secret=p_twitter.access_token_secret)

# Parse a string to find a tvshow using tvnamer
# Return a couple (boolean,episode)
def tvnamer(filename):
	try:
		episode = FileParser(filename).parse()
	except Exception, e:
		return(False,"")
	else:
		if episode.seriesname is None:
			return(False,episode)
		else:
			return(True,episode)
			
def checkifTV(episode):
	try:
		tvdb_instance[episode.seriesname]
	
	except Exception, e:
		return False
	else:
		return True

# Ask tvdb the name of the episode
def populateFromTvdb(episode):
	show = tvdb_instance[episode.seriesname]
	episode.seriesname = show['seriesname']
	
	epnames = []
	for cepno in episode.episodenumbers:
		try:
			episodeinfo = show[episode.seasonnumber][cepno]

		except tvdb_attributenotfound:
			raise EpisodeNameNotFound(
                "Could not find episode name for %s" % cepno)
		else:
			epnames.append(episodeinfo['episodename'])
	episode.episodename = epnames
	return

# Return a string containing episode information
# Format : ShowName - [01x02] - EpisodeName
def get_episode_description(episode):
	populateFromTvdb(episode)
	ep = EpisodeInfo(
		seriesname = episode.seriesname,
        seasonnumber = episode.seasonnumber,
        episodenumbers = episode.episodenumbers,
		episodename = episode.episodename,
        filename = None)
	return ep.generateFilename()

# Get the name
torrent_name = sys.argv[1]
save_path = sys.argv[2]
http_base="https://fi08.us.to/"

# Parse it to see if it's tv
is_tv = tvnamer(torrent_name)
if checkifTV(is_tv[1]):
	episode = is_tv[1]
	# Format show name and filename /home/torrent/public/tv/
	sub_path = save_path.replace("/home/torrent/public/","")
	sub_path = sub_path + "/"
	url = http_base + sub_path + torrent_name
	status = get_episode_description(episode)
	url = tinyurl.create_one(url)
	twitter_status = status + " " + url
	try:
		api.PostUpdate(twitter_status)
	except Exception, e:
		syslog.syslog(syslog.LOG_ERR,"posting to twitter: " + e.__str__())