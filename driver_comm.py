""" Module to implement the communication protocol between the Raspberry Pi
	and the Arduino in Roberto over a serial port.
"""

import serial
import sys
from time import sleep

MAX_RETRIES = 3

class ArdPiComm(object):
	"""Class to handle the serial object and implement the communication protocol"""
	
	def __init__(self, port='/dev/ttyACM0', baudrate=9600):
		print 'Connecting to serial port...'
		try:
			self.ser = serial.Serial(port=port, baudrate=baudrate)
		except serial.serialutil.SerialException:
			print '\nSerial device not connected. Program aborted.\n'
			sys.exit(1)
		except ValueError as ve:
			print '\nSerial parameters not valid.\n'
			raise ve
		else:
			print 'Done!\n'
		

	def stop(self):
		if self.ser.isOpen():
			print '\nClosing serial port...'
			self.ser.close()
			print 'Serial port closed.'
		else:
			print 'Serial port is already closed.'

	def send(self, command, argument=0):

		retries = 0
		command = command & 0xFF
		argument = argument & 0xFF

		print 'Sending command {c}, with argument {a}'.format(c=command, a=argument)

		self.ser.write(chr(command))
		self.ser.write(chr(argument))
		
		while self.check_ack() == 0 and retries < MAX_RETRIES:
			self.ser.write(chr(command))
			self.ser.write(chr(argument))
			retries += 1
			sleep(0.1) # 100ms between each retry


		if retries == MAX_RETRIES:
			# No ACK after MAX_RETRIES
			print 'Could not send command {c}, with argument {a}'.format(c=command, a=argument)
			return False
		else:
			return True


	def check_ack(self):
		print 'Receiving ACK...'
		ack = 0
		if self.ser.inWaiting() > 0:
			ack = ord(self.ser.read(1))
		print 'ACK received: {}'.format(ack)
		return ack

if __name__ == '__main__':
	# Test
	comm = ArdPiComm()
	while True:
		command = raw_input()
		if command == 's':
			print 'Sending stop command'
			comm.send(0x00)
		elif command == 'f':
			print 'Sending forward command'
			comm.send(0x03, 50)
		elif command == 'q':
			break
	comm.stop()

