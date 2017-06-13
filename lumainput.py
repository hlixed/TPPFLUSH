import socket #imports module allowing connection to IRC
from enum import IntFlag, auto

import sys

if len(sys.argv) < 2:
	print("Usage: python3 lumainput.py <3ds ip>")
	quit()

server = sys.argv[1]

tsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 4950
tsocket.connect((server, port))

circle_state = bytearray.fromhex("007ff7ff")
cstick_state = bytearray.fromhex("80800081")
touch_state =  bytearray.fromhex("02000000");
special_buttons = bytearray(4)
hid_buttons =  bytearray.fromhex("fffff000")
hid_state = bytearray.fromhex("fefff000")

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

current_pressed_buttons = HIDButtons.A ^ HIDButtons.A #no buttons

def hid_press(button):
	global current_pressed_buttons
	if button not in current_pressed_buttons:
		current_pressed_buttons |= button
	print(current_pressed_buttons)

def hid_unpress(button):
	global current_pressed_buttons
	if button in current_pressed_buttons:
		current_pressed_buttons ^= button
	print(current_pressed_buttons)

def hid_toggle(button):
	global current_pressed_buttons
	current_pressed_buttons ^= button

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

def send():
	toSend = bytearray(20) #create empty byte array
	toSend[0:4] = hid_state
	toSend[4:8] = touch_state
	toSend[8:12] = circle_state
	toSend[12:16] = cstick_state
	toSend[16:20] = special_buttons
	print(toSend)
	tsocket.send(toSend)

send()

