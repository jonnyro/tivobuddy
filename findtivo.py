import dbus,gobject,avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop
import sys
import inspect, operator
#Look for tivo sharesi
TYPE = '_tivo-videos._tcp'
#dbus.String(u'Gaston')
TIVOS=frozenset(('TIVO1','TIVO2NAME','TIVO3NAME'))
FOUND_TIVOS=set()
TIVO_DATA = dict()

def stop_scan():
    global sbrowser
    global TIVO_DATA
    global main_loop
#    for (key,val) in TIVO_DATA:
#	print key + "," + val
    #print TIVO_DATA
    #sys.exit(0)
    main_loop.quit()

def service_resolved(*args):
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
    #print 'service resolved'
    #print 'name:', args[2]
    #print 'address:', args[7]
    #print 'port:', args[8]

def print_error(*args):
    print 'error_handler'
    print args[0]
    
def myhandler(interface, protocol, name, stype, domain, flags):
    #print "Found service '%s' type '%s' domain '%s' " % (name, stype, domain)

    if flags & avahi.LOOKUP_RESULT_LOCAL:
            # local service, skip
            pass

    server.ResolveService(interface, protocol, name, stype, 
        domain, avahi.PROTO_UNSPEC, dbus.UInt32(0), 
        reply_handler=service_resolved, error_handler=print_error)


def run_scan():
	global server
	global TIVO_DATA
	global sbrowser
	global main_loop

	loop = DBusGMainLoop()

	bus = dbus.SystemBus(mainloop=loop)

	server = dbus.Interface( bus.get_object(avahi.DBUS_NAME, '/'),
        'org.freedesktop.Avahi.Server')

	sbrowser = dbus.Interface(bus.get_object(avahi.DBUS_NAME,
        	server.ServiceBrowserNew(avahi.IF_UNSPEC,
            	avahi.PROTO_UNSPEC, TYPE, 'local', dbus.UInt32(0))),
       	 	avahi.DBUS_INTERFACE_SERVICE_BROWSER)

	sbrowser.connect_to_signal("ItemNew", myhandler)

	main_loop= gobject.MainLoop()
	
	main_loop.run()

	return TIVO_DATA
#print run_scan()
