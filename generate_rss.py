#! /usr/bin/env python2.6

import os,stat,time
import PyRSS2Gen
import datetime
import re
from stat import *
from tvnamer.utils import (FileParser,EpisodeInfo)
from tvdb_api import (tvdb_error, tvdb_shownotfound, tvdb_seasonnotfound,
tvdb_episodenotfound, tvdb_attributenotfound, tvdb_userabort,Tvdb)
from my_password import (p_tvdb,p_mysql)
import sys
import getopt
import sqlite3
import syslog

# specify our log file, here local0 !
syslog.openlog('rss', 0, syslog.LOG_LOCAL0)

# Setup basic directory
http_dir = 'https://fi08.us.to/'
xml_dir = "/home/fi08/"
watch_dir = "/home/torrent/public/"

# Setup tvdb using our apikey
tvdb_instance = Tvdb(apikey=p_tvdb.key)
	
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
	# todo, remove double dots...

def generateRSS(debug):
	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"starting Zik RSS generation")
	generateLevel1("zik","zik",debug)

	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"starting App RSS generation")
	generateLevel1("applications","app",debug)

	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"starting Anime RSS generation")
	generateLevel1("anime","anime",debug)

	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"starting Movies RSS generation")
	generateLevel1("movies","movies",debug)

	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"starting Temp RSS generation")
	generateLevel1("temp","temp",debug)

	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"starting TV RSS generation")
	generateLevel2("tv","tvshows",debug)

	syslog.syslog(syslog.LOG_INFO, "generation ok")

# Will genarate an rss file in xml, watching files/folder present watch_folder, printing debug info if necessary
def generateLevel1(watch_folder,xml,debug):
	#final directory to watch
	dir = watch_dir+watch_folder
	
	#struct that will handle, filename and filedate
	date_file_list = []
	
	#for every file/folder, build a tuple and add it to the list
	for filename in os.listdir ( dir ):
		fileStats = os.stat ( dir+"/"+filename )
		date = time.localtime ( fileStats [ stat.ST_MTIME ])
		date_file_tuple = date, filename
		date_file_list.append(date_file_tuple)
	
	#sort to have new files first	
	date_file_list.sort()
	date_file_list.reverse()
	
	if(debug):
		for item in date_file_list:
			folder, file_name = os.path.split(item[1])
			# convert date tuple to MM/DD/YYYY HH:MM:SS format
			file_date = time.strftime("%m/%d/%y %H:%M:%S", item[0])
			syslog.syslog(syslog.LOG_DEBUG, file_date + " " + file_name)
	else:
		buildRssLevel1(watch_folder,xml,date_file_list)

def generateLevel2(watch_folder,xml,debug):

	episode_list = []
	dir = watch_dir+watch_folder

	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"Raw data")
	# First part, parse folder list, to obtain shows information (foldername = showname)
	for show in os.listdir(dir):
		showpath = os.path.join(dir, show)
		mode = os.stat(showpath)[ST_MODE]
		if S_ISDIR(mode):
			if(debug):
				syslog.syslog(syslog.LOG_DEBUG,"Found show " + show)
			
			# Second part, part sub folder, have season information (subfolder = s+seasonnumber)
			for season in os.listdir(showpath):
				seasonpath = os.path.join(showpath, season)
				mode = os.stat(showpath)[ST_MODE]
				if S_ISDIR(mode):
					if(debug):
						syslog.syslog(syslog.LOG_DEBUG,"Found season " + season)
						
					# Last, build a list with filename , show and filedate
					for episode in os.listdir(seasonpath):
						fileStats = os.stat ( seasonpath+"/"+episode )
						filemode = fileStats[ST_MODE]
						if S_ISREG(filemode):
							date = time.localtime ( fileStats [ stat.ST_MTIME ])
							info = episode, show, date, seasonpath
							if(debug):
								syslog.syslog(syslog.LOG_DEBUG,"date : " + time.strftime("%m/%d/%y %H:%M:%S", date) + " " + episode)
							episode_list.append(info)
	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"Raw data")	
	
	
					
	# check episode_list with the database
	# database connection
	conn = sqlite3.connect('/home/torrent/transmission-scripts/rss.db')
	cursor = conn.cursor()
	# will hold final info
	final_list = []
	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"Unsorted Data")
		
	for episode in episode_list:
		filename = episode[0]
		if(InDatabase(filename,cursor)):
			# If present to extract data
			(date,info,path) = FetchInfo(filename,cursor)
			if(debug):
				syslog.syslog(syslog.LOG_DEBUG,"database: " + date + " " + info)
		else:

			# Add the row with the good information
			title = tvnamer(episode[0],episode[1]).generateFilename()
			correct_date = datetime.date(episode[2].tm_year,episode[2].tm_mon,episode[2].tm_mday)
			(date,info,path) = (correct_date,title,episode[3].replace("/home/torrent/public/tv/","",1)+"/")
			date = correct_date.__str__()
			
			if(debug):
				syslog.syslog(syslog.LOG_DEBUG,"tvdb: "+ date + " " + title)
			else:
				query = "INSERT into rss_info (filename, date, info, path) values (\"%s\", \"%s\", \"%s\", \"%s\") " %(episode[0],date,title,episode[3])
				cursor.execute(query)	
		final_list.append((date,filename,info,path,True))		
		
	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"Unsorted data")
		
	#sort to have new files first	
	final_list.sort()
	final_list.reverse()
	
	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"Sorted data")
		for item in final_list:
			filedate = item[0]
			filename = item[1]
			info = item[2]
			path = item[3]
			# convert date tuple to MM/DD/YYYY HH:MM:SS format
			# print(filedate + " " + filename + " " + info + " " + path)
			syslog.syslog(syslog.LOG_DEBUG,filedate + " " + info)
	else:
		# build rss !
		buildRssLevel2(watch_folder,xml,final_list)
	
	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"Sorted data")	
		syslog.syslog(syslog.LOG_DEBUG,"Remove old data")
	
	# use the list to remove old data
	RemoveOldData(final_list,cursor,debug)
	
	if(debug):
		syslog.syslog(syslog.LOG_DEBUG,"Remove old data")	
	
	#close connection
	conn.commit()
	conn.close()
	
