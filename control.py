#!/usr/bin/python
import serial
import csv
import struct

ser=serial.Serial()
ser.port="/dev/ttyUSB1"
ser.baudrate=115200
ser.timeout=1
ser.open()

STEP = 0
LED = 1
COUNT = 2

def step():
    # take a step
    ser.write(struct.pack('B', STEP ));
    data = ser.read(1)

def read(reg):
    ser.write(struct.pack('B', reg ));
    data = ser.read(1) # 1 byte hard coded
    data, = struct.unpack('B', data)
    return data

with open("dumpvar" + '.csv', 'wb') as csvfile:
    wr = csv.writer(csvfile, delimiter=',')
    for i in range(2000):
        leds = read(LED)
        count = read(COUNT)
        step()

        wr.writerow([i, leds, count])
