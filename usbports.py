"""
Extracts information on USB devices attached to a Raspberry Pi, mapping physical ports to device files.

:Author:
    Fernando Cosentino
    https://github.com/fbcosentino/python-usbports
    
"""

import subprocess
import os

class UsbPorts:
    """
    The UsbPort class encapsulates the information regarding
    devices connected to USB ports in a Raspberry Pi.
    """
    
	def __init__(self):
        """Constructor. Initializes the internal lists.
        
        <instance>.portMap is a dicionary in the format:
        
        portMap[port path] = device name
        """
		self.availablePorts = self.ListPorts()
		self.portMap = {}
		for eport in self.availablePorts:
			eportid = self.PortPath(eport)
			if eportid is not None:
				self.portMap[eportid] = eport

	def ListPorts(self):
        """Retrieves a list of available USB serial ports connected.
        Scans up to 16 ttyUSB ports and 16 ttyACM ports.
        
        :returns: List of device names (such as '/dev/ttyUSB0')
        """
		path = ''
		i = 0
		plist = []
		while i < 16:
			path = '/dev/ttyUSB'+str(i)
			if (os.path.exists(path)):
				plist.append(path)
			path = '/dev/ttyACM'+str(i)
			if (os.path.exists(path)):
				plist.append(path)
			i += 1
		return plist
		
	def PortPath(self, devname):
        """
        Retrieves the port path for the supplied device name.
        
        Port path is a string in the format:
        '<controller number>.<port number>'
        
        Example: '1.3' -> Controller 1, port 3
        
        If a USB hub is attached, another level is added. Example:
        if a hub is at port 5, a device in 2nd port of the hub will be:
        '1.5.2'
        
        :returns: Port path as string
        """
		try:
			res1 = subprocess.check_output(['udevadm', 'info','--query=property','-n',devname])
		except:
			return None
		props = res1.split("\n")
		proplist = {}
		for eline in props:
			if '=' in eline:
				ekey, eval = eline.split('=')
				proplist[ekey] = eval.strip('\'')
			
		if 'ID_PATH' in proplist:
			epath = proplist['ID_PATH']
			pathitems = epath.split(':')
			plen = len(pathitems)
			if plen == 3:
				return pathitems[1]
			else:
				return None
		else:
			return None
	
	def DeviceAt(self, portid):
        """
        Finds the device name for a serial device connected
        to the specified port path.
        
        Example:
        
        >>> instance.DeviceAt('1.2')
        /dev/ttyUSB0
        
        :returns: Device name as string, or None
        """
		if portid in self.portMap:
			return self.portMap[portid]
		else:
			return None
