import paho.mqtt.client as mqttClient
import time
import os
import json
from datetime import datetime

# Getting the current date and time
def on_connect(client, userdata, flags, rc):
    print("On connect...")
    if rc == 0:
  
        print("Connected to broker")
  
        global Connected                #Use global variable
        Connected = True                #Signal connection 
  
    else:
  
        print("Connection failed")

def on_message(client, userdata, message):
    #print ("Message received: "  + str(type(message.payload)))
    m = json.loads(message.payload)
    #print(json.dumps(m))
    for param,value in m.items():
        if param == "instant_flow":
            processInstantFlow(value),
        elif param == "daily_accumulated_flow_rate":
            print("daily accumulated flow T.D.C")
        elif param == "monthly_accumulated_flow":
            print("Monthly accumiulated flow T.B.C.")
        elif param == "reading_test":
            if value != 361:
                print("MODBUS SYNC ERROR. EXITING.")
                exit()
    

def getDuration(then, now = datetime.now(), interval = "default"):

    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

    duration = now - then # For build-in functions
    duration_in_s = duration.total_seconds() 
    
    def years():
      return divmod(duration_in_s, 31536000) # Seconds in a year=31536000.

    def days(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 86400) # Seconds in a day = 86400

    def hours(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 3600) # Seconds in an hour = 3600

    def minutes(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 60) # Seconds in a minute = 60

    def seconds(seconds = None):
      if seconds != None:
        return divmod(seconds, 1)   
      return duration_in_s

    def totalDuration():
        y = years()
        d = days(y[1]) # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        return "Time between dates: {} years, {} days, {} hours, {} minutes and {} seconds".format(int(y[0]), int(d[0]), int(h[0]), int(m[0]), int(s[0]))

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': totalDuration()
    }[interval]


def processInstantFlow(instantFlow):
    global previousInstantFlow, previousTimestamp, numberOfPositiveFlowReadings
    print("Instanto flow: %s (previous: %s)" %(instantFlow, previousInstantFlow))
    if instantFlow != 0:
        if previousInstantFlow == 0:
            previousInstantFlow = instantFlow
            previousTimestamp = datetime.now()
            numberOfPositiveFlowReadings = 1
        else:
            timePassed = getDuration(previousTimestamp, datetime.now(), 'minutes')
            numberOfPositiveFlowReadings += 1
            previousInstantFlow = instantFlow
            #if timepassed > os.getenv("    "):            
            if int(timePassed) > 5: 
                print("--------ALERT-------")
                print("%s readings with positive water flow in %s minutes " %(numberOfPositiveFlowReadings, timePassed))
                print("--------ALERT-------")
    else:
        previousInstantFlow = 0
        numberOfPositiveFlowReadings = 0

  
Connected = False   #global variable for the state of the connection
  
broker_address= os.environ['MQTT_BROKER_IP']  #Broker address
port = os.environ['MQTT_BROKER_PORT']                         #Broker port
user = "yourUser"                    #Connection username
password = "yourPassword"            #Connection password
  
client = mqttClient.Client("mqtt")               #create new instance
# client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback

previousInstantFlow = 0
previousTimestamp = datetime.now()
numberOfPositiveFlowReadings = 0

try:
    client.connect(broker_address, int(port))          #connect to broker
except Exception as e:
    print("Error connecting to MQTT broker %s:%s" %(broker_address, port))

print("Connected to MQTT broker %s:%s" %(broker_address, port))

client.loop_start()        #start the loop
  
while Connected != True:    #Wait for connection
    time.sleep(0.1)

topic = "sensors"
try:
    client.subscribe(topic)
except Exception as e:
    print("Error subscribing to topic %s" %topic)

print("Subscribed to topic %s" %topic)


try:
    while True:
        time.sleep(1)
  
except Exception as e:
    print ("exiting...")
    print(e)
    client.disconnect()
    
    client.loop_stop()