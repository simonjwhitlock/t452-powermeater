# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Alec Delaney
#
# SPDX-License-Identifier: MIT
import os
import busio
import digitalio
import board
import storage
import adafruit_sdcard
import bitbangio


# Connect to the card and mount the filesystem.
spi = bitbangio.SPI(board.CLK, board.CMD, board.DAT0)
cs = digitalio.DigitalInOut(board.DAT3)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

csv_colheads = "col1,col2,col3"

with open("/sd/log.txt", "w") as sdc:
    sdc.write("{}\n".format(csv_colheads))
    
value1 = 100
value2 = 200
value3 = 300

with open("/sd/log.txt", "a") as sdadd:
    sdadd.write("{},{},{}\n".format(value1,value2,value3))
    
f = open('/sd/log.txt', 'r')
file = f.read()
print(file)