import requests
import os

def getenvirondetails():
    url = os.environ.get("VEEAM_URL_TOKEN")
    headers = os.environ.get("VEEAM_HEADER_TOKEN")
    payload = os.environ.get("VEEAM_PAYLOAD_TOKEN")

    header_dict = json.loads(headers)

    getToken(url, header_dict, payload)



response = requests.post(url, verify=False, data=payload, headers=headers)

    access_token = response.json()["access_token"]

    backuprepositories(access_token)
