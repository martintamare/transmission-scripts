#! /usr/bin/env python2.6

import re,os,stat,shutil,string,sys
from tvnamer.utils import (FileParser,EpisodeInfo)
from tvdb_api import (tvdb_error, tvdb_shownotfound, tvdb_seasonnotfound,
tvdb_episodenotfound, tvdb_attributenotfound, tvdb_userabort,Tvdb)
from my_password import p_tvdb
import syslog

# instance
tvdb_instance = Tvdb(apikey=p_tvdb.key)

# specify our log file, here local0 !
syslog.openlog('torrent_seeded.py', 0, syslog.LOG_LOCAL0)

#variables
tv_dest="/home/torrent/public/tv/"
file_source="/home/torrent/downloads/completed/"
script_path="/home/torrent/transmission-scripts/"


# Format filename : lowercase and remove spaces " " with dots "."
def format(filename):
	temp =''
	for i in filename.split(' '):
		temp = temp + i.lower() +"."
	temp = temp.rstrip(".")
	
	name=""
	for i in temp.split('_'):
		name = name + i.lower() +"."
	name = name.rstrip(".")
	return name
	

# Parse a string to find a tvshow using tvnamer
# Return a couple (boolean,episode)
def tvnamer(filename):
	try:
		episode = FileParser(filename).parse()
	except Exception, e:
		return(False,null)
	else:
		if episode.seriesname is None:
			return(False,episode)
		else:
			return(True,episode)

# Return true if tv show, else false
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
	

# Function that creates a symlink in the right folder for tv show or move directly the file if not
# Return a couple (boolean,status,http_dir)
# Status represents the name of the tv shows + episode number + episode name
# Ex : House - [06x15] - I Love Pills			
# Http_dir contains the right url for tinyurl
def sort(filename):
	is_tv = tvnamer(filename)
	formatted_filename = format(filename)
		
	if checkifTV(is_tv[1]):
		episode = is_tv[1]
		
		# Format show name and filename
		dest_folder = format(episode.seriesname)
		season = episode.seasonnumber
		
		# Store
		base_home_dir = tv_dest + dest_folder
		home_dir = base_home_dir +"/s" + str(season)
		
		# Remove symlink
		try:
			os.unlink(home_dir+"/"+formatted_filename)
		except Exception, e:
			syslog.syslog(syslog.LOG_ERR,"removing symlink" , "os.unlink failed on " + home_dir + "/" + formatted_filename + ". Error: " + e.strerror)
		#else:
			#printOk("removing symlink")
		
		# Move file
		try:
			os.rename(filename,home_dir+"/"+formatted_filename)
		except Exception, e:
			syslog.syslog(syslog.LOG_ERR,"removing file" , "os.rename failed on " + filename + " to " + home_dir + "/" + formatted_filename + ". Error: " + e.strerror)
		#else:
			#printOk("removing file")

		return True
	
	else:
		return False

#printInfo("script torrent_seeded.py started")		
os.chdir(file_source)
sort(sys.argv[1])