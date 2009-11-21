import MySQLdb
import os
import random
import sys

MAK="YOURMAKHERE"


query = """ SELECT showbuffer.ID,showID, showname, showtitle, showurl FROM conversion_menu, showbuffer WHERE showbuffer.ID=conversion_menu.showID AND status="UNTOUCHED" """

query = """ SELECT ID,showname,showurl,showtitle FROM showbuffer WHERE showname LIKE "%Breaking Bad%" """

print "Query:" + query
conn = MySQLdb.connect (host = "localhost", user="root", passwd="mysql_root_pw", db="tivo") 
cursor = conn.cursor ()
cursor.execute(query)

while(1):
	row = cursor.fetchone ()
	if row == None:
		break
	print row
	#Sometimes we dont have an episode title, just a show title
	showname = str(row[1]).splitlines()[0].strip()
	showtitle= row[3].splitlines()[0].strip() 
	if row[3] == "":
		episodetitle= str(random.randint(0,65530))
	else:
		episodetitle= row[3].splitlines()[0].strip()
	
	filename = showname + "-" + showtitle + ".mp4"
	filename = filename.replace(" ", "-")
	url = row[2].splitlines()[0]	
	print "Filename: " + filename
	print "URL: " + url

	command = "/usr/bin/curl -k --digest -u tivo:" + MAK + " -c cookies.txt \'" + url + "\' | tivodecode -m " + MAK + " -- - > tmp.avi"
	#query = """ UPDATE conversion_menu SET status="IN_PROGRESS", completed_filename="%s", last_command="%s"  WHERE showID="%s" """ % (filename, command, row[0])
	
	#print "Executing query:" + query
	#cursor.execute(query)
	os.system(command)

	command = "ffmpeg -y -i tmp.avi -b 600k tmp.avi.mp4"
	res = os.system(command)
	if (res == 0):
		command = "mv tmp.avi.mp4 " + "~/video_output/" + filename
		res = os.system(command)

#	if (res == 0):
#		query = """ UPDATE conversion_menu SET status="COMPLETED", filename="%s"  WHERE showID="%s" """ % (filename, row[0])
#	else:
#		query = """ UPDATE conversion_menu SET status="ERR" WHERE showID="%s" """ % (row[0])
#	print "Executing query:" + query
#	cursor.execute(query)
		
