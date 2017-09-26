import sys, time, math

if sys.version[0] == '2':
	raw_input("This client only works with python 3, and you're using python 2. You can download python 3 from python.org.\nPress enter to exit.")
	quit()

from tppflush import *

if len(sys.argv) < 2:
	input("To run this client, please supply an IP address from the command line: python3 command_examples.py <3ds ip>\nPress enter to exit.")
	quit()


#Create a client by creating a new LumaInputServer with the 3DS's IP address.

serverIP = sys.argv[1]
server = LumaInputServer(serverIP)
time.sleep(5)

#Now, you can press buttons with server.press()!
server.press(HIDButtons.DPADUP)
server.send(print_sent=False)
time.sleep(0.5)

#It's the responsibility of code using TPPFLUSH to send the command to unpress a button.
#That way you can control how long a button is held for.
server.unpress(HIDButtons.DPADUP)
server.send(print_sent=False)
time.sleep(0.5)

#Let's press a few more.
server.press(HIDButtons.A)
server.send(print_sent=False)
time.sleep(0.5)

server.unpress(HIDButtons.A)
server.send(print_sent=False)
time.sleep(0.5)

#Multiple buttons can be pressed at once.
server.press(HIDButtons.L)
server.press(HIDButtons.R)
server.press(HIDButtons.START)
server.press(N3DS_Buttons.ZL) #If an o3DS is connected, this function will do nothing.
server.send(print_sent=False)
time.sleep(0.5)

#You can also release all buttons at once.
server.clear_everything()
time.sleep(0.5)

#The touch screen takes an x and a y coordinate to touch.
#The bottom screen is 320 by 240 pixels big.
server.touch(319,239) #touch the bottom-right of the screen
server.send(print_sent=False)
time.sleep(0.5)

#You can only touch one location at a time. Touching a different location will overwrite the previous coordinates.
server.touch(150,120) #touch the middle of the screen
server.send(print_sent=False)
time.sleep(0.5)

server.clear_touch()
server.send(print_sent=False)
time.sleep(0.5)

#The circle pad works too!
server.circle_pad_set(CPAD_Commands.CPADUP)
server.send(print_sent=False)
time.sleep(0.5)

server.circle_pad_neutral()
server.send(print_sent=False)
time.sleep(0.5)

#The circle_pad_set function also takes a multiplier argument from -1 to 1, so you can use the circle pad without pushing it all the way.
#Let's use it to spin around in a circle!
for i in range(0,180,10):
	server.circle_pad_set(CPAD_Commands.CPADRIGHT, math.cos(i))
	server.circle_pad_set(CPAD_Commands.CPADUP, math.sin(i))
	server.send(print_sent=False)
	time.sleep(0.1)

server.circle_pad_neutral()
server.circle_pad_set(CPAD_Commands.CPADNEUTRAL) #this also resets the circle pad
server.send(print_sent=False)
time.sleep(0.5)

#The N3DS C-stick works the same way.
#This will do nothing if you're on an o3ds.
server.n3ds_cstick_set(CSTICK_Commands.CSTICKUP,0.5)
server.send(print_sent=False)
time.sleep(0.5)

#These will both reset the c-stick.
server.n3ds_cstick_set(CSTICK_Commands.CSTICKNEUTRAL)
server.n3ds_cstick_neutral()
server.send(print_sent=False)

#There are also some specialized buttons available:
#server.press(Special_Buttons.HOME)
#server.press(Special_Buttons.POWER) #as if you tapped the power button
#server.press(Special_Buttons.POWER_LONG) #as if you held down the power button

#Hope this helps!
