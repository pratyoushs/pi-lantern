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
        current_time = datetime.datetime.now().time()
        if (current_time >= start_time and current_time <= end_time):
            #if gpio input means motion detected
                # if timer is off 
                    # start timer for 5 minutes
                # else
                    # restart timer for 5 minutes
                #if lights are not on
                    #turn on the lights with low brightness
            status = l.get_light_status(username, 1)
            if sensor_input == 1:
                begin_timer = time.perf_counter()
                if not status["state"]["on"]:
                    l.toggle_lights(username, 1, True)
            #if gpio input means motion not detected
                # if timer is zero
                    #turn off the lights
            else:
                end_timer = time.perf_counter()
                if begin_timer is not None and (end_timer - begin_timer) >= 5:
                    if status["state"]["on"]:
                        l.toggle_lights(username, 1, False)

        #l.toggle_lights(username, 1, True)
        #time.sleep(5)
        #l.toggle_lights(username, 1, False)
        #time.sleep(5)


#create_user()

