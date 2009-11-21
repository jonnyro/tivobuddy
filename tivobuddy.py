TIVO="TIVO_IP"
MAK="YOURMAKHERE"

import libxml2
import libxslt
import sys
import urllib2
import MySQLdb
import os
import findtivo

def updateTivoShowCache(TIVO_ID, TIVO_IP):

	print "Attempting to open tivo at: " + str(TIVO_IP) + " with ID " + str(TIVO_ID)
	url = "https://" + TIVO_IP + "/TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse=Yes" 
	print "URL=" + url
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
	
	query = "DELETE FROM showbuffer WHERE tivoID=\"%s\"" % str(TIVO_ID)			
	cursor.execute( query )
	
	   

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
			query = "INSERT INTO showbuffer SET tivoID=\"%s\", showname=\"%s\",showtitle=\"%s\",showdescription=\"%s\",showurl=\"%s\"" % tuple(map(MySQLdb.escape_string,(str(TIVO_ID), show, episode_title, description, URL)))
			cursor.execute( query )
		curline = curline + 1



conn = MySQLdb.connect (host = "localhost", user="root", passwd="mysql_root_password", db="tivo") 
cursor = conn.cursor ()
cursor.execute ("SELECT ID,ip,description FROM boxes")

tivos= findtivo.run_scan()
print tivos

for tivo_name in tivos.keys():
	#row = cursor.fetchone ()
	#if row == None:
	#	break
	
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
