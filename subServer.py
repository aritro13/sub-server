import socket
import net
import os
import logging
from time import sleep

logger = logging.getLogger(__name__)

class server:

	def __init__(self):
		
		while True:
			if(!is_socket_closed()):
				self.operations()
			else:
				try:
					self.connectToMainServer()
				except:
					print "Main Server Down"
	
	def connectToMainServer():
		self.name = "SUB-SERVER"
		self.sock = socket.socket()
		self.host = socket.gethostname()
		self.port = 5000
		self.sock.bind(("192.168.1.102", 0))
		self.sock.connect(("192.168.1.101", self.port))

	def is_socket_closed() -> bool:
		try:
			# this will try to read bytes without blocking and also without removing them from buffer (peek only)
			data = self.sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
			if len(data) == 0:
				return True
		except BlockingIOError:
			return False  # socket is open and reading from it would block
		except ConnectionResetError:
			return True  # socket was closed for some other reason
		except Exception as e:
			logger.exception("unexpected exception when checking if a socket is closed")
			return False
		return False

	def operations(self):
		msg = self.sock.recv(1024)
		if msg == 'WHO':
				self.sock.send('123123123*'+self.name)
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
					print msg[1],"File is not exists!!!!!!!!!"


server1 = server()
