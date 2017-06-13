import sys, time
from tppflush import *

if len(sys.argv) < 2:
	print("To run as an executable: python3 lumainput.py <3ds ip>")
	quit()

server = sys.argv[1]

server = LumaInputServer(server)
server.hid_press(HIDButtons.X) #to show it works
server.send()

def quick_press(button,delay=0.3):
	global server
	server.hid_press(button)
	server.send()
	time.sleep(delay)
	server.hid_unpress(button)
	server.send()

def quick_cpad(button,delay=0.3):
	global server
	server.circle_pad_set(button)
	server.send()
	time.sleep(delay)
	server.circle_pad_set(CPAD_Commands.CPADNEUTRAL)
	server.send()

while True:
	btn = input(">").strip().upper()
	if hasattr(HIDButtons,btn):
		quick_press(HIDButtons[btn])

	if hasattr(CPAD_Commands,btn): #don't forget CPADNEUTRAL is in here
		quick_cpad(CPAD_Commands[btn])
