#!/usr/bin/python
import serial
import csv
ser=serial.Serial()
ser.port="/dev/ttyUSB1"
ser.baudrate=115200
ser.timeout=1
ser.open()

#ser.setDTR(True)
import struct
with open("dumpvar" + '.csv', 'wb') as csvfile:
    wr = csv.writer(csvfile, delimiter=',')
    for i in range(2000):
        # take a step
        ser.write(struct.pack('B', 0 ));
        data = ser.read(1)

        #read led reg
        ser.write(struct.pack('B', 1 ));
        data = ser.read(1)
        data, = struct.unpack('B', data)
        leds = data

        ser.write(struct.pack('B', 2 ));
        data = ser.read(1)
        data, = struct.unpack('B', data)
        count = data

        wr.writerow([i, leds, count])
