#Automated show converter utility, uses tivobuddy to retrieve updated showcache
import os
import random
import sys
import pickle
from tivobuddy import TivoBuddy
from tivobuddydb import Show, TivoBuddyDB
from zlib import crc32
class EncoderTargetManager:
	def __init__(self):
		try:
			input = open("showstoencode.pck","rb")
			self.showstoencode = pickle.load(input)
			input.close()
			print "Shows to encode list loaded"
		except:
			print "No shows to encode list found. Creating blank."
			self.showstoencode = []
			output = open("showstoencode.pck","wb")
			pickle.dump(self.showstoencode,output)
			output.close()
			
	def __del__(self):
		print "Storing shows to encode archive"
		output = open("showstoencode.pck","wb")
		pickle.dump(self.showstoencode,output)
		output.close()
	def getShowsToEncode(self):
		return self.showstoencode
	def addShowToEncode(self,show):
		print "Adding show to encode queue " + show
		self.showstoencode.append(show)
	def clearEncodeList(self):
		self.showstoencode = []
class TivoConverter:
	def __init__(self,MAK):
		self.tivobdy = None
		self.mak = MAK
		self.encodelog = []
		self.presetEncodeLog()
	def __del__(self):
		self.commitEncodeLog()
	def presetEncodeLog(self):
		print " Attempting to re-use existing encode log"
		try:
			input = open("tivoencodelog.pck","rb")
			self.encodelog = pickle.load(input)
			input.close()
			print "Pre-existing encode log loaded"
#			a.setBackingStore(d) 
		except:
			print "No existing encode log found, starting with empty log"	
	def commitEncodeLog(self):
		try:
			output = open("tivoencodelog.pck","wb")
			pickle.dump(self.encodelog,output)
			output.close()
			print "Encode log stored"
		except:
			print "Unable to store encode log"

	def setTivoManager(self, tivobdy):
		self.tivobdy = tivobdy	
	def convertShowsByName(self, showname):
		if self.tivobdy is not None:
			shows = self.tivobdy.getShowsByName(showname)
			random.shuffle(shows)
			for (uid,show) in shows:
				self.convertShowByGUID(uid)
	def convertShowByGUID(self,targetUUID):
		if self.tivobdy is not None:
			showobj = self.tivobdy.getShowByUUID(targetUUID)
			filename = showobj.getFriendlyFilename() 
 
			for fname in self.encodelog:
				if filename == fname:
					print "Skipping " + filename + " because it's already in encode log"
					return

			url = showobj.getURL() 

			command = "/usr/bin/curl -k --retry 9 --digest -u tivo:" + self.mak + " -c cookies.txt \'" + url + "\' -o " + filename + ".tivo"
			res = os.system(command)

			if (res == 0):
				command = "time tivodecode -o " + filename + ".mp2 " + filename + ".tivo"
				res = os.system(command)
			if (res == 0):
				os.system("rm -f " + filename + ".tivo")
				command = "HandBrakeCLI --preset iPod -S 700 --two-pass -i " + filename + ".mp2 -o " + filename + ".mp4"
	
				res = os.system(command)
			if (res == 0):
				os.system("rm -f " + filename + ".mp2")
				res = os.system("mv " + filename + ".mp4 ~/video_output")
				self.encodelog.append(filename)
				self.commitEncodeLog()

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
	print "Intentionally refreshing show cache"
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

	ws = EncoderTargetManager()
	
	for show in ws.getShowsToEncode():
		conv.convertShowsByName(show)
	
