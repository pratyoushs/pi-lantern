import requests
import json
import time
import datetime
import RPi.GPIO as GPIO
from api._bridge import Bridge
from api._lights import Lights

class Controller:

    def __init__(self):
        self.device_type = {"devicetype": "lantern#pi"}
        self.channel = 16
        self.bridge = None
        self.light = None

    def set_GPIO_data(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.channel, GPIO.IN)
        pass

    def connect_to_bridge(self):
        self.bridge = Bridge()
        self.bridge.find_bridge()
        print(self.bridge.ip)

    def connect_to_light(self, username):
        self.light = Lights(self.bridge.ip)
        self.light.get_lights(username)

    def toggle_night_lamp(self, username, toggle_value):
        if toggle_value:
            self.light.toggle_lights(username, 1, True)
            self.light.toggle_lights(username, 2, True)
            self.light.change_xy(username, 1, 0.6, 0.5)
            self.light.change_xy(username, 2, 0.6, 0.5)
            self.light.change_brightness(username, 1, 50)
            self.light.change_brightness(username, 2, 50)
            #self.light.change_hue(username, 1, 23)
            #self.light.change_hue(username, 2, 23)
            self.light.change_saturation(username, 1, 254)
            self.light.change_saturation(username, 2, 254)
            
        else:
            self.light.toggle_lights(username, 1, False)
            self.light.toggle_lights(username, 2, False)

    def main(self):
        self.set_GPIO_data()
        self.connect_to_bridge()
        username = None
        begin_timer = None
        if self.bridge.ip is not None:
            while True:
                time.sleep(5)
                self.status, self.user_data = self.bridge.create_user(self.device_type)
                print(self.status)
                print(username)
                if (self.status == 200):
                    self.user_data = json.loads(self.user_data)
                    print(self.user_data)
                    if "success" in self.user_data[0]:
                        username = self.user_data[0]["success"]["username"]
                        break
            self.connect_to_light(username)
            while True:
                # get input from gpio
                sensor_input = GPIO.input(self.channel)
                print("sensor input {sensor_input}".format(sensor_input=sensor_input))
                current_datetime = datetime.datetime.now()
                if current_datetime <= current_datetime.replace(hour=7, minute=0, second=0, microsecond=0) or \
                    current_datetime >= current_datetime.replace(hour=21, minute=0, second=0, microsecond=0):
                    if True:
                        #if gpio input means motion detected
                            # if timer is off 
                                # start timer for 5 minutes
                            # else
                                # restart timer for 5 minutes
                            #if lights are not on
                                #turn on the lights with low brightness
                        response = self.light.get_light_status(username, 1)
                        light_data = json.loads(response.content)
                        print(light_data)
                        if sensor_input == 1:
                            print("Movement detected!")
                            begin_timer = time.perf_counter()
                            if not light_data["state"]["on"]:
                                print("Turning on lights")
                                self.toggle_night_lamp(username, True)
                        #if gpio input means motion not detected
                            # if timer is zero
                                #turn off the lights
                        else:
                            print("No movement detected")
                            end_timer = time.perf_counter()
                            if begin_timer is None or \
                               begin_timer is not None and (end_timer - begin_timer) >= 60:
                                if light_data["state"]["on"]:
                                    print("Turning off lights")
                                    self.toggle_night_lamp(username, False)
                else:
                    print("Not the right time")


if __name__ == '__main__':
    print("Inside main")
    controller = Controller()
    controller.main()



