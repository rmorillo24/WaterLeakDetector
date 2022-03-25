#!/usr/bin/env python
import minimalmodbus
import serial

instrument = minimalmodbus.Instrument('/dev/ttySC0', 1) # port name, slave address (in decimal)

instrument.serial.port          # this is the serial port name
instrument.serial.baudrate = 9600   # Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.05   # seconds


## Read temperature (PV = ProcessValue) ##
test = instrument.read_long(361) # Registernumber, number of decimals
print (test)

