MAK="YOURMAKHERE"
import ConfigParser
import libxml2
import libxslt
import sys
import urllib2
import os
import pickle

from findtivo import TivoHunter
from tivobuddydb import Show, TivoBuddyDB

class TivoBuddy:

	def __init__(self,MAK):
		self.mak = MAK
		self.tivobdb = None
	def setBackingStore(self, tivobdb):
		self.tivobdb = tivobdb

	def getTivoShowCache(self):
		if self.tivobdb is not None:
			return self.tivobdb.getCacheContents()	
		else:
			return None
	def updateTivoShowCache(self):
		hunter = TivoHunter()
		tivos = hunter.run_scan()
		print tivos
		for (key,value) in tivos.items():
			print "Key: " + str(key)
			print "Value: " + str(value)
			ip = str(value)
			name = str(key)	
			print "Attempting to open tivo " + name + "  at: " + ip
			url = "https://" + ip + "/TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse=Yes" 
			print "URL=" + url

			#TODO: Set up gettivo.sh to accept Media Access Key as argument.
			cmd = "./gettivo.sh " + ip + " " + self.mak 
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
			
			   
			#Iterate line by line over tivoroll.html converting each line
			# into a format suitable for insertion into database
			item = 0
			curline = 0
			for line in f:
				linearr = line.split("|")

				if (linearr[0] == "Show"):
					show = linearr[1].rstrip("\n")
					episode_title = ""
					description = ""
					URL = ""
				if (linearr[0] == "EpisodeTitle"):
					episode_title = linearr[1].rstrip("\n")
				if (linearr[0] == "Description"):
					description = linearr[1].rstrip("\n")
				if (linearr[0] == "URL"):
					URL = linearr[1].rstrip("\n")
					#insert show entry into database
		#			query = "INSERT INTO showbuffer SET tivoID=\"%s\", showname=\"%s\",showtitle=\"%s\",showdescription=\"%s\",showurl=\"%s\"" % tuple(map(MySQLdb.escape_string,(str(TIVO_ID), show, episode_title, description, URL)))
					#cursor.execute( query )
					#Now we have everything to add to db
		#			print "Show: " + show
		#			print "EP:   " + episode_title

					if self.tivobdb is not None:
						self.tivobdb.addShowToCache(Show(show, episode_title, description, URL))
				curline = curline + 1


	def getShowList(self):
		result = set() 
		showcache = self.getTivoShowCache()
		for (uid, showobj) in showcache:
			result.add(showobj.getShowName())
	
		return result	
if __name__ == "__main__":

	#First try to obtain mak from .tivodecode_mak
	mak=""
	makfile = os.path.expanduser("~/.tivodecode_mak")
	try:
		f = open(makfile,"r")
		str = f.read()
		mak = str
		f.close()
	except:
		print "Unexpected error:", sys.exc_info()[0]

		print "Please enter MAK"
		mak = raw_input()
		try:
			f = open(makfile,"w")
			f.write(mak)
			f.close()	
		except:
			pass
	a = TivoBuddy(mak)
	print " Attempting to re-use existing show cache"
	try:
		input = open("tivocache.pck","rb")
		d = pickle.load(input)
		input.close()
		print "Pre-existing show cache loaded"
		a.setBackingStore(d) 
	except:	
		print "unable to load pre-existing show cache"
		d = TivoBuddyDB()
		a.setBackingStore(d)
		a.updateTivoShowCache()
		output = open("tivocache.pck","wb")
		pickle.dump(d,output)
		output.close()
		print "Show cache updated"
	print a.getShowList()

#	print a.getTivoShowCache()
comment = """


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


	def loadGlobalSettings(self):
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

"""
