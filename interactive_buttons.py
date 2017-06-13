import sys, time
from tppflush import *

if len(sys.argv) < 2:
	print("To run as an executable: python3 lumainput.py <3ds ip>")
	quit()

server = sys.argv[1]

server = LumaInputServer(server)
server.hid_press(HIDButtons.X)
server.send()

def quick_press(button):
	global server
	server.hid_press(button)
	server.send()
	time.sleep(0.3)
	server.hid_unpress(button)
	server.send()

while True:
	btn = input(">")
	if btn.lower() == 'a':
		quick_press(HIDButtons.A)
	if btn.lower() == 'x':
		quick_press(HIDButtons.X)
	if btn.lower() == 'b':
		quick_press(HIDButtons.B)
	if btn.lower() == 'y':
		quick_press(HIDButtons.Y)
