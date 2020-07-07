import re
import requests
import json
import os


def getenvirondetails():
    url = os.environ.get("VEEAM_URL_TOKEN")
    headers = os.environ.get("VEEAM_HEADER_TOKEN")
    payload = os.environ.get("VEEAM_PAYLOAD_TOKEN")

    header_dict = json.loads(headers)

    getToken(url, header_dict, payload)


def getToken(url, headers, payload):
    response = requests.post(url, verify=False, data=payload, headers=headers)

    access_token = response.json()["access_token"]

    backuprepositories(access_token)


def backuprepositories(access):
    accessnew = "Bearer " + access
    headers = os.environ.get("VEEAM_HEADER_BACKUPREPO")
    url = os.environ.get("VEEAM_URL_BACKUPREPO")
    header_dict = json.loads(headers)
    header_dict['Authorization'] = accessnew

    response = requests.get(url, verify=False, headers=header_dict)

    cleanup(response.json())


def cleanup(r):
    strR = str(r)
    newstring = (strR.replace('"', '').replace(' ', '').replace("'", '').replace('{', '').replace('}',
                                                                   '').replace('[','').replace("]",""))
    list = re.split(":|,", newstring)

    getids(list)


def getids(list):
    id = []

    for item in range(len(list)):
        if list[item] == 'id':
            id.append(list[item+1])

    print(id)





getenvirondetails()