# Return tuple (date,info,path) from database using filename	
def FetchInfo(filename,cursor):
	query = "SELECT date, info, path FROM rss_info WHERE filename =\'" + filename + "\'"
	cursor.execute(query)
	row = cursor.fetchone()
	# remove unecessary path from full path
	return row[0],row[1],row[2].replace("/home/torrent/public/tv/","",1)+"/"

# Check in a filename is already in database and return boolean
def InDatabase(filename,cursor):
	query = "SELECT COUNT(*) FROM rss_info WHERE filename =\'" + filename + "\'"
	cursor.execute(query)
	(numrows,)=cursor.fetchone()
	if(numrows == 0):
		return False
	else:
		return True

# Remove old entries from the tv database
def RemoveOldData(list,cursor,debug):
	# Will contain the list to be remove
	remove_list = []
	# Will contain all data from database
	data_list = []
	query = "SELECT filename FROM rss_info"
	cursor.execute(query)
	for row in cursor:
		data_list.append(row[0])
		
	# Will contain ok data from list
	ok_list = []
	for item in list:
		ok_list.append(item[1])
	
	# Now loop data_list
	for item in data_list:
		# if cannot be find in ok_list
		try:
			ok_list.index(item)
		except Exception, e:
			# add to remove list
			remove_list.append(item)
	
	# loop remove list and perform queries
	for item in remove_list:
		if(debug):
			syslog.syslog(syslog.LOG_DEBUG,"Removing " + item)
		else:
			# notice the trick, to convert item as a tuple
			cursor.execute("delete from rss_info where filename=?",(item,))
	
# Parse a string to find a tvshow using tvnamer
# Return an episode
def tvnamer(filename,show):
	try:
		episode = FileParser(filename).parse()
	except Exception, e:
		syslog.syslog(syslog.LOG_ERR,"tvnamer sur " + filename)
		exit(0)
	else:
		if episode.seriesname is None:
			episode.seriesname = show
			
		return get_episode_description(episode)

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
	
# Ask tvdb the name of the episode
def populateFromTvdb(episode):
	try:
		show = tvdb_instance[episode.seriesname]
	except Exception, e:
		syslog.syslog(syslog.LOG_ERR,"tvdb_instance",str(e) + " " + episode.filename)
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


def buildRssLevel1(folder,xml,list):
	#Creation of the rss
	rss = PyRSS2Gen.RSS2(
	    title = "TV Show Paradize RSS Feed : "+folder.capitalize(),
	    link = "https://fi08.us.to/"+folder,
	    description = "The latest "+xml.capitalize()+" of the server",
	    lastBuildDate = datetime.datetime.now(),
	)
	
	#Construction de la liste avec les items
	for item in list:
		
		# extract just the filename
		folder, file_name = os.path.split(item[1])
		# convert date tuple to MM/DD/YYYY HH:MM:SS format
		file_date = time.strftime("%m/%d/%y %H:%M:%S", item[0])
		
		rss.items.append(
			PyRSS2Gen.RSSItem(
				title = file_name.capitalize(),
				link = http_dir + folder + "/" + file_name,
				description = "",
				guid = PyRSS2Gen.Guid(http_dir + folder + "/" + file_name),
				pubDate = file_date
			)
		)
	
	rss.write_xml(open(xml_dir+xml+".xml", "w"))

def buildRssLevel2(folder,xml,list):
	#Creation of the rss
	rss = PyRSS2Gen.RSS2(
	    title = "TV Show Paradize RSS Feed : "+folder.capitalize(),
	    link = "https://fi08.us.to/"+folder,
	    description = "The latest "+xml.capitalize()+" of the server",
	    lastBuildDate = datetime.datetime.now(),
	)
	
	#Creating item
	for item in list:
		filedate = item[0]
		filename = item[1]
		info = item[2]
		path = item[3]
		
		rss.items.append(
			PyRSS2Gen.RSSItem(
				title = info,
				link = http_dir + folder + "/" + path + filename,
				description = info,
				guid = PyRSS2Gen.Guid(http_dir + folder + "/" + path + filename),
				pubDate = filedate
			)
		)
	# Write !
	rss.write_xml(open(xml_dir+xml+".xml", "w"))
	
def usage():											
	print "Only the option -d or --debug is available to print debug info"

# Test to do thing the right way using getpot !
# So far, only one parameter, debug
def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "d", ["debug"])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	debug = False
	for o, a in opts:
		if o in ("-d", "--debug"):
			debug = True
	generateRSS(debug)
	
if __name__ == "__main__":
	main()