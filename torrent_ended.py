#! /usr/bin/env python2.6

import re,os,stat,shutil,string,sys,twitter,tinyurl
from tvnamer.utils import (FileParser,EpisodeInfo)
from tvdb_api import (tvdb_error, tvdb_shownotfound, tvdb_seasonnotfound,
tvdb_episodenotfound, tvdb_attributenotfound, tvdb_userabort,Tvdb)
from my_password import (p_tvdb, p_twitter)

tvdb_instance = Tvdb(apikey=p_tvdb.key)

file_source="/home/torrent/downloads/completed/"
torrent_source="/var/lib/transmission-daemon/info/torrents/"
tv_dest="/home/torrent/public/tv/"
other_dest="/home/torrent/private/"
http_base="https://fi08.us.to/"
script_path="/home/torrent/transmission-scripts/"

def printOk(text):
	os.system(". "+script_path+"bash-beauty.sh; printTask -t -w 50 \""+text+"\";printOk")

def printFail(text,error):
	os.system(". "+script_path+"bash-beauty.sh; printTask -t -w 50 \""+text+"\";printFail \"" + error + "\"" )

def printWarn(text):
	os.system(". "+script_path+"bash-beauty.sh; printTask -t -w 50 \""+text+"\";printWarn")
	
def printInfo(text):
	os.system(". "+script_path+"bash-beauty.sh; printTask -t -w 50 \""+text+"\";printInfo")

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
	

# Function that creates a symlink in the right folder for tv show or move directly the file if not
# Return a couple (boolean,status,http_dir)
# Status represents the name of the tv shows + episode number + episode name
# Ex : House - [06x15] - I Love Pills			
# Http_dir contains the right url for tinyurl
def sort(filename,id):
	is_tv = tvnamer(filename)
	formatted_filename = format(filename)
	
	# Return value
	status = ""
	http_dir = ""
	
	if checkifTV(is_tv[1]):
		episode = is_tv[1]
		
		# Format show name and filename
		dest_folder = format(episode.seriesname)
		season = episode.seasonnumber
		
		if(season!=0):
			# Store
			base_home_dir = tv_dest + dest_folder
			home_dir = base_home_dir +"/s" + str(season)
			
			#printOk("founded : \"" + episode.seriesname + "\"")
			# Test si le dossier existe
			if(not(os.path.isdir(base_home_dir))):
				try:
					os.mkdir(base_home_dir)
				except Exception, e:
					printFail("created subdirectory" , "os.mkdir failed on " + base_home_dir + ". Error: " + e.strerror)
				else:
					printWarn("created subdirectory " + dest_folder)
				
			if(not(os.path.isdir(home_dir))):
				try:
					os.mkdir(home_dir)
				except Exception, e:
					printFail("created subdirectory" , "os.mkdir failed on " + home_dir + ". Error: " + e.strerror)
				else:
					printWarn("created subdirectory s" + str(season))
					
			try:
				os.symlink(file_source+filename,home_dir+"/"+formatted_filename)
			except Exception, e:
				printFail("created symlink", "os.symlink failed on " + home_dir + "/"+formatted_filename + ". Error: " + e.strerror)
			#else:
				#printOk("created symlink")
				
			http_dir = "tv/" + dest_folder +"/s" + str(season) + "/" + formatted_filename
			
			# Create status
			status = get_episode_description(episode)
			return(True,status,http_dir)
		else:
			printFail("tv without season" , filename)
	# else: if we did not return yet
	# Rename file or folder and then remove associated torrent	
	#printInfo("not TV, moving to temp zone")
	try:
		os.rename(file_source+filename,other_dest+formatted_filename)
	except Exception, e:
		printFail("moving : " + formatted_filename, "os.rename error:" + e.strerror)
	#else:
		#printOk("moving : " + formatted_filename)
		
	#printInfo("deleting torrent")
	os.system(script_path+"rm_torrent.sh "+id);
	return(False,status,http_dir)

# printInfo("starting script torrent_ended.py")
retour = sort(sys.argv[1],sys.argv[2])
api = twitter.Api(consumer_key=p_twitter.consumer_key,consumer_secret=p_twitter.consumer_secret, access_token_key=p_twitter.access_token_key, access_token_secret=p_twitter.access_token_secret)

if retour[0]:
	url = http_base + retour[2]
	url = tinyurl.create_one(url)
	twitter_status = retour[1] + " " + url
	try:
		api.PostUpdate(twitter_status)
	except Exception, e:
		printFail("posting to twitter", "api.PostUpdate")
	#else:
		#printOk("posting to twitter")

