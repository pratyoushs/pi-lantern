import requests
import json

class Lights:
    def __init__(self, ip_address):
        self.ip = ip_address

    def get_lights(self, username):
        response = requests.get("http://{ip}/api/{username}/lights".format(ip = self.ip, username = username))
        print(response.status_code)
        print(response.content)
        return response

    def get_light_status(self, username, id):
        response = requests.get("http://{ip}/api/{username}/lights/{id}".format(ip = self.ip, username = username, id = id))
        print(response.status_code)
        print(response.content)
        return response

    def toggle_lights(self, username, id, toggleState):
        response = requests.put("http://{ip}/api/{username}/lights/{id}/state".format(ip = self.ip, username = username, id = id),
        json = {"on":toggleState})
        print(response.status_code)
        print(response.content)
        return response

    def change_brightness(self, username, id, brightness):
        if brightness < 1:
            brightness = 1
        elif brightness > 254:
            brightness = 254
        response = requests.put("http://{ip}/api/{username}/lights/{id}/state".format(ip = self.ip, username = username, id = id),
        json = {"bri":brightness})
        print(response.status_code)
        print(response.content)
        return response

    def change_hue(self, username, id, hue):
        if hue < 0:
            hue = 0
        elif hue > 65535:
            hue = 65535
        response = requests.put("http://{ip}/api/{username}/lights/{id}/state".format(ip = self.ip, username = username, id = id),
        json = {"hue":hue})
        print(response.status_code)
        print(response.content)
        return response

    def change_saturation(self, username, id, saturation):
        if saturation < 0:
            saturation = 0
        elif saturation > 254:
            saturation = 254
        response = requests.put("http://{ip}/api/{username}/lights/{id}/state".format(ip = self.ip, username = username, id = id),
        json = {"sat":saturation})
        print(response.status_code)
        print(response.content)
        return response