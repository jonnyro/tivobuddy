TIVO="TIVO_IP"
MAK="YOURMAKHERE"
import ConfigParser
import libxml2
import libxslt
import sys
import urllib2
import MySQLdb
import os
import findtivo

MAK=-1

def checkTablesExist():

	pass

def loadGlobalSettings():
	global MAK
	global DB_FILE

	if (os.path.exists("config.ini")):
		config = ConfigParser.ConfigParser()
		config.readfp(open('config.ini'))
	else:
		print "Configuration File Not Found"

	#Attempt to load media access key
	try:
		MAK=config.get("Account Settings","MediaAccessKey")

	except:
		print "Media Access Key not found in configuration file"
		print ""
		print "Format:"
		print ""
		print "[Account Settings]"
		print "MediaAccessKey=111111132433"
		print ""
		print "Quitting"
		sys.exit(-1)

	#Attempt to load database filename
	try:
		DB_FILE = config.get("Database Settings","DBFileName")
	except:
		print "Database filename notfound in configuration file"
		print ""
		print "Format:"
		print ""
		print "[Database Settings]"
		print "DBFileName=tivobuddy.sqlite"
		print ""
		print "Quitting"
		sys.exit(-1)
		
def updateTivoShowCache(TIVO_ID, TIVO_IP):
	conn = sqlite3.connect('tivo.db')
	c = conn.cursor()



	print "Attempting to open tivo at: " + str(TIVO_IP) + " with ID " + str(TIVO_ID)
	url = "https://" + TIVO_IP + "/TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse=Yes" 
	print "URL=" + url

	#TODO: Set up gettivo.sh to accept Media Access Key as argument.
	cmd = "./gettivo.sh " + TIVO_IP
	print "CMD is " + cmd
	os.system(cmd)

	styledoc = libxml2.parseFile("tivo.xsl")
	style = libxslt.parseStylesheetDoc(styledoc)
	doc = libxml2.parseFile("tivoroll.xml")
	result = style.applyStylesheet(doc, None)
	style.saveResultToFilename("tivoroll.html", result, 0)
	style.freeStylesheet()
	doc.freeDoc()
	result.freeDoc()

	f=open('./tivoroll.html')

	linecount=0
	for line in f:
		linecount = linecount+1

	f.close()

	import math

	f=open('./tivoroll.html')

	#Delete all shows for this tivo from the showbuffer
	query = "DELETE FROM showbuffer WHERE tivoID=\"%s\"" % str(TIVO_ID)			
	cursor.execute( query )
	
	   
	#Iterate line by line over tivoroll.html converting each line
	# into a format suitable for insertion into database
	item = 0
	curline = 0
	for line in f:
		linearr = line.split("|")

		if (linearr[0] == "Show"):
			show = linearr[1]
			episode_title = ""
			description = ""
			URL = ""
		if (linearr[0] == "EpisodeTitle"):
			episode_title = linearr[1]
		if (linearr[0] == "Description"):
			description = linearr[1]
		if (linearr[0] == "URL"):
			URL = linearr[1]
			#insert show entry into database
			query = "INSERT INTO showbuffer SET tivoID=\"%s\", showname=\"%s\",showtitle=\"%s\",showdescription=\"%s\",showurl=\"%s\"" % tuple(map(MySQLdb.escape_string,(str(TIVO_ID), show, episode_title, description, URL)))
			cursor.execute( query )
		curline = curline + 1



if __name__ == "__main__":
	#Confirm sqlite tables exist and match our specifications
	if not checkTablesExist():
		echo "Error initializing/connecting to sqlite database"
		sys.exit(-1)


	conn = sqlite3.connect(
	cursor.execute ("SELECT ID,ip,description FROM boxes")

	tivos= findtivo.run_scan()
	print tivos

	for tivo_name in tivos.keys():
		#List all of the tivos	
		cursor.execute ("SELECT ID,ip,name FROM boxes WHERE name=\"" + tivo_name + "\"" )
		data = cursor.fetchone()

		ID = data[0]
		
		ip = tivos[tivo_name]

		#update IP in boxes table
		cursor.execute ("UPDATE boxes SET ip=\"" + ip + "\" WHERE ID=\"" + str(ID) + "\"")

		#print row[0]
		print "Tivo Name: " + tivo_name
		print "Tivo IP: " + ip
		print "matching ID: " + str(ID)
		updateTivoShowCache(ID,ip)
