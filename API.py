import requests
import json
import os

def getenvirondetails():
    url = os.environ.get('VEEAM_URL_TOKEN')
    headers = os.environ.get('VEEAM_HEADER_TOKEN')
    payload = os.environ.get('VEEAM_PAYLOAD_TOKEN')

    header_dict = json.loads(headers)

    getToken(url, header_dict, payload)


def getToken(url, headers, payload):

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    print(response)


getenvirondetails()