""" TODO: EVERYTHING
"""

from time import sleep
from driver_comm import ArdPiComm
from master_comm import MasterComm

""" Commands received from master:
	stop
	forward
	backward
	left
	right
	arm_left
	arm_right
	arm_v_pos
	wrist_pos
	open_grasp
	close_grasp
"""

""" Command code list. 
	Keys are received from the master (as strings)
	We must send the corresponding code value to the driver.
"""
DRIVER_COMMANDS = {
	"stop" :		0x00,
	"forward" :		0x03,
	"backward" :	0x0C,
	"left" :		0x0F,
	"right" :		0x30,
	"arm_left" :	0x33,
	"arm_right" :	0x3C,
	"arm_up" :		0x3F,
	"arm_down" :	0xC0,
	"arm_h_pos" :	0xC3,
	"arm_v_pos" :	0xCC,
	"wrist_left" :	0xFF,
	"wrist_right" :	0xF0,
	"wrist_pos" :	0xF3,
	"open_grasp" :	0xFC,
	"close_grasp" :	0xFF
}

driver = None

def command_callback(command, argument):
	# Try to parse the argument into an integer
	try:
		argument = int(argument)
	except ValueError, ve:
		print 'Argument error, not integer'
	else:
		print 'Received command: {}({})'.format(command, argument)
		print 'Sending command: {}({})'.format(DRIVER_COMMANDS[command], argument)
		driver.send(DRIVER_COMMANDS[command], argument)

if __name__ == '__main__':
	driver = ArdPiComm()
	master = MasterComm(command_callback)
	master.start()
	print "Enter 'q' to exit"
	while True:
		stop = raw_input()
		if stop == 'q':
			break
	driver.stop()
	master.stop()