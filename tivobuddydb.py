#!/usr/bin/env/python

#TivoBuddyDB.py

#Copyright (c) 2009 Jonathan S. Romero

import uuid

class Show:
	def __init__(self,showname,title,description=None,url=None,ip=None):
		self.showname 	 = showname
		self.title	 = title
		self.description = description
		self.url	 = url
		self.ip 	 = ip
	def getTitle(self):
		return self.title
	def getDescription(self):
		return self.description
	def getURL(self):
		return self.url
	def getShowName(self):
		return self.showname
	def getFriendlyFilename(self):
		filename = self.showname + "-" + self.title
		filename = filename.replace(" ", "-")
		filename = filename.replace("*", "_")
		filename = filename.replace("\'", "_")
		filename = filename.replace(";", "_")
		filename = filename.replace('&', "and")
		print "Title: " + self.title + " Showname: " + self.showname + " Converted Title: " + filename
		return filename
	def getIP(self):
		return self.ip
class TivoBuddyDB:
	def __init__(self):
		self.shows = []
		self.encodequeue = []
	def initializeBackingStore(self):
		pass
	def addShowToCache(self,ShowObj):
		GUID = uuid.uuid4().hex
		self.shows.append((GUID,ShowObj))
	def clearShowCache(self):
		self.shows = []
	def getCacheContents(self):
		return self.shows	
	def markShowForEncode(self,GUID):
		self.encodequeue.append(GUID)
	def clearEncodeQueue(self):
		self.encodequeue=[]

if __name__ == "__main__":
	print "Basic Tests of TivoBuddyDB"
	db = TivoBuddyDB()
	db.addShowToCache(Show(title="Knight Rider",description="Car jumps over another car"))
	print db.getCacheContents()
