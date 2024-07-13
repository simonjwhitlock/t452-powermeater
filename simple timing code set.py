"""Example for Pico. Turns on the built-in LED."""
import board
import digitalio
import time
import os
import busio
import storage
import adafruit_sdcard
import bitbangio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def flash_count(count):
    done=0
    print("flashing ",count," times.")
    while (done<count):
        done += 1
        print(done)
        led.value = True
        time.sleep(0.5)
        led.value = False
        if (done==count):
            print("DONE")
            break
        time.sleep(0.5)

def timing(interval,timestamp,reps):
    count = 0
    while (count < reps):
        timenext = timestamp + interval
        print("time: ",timestamp," time.time(): ",time.time()," timenext: ",timenext)
        flash_count(10)
        count += 1
        timestamp = wait_timenext(interval,timenext)

        
def wait_timenext(interval,wait_till):
    print("interval: ",interval," wait_till: ",wait_till)
    while time.time() < wait_till:
        time.sleep(0.5)
    return(time.time())

    
timestamp = time.time()
timing(20,timestamp,3)

