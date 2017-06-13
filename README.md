# The Python Presser Library For Luma3DS Unbricked Systems that are Hacked

## What is it?

Luma3DS 8.0 introduced an Input Redirection feature available through the Rosalina menu (L+down+select -> Miscellaneous options... -> InputRedirection) that allows a computer to send inputs to a hacked 3DS. TPPFLUSH is a python library that allows sending inputs via this method.

As it stands now, this library is a work-in-progress.

Supported inputs:
	* ABXY, L/R, Start/Select
	* Circle pad
	* D-pad
	* Touch input

Not yet supported:
	* N3DS C-Stick
	* N3DS ZR and ZL
	* Home and power buttons

## If I'm a developer, how do I use TPPFLUSH in my own python application?

After importing `tppflush`, Create a `LumaInputServer` with the IP of the target 3DS, then call various functions with the appropriate enum of the button you want as appropriate to change the internal state, and finally call `send()` to send the input to the 3DS. *Nothing will happen unless `send()` is called!*

## How do I connect TPPFLUSH to a 3DS?

First, find the IP of your 3DS - FTP applications are useful for figuring this out. Activate input redirection via the rosalina menu (L+down+select -> Miscellaneous options... -> InputRedirection). Finally, run `interactive_buttons.py <3DS IP>` to connect, then type 'A' and press enter to push the A button on the DS.

## I'm not a developer; is this useful to me?

Yes! If you want to control your 3DS from a computer, run interactive_buttons.py for a bare-bones client that works on all platforms, not just windows.

As of June 12, 2017, TPPFLUSH is the only client that works for linux without requiring compiliation. 

## Credits

Thanks to [TuxSH](https://github.com/TuxSH/InputRedirectionClient-Qt) and [Stary2001](https://github.com/Stary2001/InputClient-SDL) for their existing luma3DS clients, which I've copied a lot of code from.
