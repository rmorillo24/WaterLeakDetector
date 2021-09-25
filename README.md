# WaterLeakDetector
A smart meter connected to a pi-like device, to notify when the main water pipe is broken, and prevent major leaks that can cost money.

Some info about the project here: https://forums.balena.io/t/build-log-detecting-if-the-main-water-pipe-breaks

Instead of hardocding the SmartMeter register addresses, the project implements a generic datamodel parser to allow different configurations and/or devices.

The project is meant to run on [balena](https://www.balena.io), but the main script works in any PC

## Selected Protocol registers
For the initial project I've used [this](https://es.aliexpress.com/item/1005003015658136.html) smart meter that includes a modbus slave with many parameters. As per my interest, I've only included in the datamodel the ones I'm going to process. The following is an extract from the manufacturer's doc:

| Register address | Register number | Register Name | Data format | Description |
| - | - | - | - | :-: |
| 0001-0002 | 2 | Instant flow rate | IEEE754 | Unit: m3/h |
| 0137-0138 | 2 | Daily accumulated flow rate | LONG | 9 Digits |
| 0141-0142 | 2 | Monthly accumulated flow rate | LONG |
| 0361-0362 | 2 | Always display 361.00 | IEEE754 | For test |


## How it works
### Datamodel
The datamodel.json file defines the parameters I want to read from my modbus slave. The idea is that anyone can use this to add any other parameter with my initial smart meter, or with another one supporting modbus. 
An example of a parameter that will be automatically be read:

```
    "instant_flow": {
                "address": 1,
                "length": 2,
                "polling_secs": 25,
                "format": "ieee754"
    }
```

The format of the data model allows to configure

* Input or output variables
* Register address
* Number of registers to read for this parameter
* format of the value (will be decoded accordingly)


## Reading and looping
Each parameter has a polling time, that may depend on the meaning of the parameter. The script will spawn a process for each parameter. This process will loop infinitelly, with a sleeping time bewteen loops equaling the polling time we have defined


## Acknowledgments
Some inspiration on:
* [modbus2mqtt](https://github.com/Instathings/modbus2mqtt)
* [modbus-herdsman-converters](https://github.com/Instathings/modbus-herdsman-converters)
A smart meter connected to a pi-like device running a balena app, to notify when the main water pipe is broken, and prevent major leaks that can cost money.
Some info about the project here: https://forums.balena.io/t/build-log-detecting-if-the-main-water-pipe-breaks

