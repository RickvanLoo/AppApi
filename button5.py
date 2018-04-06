import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)  
# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.  
# Both ports are wired to connect to GND on button press.  
# So we'll be setting up falling edge detection for both  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# GPIO 24 set up as an input, pulled down, connected to 3V3 on button press  
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
  
# now we'll define two threaded callback functions  
# these will run in another thread when our events are detected  
def my_callback(channel):  
    print "aan/uit"
 
def my_callback2(channel):  
    print "Next Song"  
  
def my_callback3(channel):
	print " vol Down"

def my_callback4(channel):
	print " vol up"

def my_callback5(channel):
	print "Connect/Disconnect" 
  
# when a falling edge is detected on port 17, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback, bouncetime=900)  
GPIO.add_event_detect(4, GPIO.RISING, callback=my_callback2, bouncetime=900)
GPIO.add_event_detect(27, GPIO.RISING, callback=my_callback3, bouncetime=900)
GPIO.add_event_detect(17, GPIO.RISING, callback=my_callback4, bouncetime=900)  
GPIO.add_event_detect(25, GPIO.RISING, callback=my_callback5, bouncetime=900)  
  
try:  
    print "System active"  
    input=raw_input()
    if input == "stop":
	sys.exit(0) 
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit 
