#! /usr/bin/env python2.6

import os,stat,time
import PyRSS2Gen
import datetime
import re
from stat import *
from tvnamer.utils import (FileParser,EpisodeInfo)
from tvdb_api import (tvdb_error, tvdb_shownotfound, tvdb_seasonnotfound,
tvdb_episodenotfound, tvdb_attributenotfound, tvdb_userabort,Tvdb)
from my_password import p_tvdb

http_dir = 'https://fi08.us.to/'
dest = "/home/fi08/"

tvdb_instance = Tvdb(apikey=p_tvdb.key)

# useless but i dont know anything equivalent in python ;)
beauty_path = "/home/torrent/transmission-scripts/bash-beauty.sh"
def printOk(text):
	os.system(". "+beauty_path+"; printTask -t -w 50 \""+text+"\";printOk")

def printFail(text,error):
	os.system(". "+beauty_path+"; printTask -t -w 50 \""+text+"\";printFail \"" + error + "\"" )

def printWarn(text):
	os.system(". "+beauty_path+"; printTask -t -w 50 \""+text+"\";printWarn")
	
def printInfo(text):
	os.system(". "+beauty_path+"; printTask -t -w 50 \""+text+"\";printInfo")
	
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
			ep_ok = get_episode_description(episode)
			return(True,ep_ok)

# Ask tvdb the name of the episode
def populateFromTvdb(episode):
	try:
		show = tvdb_instance[episode.seriesname]
	except Exception, e:
		printFail("tvdb_instance",str(e) + " " + episode.filename)
		return
	else:	
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
	return ep
	
def build_rss(liste_item,dir,name):
	# Va contenir la liste des items
	liste = []
	
	#Creation du flux
	rss = PyRSS2Gen.RSS2(
	    title = "TV Show Paradize RSS Feed : "+name.capitalize(),
	    link = "https://fi08.us.to/",
	    description = "The latest "+name.capitalize()+" of the server",
	    lastBuildDate = datetime.datetime.now(),

	)
	
	#Construction de la liste avec les items
	for file in liste_item:
                test = []
                # extract just the filename
                folder, file_name = os.path.split(file[1])
                # convert date tuple to MM/DD/YYYY HH:MM:SS format
                file_date = time.strftime("%m/%d/%y %H:%M:%S", file[0])
                #print "%-40s %s" % (file_name, file_date)

                rss.items.append(
                PyRSS2Gen.RSSItem(
                        title = file_name.capitalize(),
                        link = http_dir + dir + "/" + file_name,
                        description = "",
                        guid = PyRSS2Gen.Guid(http_dir + dir + "/" + file_name),
                        pubDate = file_date
                )
                )
	
	rss.write_xml(open(dest+name+".xml", "w"))

# RSS de profondeur 1
def generate_rss_l1(ext,name):
	#repertoire qui va bien
	dir = "/home/torrent/public/"+ext
	
	#structure qui va contenir date et nom de fichier
	date_file_list = []
	
	#pour chaque fichier on regarde la date cree un tuple et on lajoute
	for filename in os.listdir ( dir ):
		fileStats = os.stat ( dir+"/"+filename )
		date = time.localtime ( fileStats [ stat.ST_MTIME ])
		date_file_tuple = date, filename
		date_file_list.append(date_file_tuple)
		
	#on trie par date pour avoir les nouveau en 1er
	date_file_list.sort()
	date_file_list.reverse()
	
	build_rss(date_file_list,ext,name)
	

	
#RSS de profondeur deux !	
def generate_rss(dir,name):
	
	#Creation du flux
	rss = PyRSS2Gen.RSS2(
	    title = "TV Show Paradize RSS Feed : "+name.capitalize(),
	    link = "https://fi08.us.to/",
	    description = "The latest "+name.capitalize()+" of the server",
	    lastBuildDate = datetime.datetime.now(),

	)
	
	#structure qui va contenir date et nom de fichier et rep
	date_file_list = []
	
	for f in os.listdir(dir):
		pathname = os.path.join(dir, f)
		mode = os.stat(pathname)[ST_MODE]
		fileStats = os.stat ( pathname )
		if S_ISDIR(mode):
			# It's a directory, build rss from the file
			
			for h in os.listdir(pathname):
				subpathname = os.path.join(pathname, h)
				fileStats = os.stat ( subpathname)
				submode = fileStats[ST_MODE]
				if S_ISDIR(submode):
					for files in os.listdir(subpathname):
						fileStats = os.stat ( subpathname+"/"+files )
						filemode = fileStats[ST_MODE]
						if S_ISREG(filemode):
							# On ajoute le tuple, date nom du chier
							# print "on ajoute fichier " + files
							date = time.localtime ( fileStats [ stat.ST_MTIME ])
							date_file_tuple = date, f + "/" + h + "/" + files, ""
							date_file_list.append(date_file_tuple)
					
		elif S_ISREG(mode):
			# On ajoute le tuple, date nom du chier
			#print "on ajoute fichier "
			date = time.localtime ( fileStats [ stat.ST_MTIME ])
			date_file_tuple = date, f, ""
			date_file_list.append(date_file_tuple)
			
	#on trie par date pour avoir les nouveau en 1er
	date_file_list.sort()
	date_file_list.reverse()

	#Construction de la liste avec les items
	for g in date_file_list:
		# extract just the filename
		folder, file_name = os.path.split(g[1])
		
		# print "folder:"+folder+" file:"+file_name
		# convert date tuple to MM/DD/YYYY HH:MM:SS format
		file_date = time.strftime("%m/%d/%y %H:%M:%S", g[0])
		#print "%-40s %s" % (file_name, file_date)
		
		# Get right info
		# print "On traite %s" % (file_name)
		is_tv = tvnamer(file_name)
		title = ""
		# If only one file
		if is_tv[0]:
			episode = is_tv[1]
			title = episode.generateFilename()
			# print ": %s" % (title)
		
		# print(file_date)
		rss.items.append(
                PyRSS2Gen.RSSItem(
                        title = title,
                        link = http_dir + "tv/" + folder + "/"+file_name,
                        guid = PyRSS2Gen.Guid(http_dir + "tv/" + folder + "/"+file_name),
                        pubDate = file_date)
						)
	
	rss.write_xml(open(dest+name.lower()+".xml", "w"))	
		
		
		
printInfo("starting RSS generation")

#print('--------------ZIK-------------')
generate_rss_l1("zik","zik")

#print('--------------ZIK-------------')
generate_rss_l1("applications","app")

#print('--------------ANIME-------------')
generate_rss_l1("anime","anime")

#print('--------------MOVIE-------------')
generate_rss_l1("movies","movies")

#print('--------------TEMP-------------')
generate_rss_l1("temp","temp")

#print('--------------TV-------------')
generate_rss("/home/torrent/public/tv","Tvshows")
#generate_rss_l2("/home/torrent/public/tv","tv")

printOk("RSS generated")
