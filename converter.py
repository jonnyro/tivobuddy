#Automated show converter utility, uses tivobuddy to retrieve updated showcache
import os
import random
import sys
import pickle
from tivobuddy import TivoBuddy
from tivobuddydb import Show, TivoBuddyDB

class TivoConverter:
	def __init__(self,MAK):
		self.tivobdy = None
		self.mak = MAK
	def setTivoManager(self, tivobdy):
		self.tivobdy = tivobdy	
	def convertShowsByName(self, showname):
		if self.tivobdy is not None:
			shows = self.tivobdy.getShowsByName(showname)
			for (uid,show) in shows:
				self.convertShowByGUID(uid)
	def convertShowByGUID(self,targetUUID):
		if self.tivobdy is not None:
			showobj = self.tivobdy.getShowByUUID(targetUUID)
			filename = showobj.getFriendlyFilename()			
			url = showobj.getURL() 
			print "Filename: " + filename
			print "URL: " + url

			command = "/usr/bin/curl -k --digest -u tivo:" + self.mak + " -c cookies.txt \'" + url + "\' | tivodecode -m " + self.mak + " -- - > tmp.avi"
			os.system(command)

			command = "ffmpeg -y -i tmp.avi -b 600k tmp.avi.mp4"
			res = os.system(command)
			if (res == 0):
				command = "mv tmp.avi.mp4 " + "~/video_output/" + filename
				res = os.system(command)

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
	#print a.getShowList()

	conv = TivoConverter(mak)
	conv.setTivoManager(a)
	
	conv.convertShowsByName("M*A*S*H")
	
