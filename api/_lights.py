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

    def change_lights(self, username, id):
        response = requests.put("http://{ip}/api/{username}/lights/{id}/state".format(ip = self.ip, username = username, id = id),
        json = {"on":False})
        print(response.status_code)
        print(response.content)
        return response