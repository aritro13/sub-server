import socket
import net
import os
import logging
from time import sleep

logger = logging.getLogger(__name__)

class server:

	def __init__(self):
                self.connectToMainServer()
                self.startServer()

        def startServer(self):
		while True:
                            try:
                                print "Starting Ops"
                                self.operations()
                            except Exception as e:
                                print "Operations Failed: ", e
                                self.connectToMainServer()

	def connectToMainServer(self):
	    self.name = "SUB-SERVER"
            self.sock = socket.socket()
            self.port = 5000
            self.host = socket.gethostname()
            self.sock.bind(("192.168.1.104", 0))
            try:
		self.sock.connect(("192.168.1.101", self.port))
                print "Connection Established"
            except Exception as e:
                print "Main Server Down", e
                sleep(1)

	def operations(self):
		msg = self.sock.recv(1024)
                print "MSG:", msg, type(msg)
		if msg == 'WHO':
		    self.sock.send('123123123*'+self.name)
                if msg == '':
                    self.connectToMainServer()
                if '*' in msg:
			msg = msg.split('*')
			print "Query : ",msg
			if msg[0] == 'PREPARE':
				self.sock.send("READY")
				net.downloadFile(msg[1],self.sock)
				print "Chunk "+msg[1]+" is stored on "+self.name
			if msg[0] == 'MAKE':
				self.sock.send('READY?')
				sleep(1)
				net.uploadFile(msg[1],self.sock)
				#print "Chunk "+msg[1]+" is on mainserver by "+self.name
			if msg[0] == "DEL":
				print "Deletion Command received..",msg[1]
				if os.path.isfile(msg[1]):
					os.remove(msg[1])
					print "Deleted",msg[1]
				else:
					print msg[1],"File does not exists!!!!!!!!!"


server1 = server()
