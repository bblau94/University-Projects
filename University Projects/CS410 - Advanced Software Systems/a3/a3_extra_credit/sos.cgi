#!/bin/sh
#Morse code for sos is blinked through arduino led
echo -n "sos" > /dev/ttyACM0
echo date
