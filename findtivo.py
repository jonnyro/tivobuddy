import dbus,gobject,avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop
import sys
import inspect, operator
import signal, os

#Look for tivo sharesi
TYPE = '_tivo-videos._tcp'
#dbus.String(u'Gaston')

class TivoHunter:
	

	def __init__(self,maxDuration=5,debugDuringSearch=False):
		self.main_loop= gobject.MainLoop()
		self.loop = DBusGMainLoop()
		self.bus = dbus.SystemBus(mainloop=self.loop)
		gobject.timeout_add(maxDuration*1000,self.stop_scan)
		self.debug = debugDuringSearch
		self.TIVO_DATA = dict()
		

	def stop_scan(self):
	    self.main_loop.quit()

	def service_resolved(self,*args):
	#	FOUND_TIVOS.add(str(args[2]))
	    self.TIVO_DATA[str(args[2])] = str(args[7])
	    if self.debug:
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
		#global sbrowser
		#global main_loop

		#Set up an alarm to stop scanning when maxDuration expires

		server = dbus.Interface( self.bus.get_object(avahi.DBUS_NAME, '/'),
		'org.freedesktop.Avahi.Server')

		sbrowser = dbus.Interface(self.bus.get_object(avahi.DBUS_NAME,
			server.ServiceBrowserNew(avahi.IF_UNSPEC,
			avahi.PROTO_UNSPEC, TYPE, 'local', dbus.UInt32(0))),
			avahi.DBUS_INTERFACE_SERVICE_BROWSER)

		sbrowser.connect_to_signal("ItemNew",self.myhandler)

		
		self.main_loop.run()
		
		return self.TIVO_DATA

if __name__ == "__main__":
	#Create TivoHunter object, set maximum search time to 5
	a = TivoHunter(maxDuration=5,debugDuringSearch=False)
#	signal.signal(signal.SIGALRM, a.stop_scan)
#	signal.alarm(5)
	print a.run_scan()
	
