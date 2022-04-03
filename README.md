# WaterLeakDetector
A smart meter connected to a pi-like device, to notify when the main water pipe is broken, and prevent major leaks that can cost money.

Some info about the project here: https://forums.balena.io/t/build-log-detecting-if-the-main-water-pipe-breaks

Instead of hardocding the SmartMeter register addresses, the project implements a generic datamodel parser to allow different configurations and/or devices.

The project is meant to run on [balena](https://www.balena.io), but the main script works in any PC

Using [this](https://www.waveshare.com/wiki/2-CH_RS485_HAT) HAT to add RS485 to the balenaFin. 

## Selected Protocol registers
For the initial project I've used [this](https://es.aliexpress.com/item/1005003015658136.html) smart meter that includes a modbus slave with many parameters. As per my interest, I've only included in the datamodel the ones I'm going to process. The following is an extract from the manufacturer's doc:

| Register address | Register number | Register Name | Data format | Description |
| - | - | - | - | :-: |
| 0001-0002 | 2 | Instant flow rate | IEEE754 | Unit: m3/h |
| 0137-0138 | 2 | Daily accumulated flow rate | LONG | 9 Digits |
| 0141-0142 | 2 | Monthly accumulated flow rate | LONG |
| 0361-0362 | 2 | Always display 361.00 | IEEE754 | For test |


## How it works

There are basically different existing services and  balenaBlocks from the meter to the algorithm that detects the Leak:

- [tcpmodbus2mqtt](https://hub.balena.io/rmorillo/tcpmodbus2mqtt): By defining a parameter's datamodel, it reads the MODBUS slave and publishes value to an MQTT server
- [mqtt](): A mosquito server
- [connector](https://hub.balena.io/balenablocks/connector): Intelligently connect data sources with data sinks.
- [influxdb](): A database to store read data
- [dashboard](https://hub.balena.io/balenablocks/dashboard): A customizable data visualization tool with automatically generated dashboards.

And finally, the algorith that detects the Leaks, basically detecting when there's water running for too long: the `smartmeterprocessor` service.


## How to try it in your PC

You can try this setup in your PC running a node-red server with the right modules.

* Load `utils/flows.json` file in node-red to run the modbus server simulator. It will act as a smart meter, or any other modbus slave.
* Configure the server with the IP address of your PC
* Run `utils/randomModbusInjector.py` to populate the slave sim with some random data. Beware that the script has the parameters hardcoded, so if you change the `datamodel.json`file you will have to adapt this script. Also, change the IP address to match with the above

Note: The MQTT broker is not needed for the simulator. You will receive a warning, but the script will run

## Acknowledgments
Some inspiration on:
* alanb128 for the algorithm
* balenaLabs and all [balena](https://www.balena.io) team for the great product and support
