import struct
import binascii
import time
import os
import paho.mqtt.client as mqtt
import json

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder


from struct import *
from pymodbus.client.sync import ModbusTcpClient

import logging
logging.basicConfig()
log = logging.getLogger()
#log.setLevel(logging.DEBUG)

UNIT = 0x1
error = False

#Read servers variables. If they don't exist, print error, and exit
try:
    modbus_host = os.environ['MODBUS_HOST_IP']
    modbus_port = os.environ['MODBUS_HOST_PORT']
    mqtt_ip = os.environ['MQTT_BROKER_IP']
    mqtt_port = os.environ['MQTT_BROKER_PORT']
except:
    print("MODBUS slave address and/or MQTT broker variables not set.")
    error = True

#Reading parameters address, length and polling time
#Defaulting values if variables dont exists
try:
    instant_flow_address = int(os.environ['REG_INSTANT_FLOW'])
except:
    instant_flow_address = 1
print("Setting flow address register number to %s" %instant_flow_address)

try:
    instant_flow_length = int(os.environ['LENGTH_INSTANT_FLOW'])
except:
    instant_flow_length = 2
print("Setting register length to %s" %instant_flow_length)

#TO-DO: Specify a different polling time per variable
try:
    polling_time = int(os.environ['MODBUS_POLLING_SECS'])
except:
    polling_time = 2
print("Setting polling time to %s" %polling_time)

#Connecting to servers

try:
    client = ModbusTcpClient(modbus_host, modbus_port)
    client.connect()
    print("Connected to modbus server %s:%s" %(modbus_host, modbus_port))
except:
    print("Unable to connect to MODBUS slave.")
    error = True

try:
    mqttc = mqtt.Client("modbusreader")  # Create instance of client with client ID “digitest”
    mqttc.connect(mqtt_ip, int(mqtt_port))  # Connect to (broker, port, keepalive-time)
except:
    print("Unable to connect to MQTT server.")
    error = True

print("Connected to mqtt server %s:%s" %(mqtt_ip, mqtt_port))


#Start polling loop
while (not error):
    try:
        #Read input registers
        rr = client.read_holding_registers(instant_flow_address, instant_flow_length, unit=1)
        assert(not rr.isError())     # test that we are not an error
        assert(rr.function_code < 0x80) # test that we are not an error

        print ("Read: %s" %rr.registers)

        # Decoding PYTHON FLOAT IEEE 754
        decoder = BinaryPayloadDecoder.fromRegisters(rr.registers, Endian.Little, Endian.Little)
        try:
            value = decoder.decode_32bit_float()
            print ("Reading 32bit_float is ", value)
        except:
                print("error decoder 32bit_float")
                pass

        # Convert to JSON to send mqtt
        json_value = {
            "instant_flow": value
            }
        print ("Sending mqtt message to ", mqtt_ip, mqtt_port)
        mqttc.publish("sensors", json.dumps(json_value)) 

        time.sleep(polling_time)
    
    except Exception as e:
        print("Error. Exiting.", e)
        error = True