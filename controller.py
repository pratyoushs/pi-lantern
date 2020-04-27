import requests
import json
import time
import datetime
import RPi.GPIO as GPIO
from api._bridge import Bridge
from api._lights import Lights

device_type = {"devicetype": "lantern#pi"}
channel = 16
username = None

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.IN)


b = Bridge()
b.find_bridge()
print(b.ip)
start_time = datetime.time(21, 0, 0)
end_time = datetime.time(6, 0, 0)
begin_timer = None
#print(start_time)
#print(end_time)
#print(datetime.datetime.now().time())
#print(start_time < datetime.datetime.now().time())
#print(datetime.datetime.now().time() - start_time < datetime.timedelta(hours=6))
if b.ip is not None:
    while True:
        time.sleep(5)
        status, user_data = b.create_user(device_type)
        print(status)
        print(username)
        if (status == 200):
            user_data = json.loads(user_data)
            print(user_data)
            if "success" in user_data[0]:
                username = user_data[0]["success"]["username"]
                break
    
    l = Lights(b.ip)
    l.get_lights(username)
    start_time = datetime.time(21, 0, 0)
    end_time = datetime.time(6, 0, 0)
    while True:
        # get input from gpio
        sensor_input = GPIO.input(channel)
        print("sensor input {sensor_input}".format(sensor_input=sensor_input))
        current_time = datetime.datetime.now().time()
        #if (start_time <= current_time <= end_time):
        if True:
            #if gpio input means motion detected
                # if timer is off 
                    # start timer for 5 minutes
                # else
                    # restart timer for 5 minutes
                #if lights are not on
                    #turn on the lights with low brightness
            response = l.get_light_status(username, 1)
            light_data = json.loads(response.content)
            print(light_data)
            if sensor_input == 1:
                print("Movement detected!")
                begin_timer = time.perf_counter()
                if not light_data["state"]["on"]:
                    print("Turning on lights")
                    l.toggle_lights(username, 1, True)
            #if gpio input means motion not detected
                # if timer is zero
                    #turn off the lights
            else:
                print("No movement detected")
                end_timer = time.perf_counter()
                if begin_timer is not None and (end_timer - begin_timer) >= 5:
                    if light_data["state"]["on"]:
                        print("Turning off lights")
                        l.toggle_lights(username, 1, False)
        else:
            print("Not the right time")
        #l.toggle_lights(username, 1, True)
        #time.sleep(5)
        #l.toggle_lights(username, 1, False)
        #time.sleep(5)


#create_user()

