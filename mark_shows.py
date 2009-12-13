#Mark shows for conversion
import os
import random
import sys
import pickle
from tivobuddy import TivoBuddy
from tivobuddydb import Show, TivoBuddyDB
from converter import TivoConverter
from zlib import crc32
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
	print a.getShowList()	
	#conv.convertShowsByName("M*A*S*H")
	
else:
	print "This file is meant to be run directly, not imported"
