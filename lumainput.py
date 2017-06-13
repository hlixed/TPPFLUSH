import socket #imports module allowing connection to IRC
from enum import IntFlag, auto


class HIDButtons(IntFlag):
	A = auto()
	B = auto()
	SELECT	= auto()
	START = auto()
	DPADRIGHT = auto()
	DPADLEFT = auto()
	DPADUP = auto()
	DPADDOWN = auto()
	R = auto()
	L = auto()
	X = auto()
	Y = auto()



def bytearray_not(arr):
	return bytearray([255-i for i in arr])

class LumaInputServer():
	def __init__(self, server, port=4950):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		port = 4950
		self.socket.connect((server, port))

		self.current_pressed_buttons = HIDButtons.A ^ HIDButtons.A #no buttons

		#button-pressing functions
		#these do nothing until self.send() is called.
	def hid_press(self, button):
		if button not in self.current_pressed_buttons:
			self.current_pressed_buttons |= button

	def hid_unpress(self, button):
		if button in self.current_pressed_buttons:
			self.current_pressed_buttons ^= button

	def hid_toggle(self, button):
		self.current_pressed_buttons ^= button

	def send(self):
		circle_state = bytearray.fromhex("007ff7ff")
		cstick_state = bytearray.fromhex("80800081")
		touch_state =  bytearray.fromhex("02000000");
		special_buttons = bytearray(4)

		hid_buttons = self.current_pressed_buttons.to_bytes(4,byteorder='little')
		hid_state = bytearray_not(hid_buttons)

		toSend = bytearray(20) #create empty byte array
		toSend[0:4] = hid_state
		toSend[4:8] = touch_state
		toSend[8:12] = circle_state
		toSend[12:16] = cstick_state
		toSend[16:20] = special_buttons
		print(toSend)
		self.socket.send(toSend)

"""
	if(circle_x != 0 || circle_y != 0) // Do circle magic. 0x5d0 is the upper/lower bound of circle pad input
	{
		uint32_t x = circle_x;
		uint32_t y = circle_y;
		x = ((x * CPAD_BOUND) / 32768) + 2048;
		y = ((y * CPAD_BOUND) / 32768) + 2048;
		circle_state = x | (y << 12);
	}

	if(cstick_x != 0 || cstick_y != 0 || zlzr_state != 0)
	{
		double x = cstick_x / 32768.0;
		double y = cstick_y / 32768.0;

		// We have to rotate the c-stick position 45deg. Thanks, Nintendo.
		uint32_t xx = (uint32_t)((x+y) * M_SQRT1_2 * CPP_BOUND) + 0x80;
		uint32_t yy = (uint32_t)((y-x) * M_SQRT1_2 * CPP_BOUND) + 0x80;

		cstick_state = (yy&0xff) << 24 | (xx&0xff) << 16 | (zlzr_state&0xff) << 8 | 0x81;
	}

	if(touching) // This is good enough.
	{
		uint32_t x = touch_x;
		uint32_t y = touch_y;
		x = (x * 4096) / window_w;
		y = (y * 4096) / window_h;
		touch_state = x | (y << 12) | (0x01 << 24);
}"""

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("To run as an executable: python3 lumainput.py <3ds ip>")
		quit()

	server = sys.argv[1]

	server = LumaInputServer(server)
	server.hid_press(HIDButtons.X)
	server.send()
	
