import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ticks import ticks_ms, ticks_add, ticks_less
import microcontroller
microcontroller.cpu.frequency = 912000000
print(microcontroller.cpu.frequency)

# Create the I2C bus
i2c0 = busio.I2C(board.SCL0, board.SDA0)
i2c1 = busio.I2C(board.SCL1, board.SDA1)

# Create the ADC object using the I2C bus
ads0 = ADS.ADS1015(i2c0)
ads1 = ADS.ADS1015(i2c1)
# Set Gain on ADS1115
ads0.gain = 1
ads1.gain = 1

# Set data rate on ADS1115
ads0.data_rate = 3300
ads1.data_rate = 3300

ads0.mode = 0
ads1.mode = 0
# Create difrential input on channel 0
chan0 = AnalogIn(ads0, ADS.P0, ADS.P1)
# Create difrential input on channel 1
#chan1 = AnalogIn(ads0, ADS.P2, ADS.P3)
# Create difrential input on channel 2
chan2 = AnalogIn(ads1, ADS.P0, ADS.P1)
# Create difrential input on channel 3
#chan3 = AnalogIn(ads1, ADS.P2, ADS.P3)

# get systmemtime
timenow = time.monotonic_ns()
print("start time", timenow)
count = 0
t_end = timenow + 50000000
print("end time", t_end)
values = {}

while time.monotonic_ns() < t_end:
    vals = [chan0.value,chan2.value]
    values[count]= vals
    count += 1

#timediff = (timenow - timelast)*0.0000001
#print("{:>5.3f}\t{:>5.3f}\t{:>5.3f}".format(timenow,timelast,timediff))
endtime = time.monotonic_ns()
print("ended",endtime)
print(count)
print(values)
