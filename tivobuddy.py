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
#			print "Key: " + str(key)
#			print "Value: " + str(value)
			ip = value
			name = key	
#			print "Attempting to open tivo " + name + "  at: " + ip
			url = "https://" + ip + "/TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse=Yes" 
#			print "URL=" + url

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

					if self.tivobdb is not None:
						self.tivobdb.addShowToCache(Show(show, episode_title, description, URL))
				curline = curline + 1

	def getShowByUUID(self,targetUUID):
		showcache = self.getTivoShowCache()
		for (uid, showobj) in showcache:
			if (uid == targetUUID):
				return showobj 
		return None
	def getShowList(self):
		result = set() 
		showcache = self.getTivoShowCache()
		for (uid, showobj) in showcache:
			result.add(showobj.getShowName())
	
		return result	
	def getShowsByName(self,showname):
		result = [] 
		showcache = self.getTivoShowCache()
		for (uid, showobj) in showcache:
			name = showobj.getShowName()
			if (name == showname):
				result.append((uid,showobj))
	
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

