from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
from collections import OrderedDict
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder

import numpy as np    
import os
import time

ORDER_DICT = {
    "<": "LITTLE",
    ">": "BIG"
}

client = ModbusClient('192.168.1.132', port=10502)
client.connect()

print("Starting random positive floats injector")

while(1):
    my_random = np.random.uniform(0, 1000)

    builder = BinaryPayloadBuilder(byteorder=Endian.Little,
                                    wordorder=Endian.Little)
    builder.add_32bit_float(my_random)
    payload = builder.to_registers()
    print("Value: %s -> %s" % (my_random,payload))
    payload = builder.build()
    address = 1

    #Writing into the slave
    client.write_registers(address, payload, skip_encode=True, unit=1)

    #Reading to check if it's stored
    result = client.read_holding_registers(address, len(payload),  unit=1)
    print("Read raw: %s" % payload)

    #Decoding to check if the value is the same
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers,Endian.Little, Endian.Little)
    print("Read decoded: %s" % decoder.decode_32bit_float())

    time.sleep(25)


