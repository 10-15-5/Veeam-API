import requests
import os
import json
import time


class Token():

    def __init__(self):
        self.url = os.environ.get("VEEAM_URL")
        self.headers = os.environ.get("VEEAM_HEADER")
        self.payload = os.environ.get("VEEAM_PAYLOAD_TOKEN")

    def getToken(self):
        header_dict = json.loads(self.headers)
        tokenurl = self.url + "Token"
        response = requests.post(tokenurl, verify=False, data=self.payload, headers=header_dict).json()

        access_token = response["access_token"]
        #       localtime = time.asctime(time.localtime(time.time()))

        return access_token


class Proxies():

    def __init__(self, token):
        self.token = token
        self.url = os.environ.get("VEEAM_URL")
        self.header = os.environ.get("VEEAM_HEADER_AUTH")

    def getProxies(self):
        proxyurl = self.url + "Proxies"
        header_dict = json.loads(self.header)
        accessnew = "Bearer " + self.token
        header_dict["Authorization"] = accessnew

        response = requests.get(proxyurl, verify=False, headers=header_dict).json()

        return response


class DisplayRepo():

    def __init__(self, token):
        self.token = token
        self.url = os.environ.get("VEEAM_URL")
        self.header = os.environ.get("VEEAM_HEADER_AUTH")

    def displayRepos(self):
        repourl = self.url + "BackupRepositories"
        header_dict = json.loads(self.header)
        accessnew = "Bearer " + self.token
        header_dict["Authorization"] = accessnew

        response = requests.get(repourl, verify=False, headers=header_dict).json()

        return response


'''
class CreateRepo():
    def __init__(self, name, proxyid, path, description, retentiontype, retentionperiodtype, retentionperiod,
                 retentionfrequency, dailytime, dailytype):
        self.name = name
        self.proxyid = proxyid
        self.path = path
        self.description = description
        self.retentiontype = retentiontype
        self.retentionperiodtype = retentionperiodtype
        self.retentionperiod = retentionperiod
        self.retentionfrequency = retentionfrequency
        self.dailytime = dailytime
        self.dailytype = dailytype

    def create(self):

'''
