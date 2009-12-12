import dbus,gobject,avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop
import sys
import inspect, operator
import signal, os

#Look for tivo sharesi
TYPE = '_tivo-videos._tcp'
#dbus.String(u'Gaston')
TIVOS=frozenset(('TIVO1','TIVO2NAME','TIVO3NAME'))
FOUND_TIVOS=set()
TIVO_DATA = dict()

class TivoHunter:
	

	def __init__(self,maxDuration=5):
		self.main_loop= gobject.MainLoop()
		self.loop = DBusGMainLoop()
		self.bus = dbus.SystemBus(mainloop=self.loop)

		#Set up an alarm to stop scanning when maxDuration expires
		signal.signal(signal.SIGALRM, self.stop_scan)
		signal.alarm(maxDuration)
		

	def stop_scan(self,signum,frame):
	    for (key,val) in TIVO_DATA:
		print key + "," + val
	    #print TIVO_DATA
	    #sys.exit(0)
	    self.main_loop.quit()

	def service_resolved(self,*args):
	    global TIVOS
	    global FOUND_TIVOS
	    global TIVO_DATA

	    global finished
	    if args[2] in TIVOS:
		FOUND_TIVOS.add(str(args[2]))
		TIVO_DATA[str(args[2])] = str(args[7])
		if FOUND_TIVOS >= TIVOS:
			#print "Stopping scan"
			stop_scan()		
	    print 'service resolved'
	    print 'name:', args[2]
	    print 'address:', args[7]
	    print 'port:', args[8]

	def print_error(self,*args):
	    print 'error_handler'
	    print args[0]
	    
	def myhandler(self,interface, protocol, name, stype, domain, flags):

	    if flags & avahi.LOOKUP_RESULT_LOCAL:
		    # local service, skip
		    pass

	    server.ResolveService(interface, protocol, name, stype, 
		domain, avahi.PROTO_UNSPEC, dbus.UInt32(0), 
		reply_handler=self.service_resolved, error_handler=self.print_error)


	def run_scan(self):
		global server
		global TIVO_DATA
		global sbrowser
		global main_loop


		server = dbus.Interface( self.bus.get_object(avahi.DBUS_NAME, '/'),
		'org.freedesktop.Avahi.Server')

		sbrowser = dbus.Interface(self.bus.get_object(avahi.DBUS_NAME,
			server.ServiceBrowserNew(avahi.IF_UNSPEC,
			avahi.PROTO_UNSPEC, TYPE, 'local', dbus.UInt32(0))),
			avahi.DBUS_INTERFACE_SERVICE_BROWSER)

		sbrowser.connect_to_signal("ItemNew",self.myhandler)

		
		self.main_loop.run()

		return TIVO_DATA

if __name__ == "__main__":
	a = TivoHunter()
	a.run_scan()
	signal.alarm(0)
