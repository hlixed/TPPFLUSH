import socket #imports module allowing connection to IRC
from enum import IntFlag, Flag, auto


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

class CPAD_Commands(Flag):
	CPADUP = auto()
	CPADDOWN = auto()
	CPADLEFT	= auto()
	CPADRIGHT = auto()
	CPADNEUTRAL = auto() #sets cpad to 0,0

class CSTICK_Commands(Flag): #N3DS c-stick
	CSTICKUP = auto()
	CSTICKDOWN = auto()
	CSTICKLEFT	= auto()
	CSTICKRIGHT = auto()
	CSTICKNEUTRAL = auto() #sets cstick to 0,0

class N3DS_Buttons(IntFlag):
	ZL = 2
	ZR = 4

def bytearray_not(arr):
	return bytearray([255-i for i in arr])

class LumaInputServer():
	def __init__(self, server, port=4950):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		port = 4950
		self.socket.connect((server, port))

		self.CPAD_BOUND = 0x5d0
		self.CPP_BOUND = 0x7f #what does this stand for? Circle Pad Pro?
		self.SQRT_ONEHALF = 0.707106781186547524401
		self.TOUCHSCREEN_SIZES = [320,240]

		self.current_pressed_buttons = HIDButtons.A ^ HIDButtons.A #no buttons
		self.circle_pad_coords = [0,0] #0,0 is the center
		self.touch_pressed = False
		self.current_touch_coords = [0,0]
		self.cstick_coords = [0,0] #n3ds c-stick, not the circle pad
		self.zlzr_state = N3DS_Buttons.ZL ^ N3DS_Buttons.ZL #n3ds zl and zr

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

	def n3ds_zlzr_press(self, button):
		if button not in self.zlzr_state:
			self.n3ds_zlzr_toggle(button)

	def n3ds_zlzr_unpress(self, button):
		if button in self.zlzr_state:
			self.n3ds_zlzr_toggle(button)

	def n3ds_zlzr_toggle(self, button):
		self.zlzr_state ^= button

	def touch(self,x,y):
		if x >= self.TOUCHSCREEN_SIZES[0] or y >= self.TOUCHSCREEN_SIZES[1] or x < 0 or y < 0:
			raise ValueError

		self.touch_pressed = True
		self.current_touch_coords = [int(x),int(y)]

	def clear_touch(self):
		self.touch_pressed = False

	def circle_pad_set(self, button, multiplier=1):
		if button == CPAD_Commands.CPADUP:
			self.circle_pad_coords[1] = 32767*multiplier
		if button == CPAD_Commands.CPADDOWN:
			self.circle_pad_coords[1] = -32767*multiplier
		if button == CPAD_Commands.CPADLEFT:
			self.circle_pad_coords[0] = -32767*multiplier
		if button == CPAD_Commands.CPADRIGHT:
			self.circle_pad_coords[0] = 32767*multiplier
		if button == CPAD_Commands.CPADNEUTRAL: #resets cpad
			self.circle_pad_coords = [0,0]

	def circle_pad_neutral(self):
		self.circle_pad_coords = [0,0]

	def n3ds_cstick_set(self, button, multiplier=1):
		if button == CSTICK_Commands.CSTICKUP:
			self.cstick_coords[1] = 32767*multiplier
		if button == CSTICK_Commands.CSTICKDOWN:
			self.cstick_coords[1] = -32767*multiplier
		if button == CSTICK_Commands.CSTICKLEFT:
			self.cstick_coords[0] = -32767*multiplier
		if button == CSTICK_Commands.CSTICKRIGHT:
			self.cstick_coords[0] = 32767*multiplier
		if button == CSTICK_Commands.CSTICKNEUTRAL:
			self.cstick_coords = [0,0]

	def send(self):
		special_buttons = bytearray(4)

		hid_buttons = self.current_pressed_buttons.to_bytes(4,byteorder='little')
		hid_state = bytearray_not(hid_buttons)

		circle_state = bytearray.fromhex("7ff7ff00")
		if self.circle_pad_coords[0] != 0 or self.circle_pad_coords[1] != 0: # "0x5d0 is the upper/lower bound of circle pad input", says stary2001
			x,y = self.circle_pad_coords
			x = ((x * self.CPAD_BOUND) // 32768) + 2048
			y = ((y * self.CPAD_BOUND) // 32768) + 2048
			circle_state = (x | (y << 12)).to_bytes(4,byteorder='little')

		touch_state = bytearray.fromhex("20000000")
		if(self.touch_pressed):
			x,y = self.current_touch_coords
			x = (x * 4096) // self.TOUCHSCREEN_SIZES[0]
			y = (y * 4096) // self.TOUCHSCREEN_SIZES[1]
			touch_state = (x | (y << 12) | (0x01 << 24)).to_bytes(4,byteorder='little')


		n3ds_exclusives_state = bytearray.fromhex("81008080")
		if self.cstick_coords[0] != 0 or self.cstick_coords[1] != 0 or self.zlzr_state != 0:
			x = self.cstick_coords[0] / 32768.0
			y = self.cstick_coords[1] / 32768.0

			#TuxSH note: We have to rotate the c-stick position 45deg. Thanks, Nintendo.
			rotated_x = int(((x+y) * self.SQRT_ONEHALF * self.CPP_BOUND) + 0x80)
			rotated_y = int(((y-x) * self.SQRT_ONEHALF * self.CPP_BOUND) + 0x80)
			#rotated_x and rotated_y are between 0 and 0xff now

			n3ds_exclusives_state = ((rotated_y&0xff) << 24 | (rotated_x&0xff) << 16 | (self.zlzr_state&0xff) << 8 | 0x81).to_bytes(4,byteorder='little')

		toSend = bytearray(20) #create empty byte array
		toSend[0:4] = hid_state
		toSend[4:8] = touch_state
		toSend[8:12] = circle_state
		toSend[12:16] = n3ds_exclusives_state
		toSend[16:20] = special_buttons
		print(toSend)
		self.socket.send(toSend)

"""
	if(cstick_x != 0 || cstick_y != 0 || zlzr_state != 0)
	{
		double x = cstick_x / 32768.0;
		double y = cstick_y / 32768.0;

		// We have to rotate the c-stick position 45deg. Thanks, Nintendo.
		uint32_t xx = (uint32_t)((x+y) * M_SQRT1_2 * CPP_BOUND) + 0x80;
		uint32_t yy = (uint32_t)((y-x) * M_SQRT1_2 * CPP_BOUND) + 0x80;

		n3ds_exclusives_state = (yy&0xff) << 24 | (xx&0xff) << 16 | (zlzr_state&0xff) << 8 | 0x81;
	}


}"""

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("To run as an executable: python3 lumainput.py <3ds ip>")
		quit()

	server = sys.argv[1]

	server = LumaInputServer(server)

	#example commands
	server.hid_press(HIDButtons.X) # hold x
	server.circle_pad_set(CPAD_Commands.CPADUP)
	server.touch(319,239) #touch the bottom-right of the screen
	
	#send inputs to 3DS
	server.send()
	
