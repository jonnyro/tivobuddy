#!/usr/bin/env/python

#TivoBuddyDB.py

#Copyright (c) 2009 Jonathan S. Romero

import uuid

class Show:
	def __init__(self,title,description=None,url=None):
		self.title	 = title
		self.description = description
		self.url	 = url
	def getTitle(self):
		return self.title
	def getDescription(self):
		return self.description
	def getURL(self):
		return self.url

class TivoBuddyDB:
	def __init__(self):
		self.shows = []
		self.encodequeue = []
	def initializeBackingStore(self):
		pass
	def addShowToCache(self,ShowObj):
		GUID = uuid.uuid4()
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
