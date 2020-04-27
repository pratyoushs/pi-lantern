import requests
import json

class Bridge:

    def __init__(self):
        self.ip = None
        self.username = None


    def find_bridge(self):
        response = requests.get("http://www.meethue.com/api/nupnp")
        for item in json.loads(response.text):
            try:
                #print(item["id"] + " " + item["internalipaddress"])
                descriptionResponse = requests.get("http://{ip}/description.xml".format(ip = item["internalipaddress"]))
                #print(descriptionResponse.text)
                if "<modelDescription>Philips hue Personal Wireless Lighting</modelDescription>" in descriptionResponse.text:
                    #print("Found the ip address: {ip}".format(ip=item["internalipaddress"]))
                    self.ip = item["internalipaddress"]
                break
            except:
                print("Not the right ip address")
            finally:
                pass

    def create_user(self, device_type):
        response = requests.post("http://{ip}/api".format(ip = self.ip), json=device_type)
        #print(response.status_code)
        #print(response.content)
        return (response.status_code, response.text)