""" TODO: DOC
"""

import socket
from time import sleep
from threading import Thread


PORT = 7070


class MasterComm(Thread):
	"""Thread to receive and process the commands from the master"""
	
	def __init__(self, callback, address=''):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((address, PORT))

		self.command_callback = callback

		Thread.__init__(self)
		self.daemon = True
		self.running = True

	def run(self):
		print 'MasterComm thread running'
		buff = ''
		while self.running:
			new_data, addr = self.sock.recvfrom(1024)
			buff += new_data
			endl = buff.find('\n')
			if endl != -1:
				data = buff[:endl]
				buff = buff[endl+1:]
				command,argument = data.split(',')
				# Process the command outside here.
				# Both comand and argument shall be parsed in the callback function,
				# so this interface is command-agnostic
				self.command_callback(command, argument)
			sleep(0.02)


	def stop(self):
		print 'Stopping comms'
		self.sock.close()
		self.running = False


def test_callback(command, argument):
	try:
		argument = int(argument)
	except ValueError, ve:
		print 'Argument error, not a byte'
	except TypeError, te:
		print 'Argument error, not integer'
	else:
		print 'Received command: {}({})'.format(command, argument)


if __name__ == '__main__':
	# TEST
	comms = MasterComm(test_callback)
	comms.start()
	sleep(10)
	comms.stop()
