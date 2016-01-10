CS 410 
Physical Computing Extra Credit Section - Tyler Butler, Ben Blau, Jeffery Zurita

The morse_code file is in .txt format currently.

For the extra physical computing portion, we used an Arduino Uno with no expansions for our hardware. We made an "SOS.cgi" file that can be executed on our webserver, which then writes the characters "sos" to the computer's serial port that is connected to the Arduino. 

The Arduino receives input from the computer's serial port, and reads in the characters "sos" that were written. Then, for each character read in, we execute code that blinks the Arduino's internal LED with the corresponding morse code value for the character read in. 

Modifications:
With more time, we could modify the web server to take input from an HTML text form and submit it to a CGI file which would then write it to the serial port, allowing users to input strings to the web server that will be flashed on the Arduino's LED in morse code. 


