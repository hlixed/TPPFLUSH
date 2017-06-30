import sys, time

if sys.version[0] == '2':
	raw_input("This client only works with python 3, and you're using python 2. You can download python 3 from python.org.\nPress enter to exit.")
	quit()

from tppflush import *

if len(sys.argv) < 2:
	input("To run this client, please supply an IP address from the command line: python3 interactive_buttons.py <3ds ip>\nPress enter to exit.")
	quit()

server = sys.argv[1]

server = LumaInputServer(server)
time.sleep(3)
#server.hid_press(HIDButtons.X) #to show it works
#server.send()

def quick_press(button,delay=0.3):
	global server
	server.press(button)
	server.send()
	time.sleep(delay)
	server.unpress(button)
	server.send()

def quick_cpad(button,delay=0.3):
	global server
	server.circle_pad_set(button)
	server.send()
	time.sleep(delay)
	server.circle_pad_set(CPAD_Commands.CPADNEUTRAL)
	server.send()

def quick_touch(x,y,delay=0.3):
	global server
	server.touch(x,y)
	server.send()
	time.sleep(delay)
	server.clear_touch()
	server.send()

def quick_cstick(button,delay=0.3):
	global server
	server.n3ds_cstick_set(button)
	server.send()
	time.sleep(delay)
	server.n3ds_cstick_set(CSTICK_Commands.CSTICKNEUTRAL)
	server.send()

while True:
	#Commands are things like 'a', 'touch 200 200', 'cpadneutral', 'dpadup', or 'cpadup'
	btn = input(">").strip().upper()
	if hasattr(HIDButtons,btn):
		quick_press(HIDButtons[btn])

	if hasattr(N3DS_Buttons,btn):
		quick_press(N3DS_Buttons[btn])

	if hasattr(Special_Buttons,btn):
		quick_press(Special_Buttons[btn])


	if hasattr(CPAD_Commands,btn): #don't forget CPADNEUTRAL is in here
		quick_cpad(CPAD_Commands[btn])
	if hasattr(CSTICK_Commands,btn):
		quick_cstick(CSTICK_Commands[btn])

	if btn.startswith("TOUCH"):
		cmd = btn.split()
		try:
			x = int(cmd[1])
			y = int(cmd[2])
			quick_touch(x,y)
		except ValueError:
			print("Error!")

