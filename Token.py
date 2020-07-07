import requests


class Token():
    def __init__(self, url, headers, payload):
        self.url = url
        self.headers = headers
        self.payload = payload

    def getToken(self):
        response = requests.post(self.url, verify=False, data=self.payload, headers=self.headers)

        access_token = response.json()["access_token"]

        return access_token
