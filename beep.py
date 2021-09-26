# Based on rpi-pcspeaker by jsubirat

import RPi.GPIO as GPIO
import time
import itertools
import argparse
import sys

# GPIO speaker output port in the BCM numbering scheme
speakerpin = 22

# Number of steps from A3. Font: http://www.phy.mtu.edu/~suits/NoteFreqCalcs.html
notes = {'A2': -12.0, 'Bb2': -11.0, 'B2': -10.0, 'C3': -9.0, 'Db3': -8.0, 'D3': -7.0, 'Eb3': -6.0, 'E3': -5.0, 'F3': -4.0, 'Gb3': -3.0, 'G3': -2.0, 'Ab3': -1.0, 'A3': 0.0, 'Bb3': 1.0, 'B3': 2.0, 'C4': 3.0, 'Db4': 4.0, 'D4': 5.0, 'Eb4': 6.0, 'E4': 7.0, 'F4': 8.0, 'Gb4': 9.0, 'G4': 10.0, 'Ab4': 11.0, 'A4': 12.0, 'Bb4': 13.0, 'B4': 14.0, 'C5': 15.0, 'Db5': 16.0, 'D5': 17.0, 'Eb5': 18.0, 'E5': 19.0, 'F5': 20.0, 'Gb5': 21.0, 'G5': 22.0, 'Ab5': 23.0}

# Key to note mapping
keys = {'y': 'A2', 's': 'Bb2', 'x': 'B2', 'c': 'C3', 'f': 'Db3', 'v': 'D3', 'g': 'Eb3', 'b': 'E3', 'n': 'F3', 'j': 'Gb3', 'm': 'G3', 'k': 'Ab3', 'q': 'A3', '2': 'Bb3', 'w': 'B3', 'e': 'C4', '4': 'Db4', 'r': 'D4', '5': 'Eb4', 't': 'E4', 'z': 'F4', '7': 'Gb4', 'u': 'G4', '8': 'Ab4', 'i': 'A4', '9': 'Bb4', 'o': 'B4', 'p': 'C5'} #etc.

# Imperial march
FREQS = [ 392, 392, 392, 311.1, 466.2, 392, 311.1, 466.2, 392, 587.32, 587.32, 587.32, 622.26, 466.2, 369.99, 311.1, 466.2, 392, 784, 392, 392, 784, 739.98, 698.46, 659.26, 622.26, 659.26, 415.3, 554.36, 523.25, 493.88, 466.16, 440, 466.16, 311.13, 369.99, 311.13, 392, 466.16, 392, 466.16, 587.32, 784, 392, 392, 784, 739.98, 698.46, 659.26, 622.26, 659.26, 415.3, 554.36, 523.25, 493.88, 466.16, 440, 466.16, 311.13, 392, 311.13, 466.16, 392.00, 311.13, 466.16, 392 ]

LENGTHS = [ 350, 350, 350, 250, 25, 350, 250, 25, 700, 350, 350, 350, 250, 25, 350, 250, 25, 700, 350, 250, 25, 350, 250, 25, 25, 25, 50, 25, 350, 250, 25, 25, 25, 50, 25, 350, 250, 25, 350, 250, 25, 700, 350, 250, 25, 350, 250, 25, 25, 25, 50, 25, 350, 250, 25, 25, 25, 50, 25, 350, 250, 25, 300, 250, 25, 700 ]

PAUSES = [ 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 400, 200, 100, 100, 100, 100, 100, 400, 200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 400, 200, 100, 100, 100, 100, 100, 400, 200, 100, 100, 100, 150, 100, 100, 100 ]

# Sets the desired note at the speaker
def tone ( speaker, note ) :

	frequency = 440.0 * ( 1.05946309435929530984310531 ** notes[note] )
	# 50 Hertz PWM
	p = GPIO.PWM ( speaker, frequency )
	# Duty cicle: 50%
	p.start ( 50 )
	time.sleep ( 0.5 )
	p.stop ( )

# Emulates the beep command, frequency in Hz, length in ms, pause in ms
def beep ( speaker, frequency, length, pause ) :
	p = GPIO.PWM ( speaker, frequency )
	p.start ( 50 )
	time.sleep ( length / 1000.0 )
	p.stop ( )
	time.sleep ( pause / 1000.0 )

# Play the imperial march
def imperial ( speaker ) :
	for ( a, b, c ) in zip ( FREQS, LENGTHS, PAUSES ) :
		beep ( speaker, a, b, c )

# Use keyboard to 'play'
def keyboard ( speaker ) :
	key = ''
	while key != ' ' :
		key = raw_input ( u"Enter a note: " )
		if key in keys.keys ( ) :
			tone ( speaker, keys[key] )
		else :
			if key == ' ' :
				break
			else :
				print ( u"Invalid note (space to exit)!" )

# Sound a sinosoidal alarm 3 times
def alarm ( speaker ) :
	for x in range ( 0, 2 ) :
		alarmfreq = 420
		for i in range ( 50, alarmfreq ) :
			beep ( speaker, i, 20, 2 )
		beep ( speaker, alarmfreq, 15000, 0 )
		for i in range ( alarmfreq, 50, -1 ) :
			beep ( speaker, i, 20, 2 )

# Main code
GPIO.setmode ( GPIO.BCM )
GPIO.setup ( speakerpin, GPIO.OUT )

parser = argparse.ArgumentParser ( description = 'Beep via GPIO' )
parser.add_argument ( '-a', '--alarm', help = 'Sound an alarm', action = 'store_true' )
parser.add_argument ( '-k', '--keyboard', help = 'Play via keyboard', action = 'store_true' )
parser.add_argument ( '-i', '--imperial', help = 'Imperial march', action = 'store_true' )
args = parser.parse_args ( )

if ( len ( sys.argv ) == 1 ) :
	selection = raw_input ( u"Select mode: [A]larm, [K]eyboard, [I]mperial or [Q]uit\n " )
	if selection == "A" or selection == "a" :
		alarm ( speakerpin )
	elif selection == "K" or selection == "k" :
		keyboard ( speakerpin )
	elif selection == "I" or selection == "i" :
		imperial ( speakerpin )
	elif selection == "Q" or selection == "q" :
		GPIO.cleanup ( )
		quit ( )
	else :
		print ( u"Invalid selection!" )
elif ( len ( sys.argv ) > 2 ) :
	print ( u"Only one argument allowed!" )
	GPIO.cleanup ( )
	quit ( )
else :
	if args.alarm :
		alarm ( speakerpin )
	elif args.keyboard :
		keyboard ( speakerpin )
	elif args.imperial :
		imperial ( speakerpin )
	else :
		print ( u"Error in parsing argument!" )

# Clean the state
GPIO.cleanup ( )

#
