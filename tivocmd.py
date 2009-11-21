


TIVO="TIVO_IP"
MAK="YOURMAC"

import libxml2
import libxslt
import sys
import os
import urllib2

url = "https://" + TIVO + "/TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse=Yes" 
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, url, "tivo", MAK)
authhandler = urllib2.HTTPDigestAuthHandler(password_mgr)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)
try: 
	pagehandle = urllib2.urlopen(url)
	html = pagehandle.read()
	pagehandle.close()
except urllib2.HTTPError, e:
	print e.code
	print e.headers
	sys.exit(-1)

styledoc = libxml2.parseFile("tivo.xsl")
style = libxslt.parseStylesheetDoc(styledoc)
doc = libxml2.parseDoc(html)
result = style.applyStylesheet(doc, None)
style.saveResultToFilename("tivoroll.html", result, 0)
style.freeStylesheet()
doc.freeDoc()
result.freeDoc()

shows = [] 

f=open('./tivoroll.html')

for line in f:
	line = line.rstrip()
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
		#We now have all the info we need to display the show
		shows.append([show,episode_title, description, URL])
i=0

for i in range(0,len(shows)):
	print str(i) + " " + shows[i][0] + "-" + shows[i][1]

print "What show do you want?"
num = int(raw_input())

cmd = "/usr/bin/curl -k --digest -u tivo:YOURMAKHERE -c cookies.txt " + "'" + shows[num][3] + "' | /usr/local/bin/tivodecode -m YOURMAKHERE -- - | /usr/bin/mplayer -vf pp=lb -ao alsa -cache 32768 -"

cmd = "/usr/bin/curl -k --digest -u tivo:YOURMAKHERE -c cookies.txt " + "'" + shows[num][3] + "' | /usr/local/bin/tivodecode -m YOURMAKHERE -- - > ./tmp.avi"

#print "You selected" + str(num)
#print "This will be the command: " + cmd
os.system(cmd)
