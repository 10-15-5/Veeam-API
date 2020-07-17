import requests
import os
import json
import datetime
import re


class Token:

    def __init__(self):
        self.url = os.environ.get("VEEAM_URL")
        self.headers = os.environ.get("VEEAM_HEADER")
        self.payload = os.environ.get("VEEAM_PAYLOAD_TOKEN")
        self.time = datetime.datetime.now()

    def getToken(self):
        if not os.path.isfile("token.txt"):
            with open("token.txt", "w+") as file:
                header_dict = json.loads(self.headers)
                tokenurl = self.url + "Token"
                response = requests.post(tokenurl, verify=False, data=self.payload, headers=header_dict).json()

                access_token = response["access_token"]
                current = self.time.strftime("%Y-%m-%d %H:%M:%S")
                writelist = [current, access_token]
                file.write(str(writelist))
                return access_token
        try:
            with open("token.txt", "r+") as file:
                if os.stat("token.txt").st_size == 0:
                    header_dict = json.loads(self.headers)
                    tokenurl = self.url + "Token"
                    response = requests.post(tokenurl, verify=False, data=self.payload, headers=header_dict).json()

                    access_token = response["access_token"]
                    current = self.time.strftime("%Y-%m-%d %H:%M:%S")
                    writelist = [current, access_token]
                    file.write(str(writelist))
                    return access_token
                else:
                    f = file.read()
                    file.close()

            oldtoken = (f.replace("[", "").replace("]", "").replace("'", ""))
            oldtoken = re.split(",", oldtoken)

            current = self.time.strftime("%Y-%m-%d %H:%M:%S")
            datetimenow = datetime.datetime.strptime(current, "%Y-%m-%d %H:%M:%S")
            datetimeold = datetime.datetime.strptime(oldtoken[0], "%Y-%m-%d %H:%M:%S")

            diff = datetimenow - datetimeold
            min = diff.seconds / 60

            if min > 60:
                header_dict = json.loads(self.headers)
                tokenurl = self.url + "Token"
                response = requests.post(tokenurl, verify=False, data=self.payload, headers=header_dict).json()

                access_token = response["access_token"]
                with open("token.txt", "w") as file:
                    writelist = [current, access_token]
                    file.write(str(writelist))
                    file.close()
                return access_token
            else:
                return oldtoken[1]

        except IOError:
            print("Stop")


class Proxies:

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


class Display:

    def __init__(self, token):
        self.token = token
        self.url = os.environ.get("VEEAM_URL")
        self.header = os.environ.get("VEEAM_HEADER_AUTH")

    def repo(self):
        repourl = self.url + "BackupRepositories"
        header_dict = json.loads(self.header)
        accessnew = "Bearer " + self.token
        header_dict["Authorization"] = accessnew

        response = requests.get(repourl, verify=False, headers=header_dict).json()

        return response

    def org(self):
        orgurl = self.url + "Organizations"
        header_dict = json.loads(self.header)
        accessnew = "Bearer " + self.token
        header_dict["Authorization"] = accessnew

        response = requests.get(orgurl, verify=False, headers=header_dict).json()

        return response


class Creation:

    def __init__(self, payload, token):
        self.payload = payload
        self.token = token
        self.url = os.environ.get("VEEAM_URL")
        self.header = os.environ.get("VEEAM_HEADER_AUTH")

    def repo(self):
        createurl = self.url + "BackupRepositories"
        header_dict = json.loads(self.header)
        accessnew = "Bearer " + self.token
        header_dict["Authorization"] = accessnew
        header_dict["Content-Type"] = "application/json"

        response = requests.post(createurl, verify=False, data=json.dumps(self.payload), headers=header_dict).json()

        return response

    def org(self):
        orgurl = self.url + "Organizations"
        header_dict = json.loads(self.header)
        accessnew = "Bearer " + self.token
        header_dict["Authorization"] = accessnew
        header_dict["Content-Type"] = "application/json"

        response = requests.post(orgurl, verify=False, data=json.dumps(self.payload), headers=header_dict).json()

        return response


class Removal:

    def __init__(self, token, removeid):
        self.token = token
        self.removeid = removeid
        self.url = os.environ.get("VEEAM_URL")
        self.header = os.environ.get("VEEAM_HEADER_AUTH")

    def repo(self):
        remurl = self.url + "BackupRepositories/" + self.removeid
        header_dict = json.loads(self.header)
        accessnew = "Bearer " + self.token
        header_dict["Authorization"] = accessnew
        header_dict["Content-Type"] = "application/json"

        response = requests.delete(remurl, verify=False, headers=header_dict).json()

        return response

    def org(self):
        remurl = self.url + "Organizations/" + self.removeid
        header_dict = json.loads(self.header)
        accessnew = "Bearer " + self.token
        header_dict["Authorization"] = accessnew
        header_dict["Content-Type"] = "application/json"

        response = requests.delete(remurl, verify=False, headers=header_dict).json()

        return response


class DisplayJobs:

    def __init__(self, token, orgid):
        self.token = token
        self.orgid = orgid
        self.url = os.environ.get("VEEAM_URL")
        self.header = os.environ.get("VEEAM_HEADER_AUTH")

    def jobs(self):
        joburl = self.url + "Organizations/" + self.orgid + "/Jobs"
        header_dict = json.loads(self.header)
        accessnew = "Bearer " + self.token
        header_dict["Authorization"] = accessnew
        header_dict["Content-Type"] = "application/json"

        response = requests.get(joburl, verify=False, headers=header_dict).json()

        return response


class Organization:

    def __init__(self, token, id, payload):
        self.token = token
        self.id = id
        self.payload = payload
        self.url = os.environ.get("VEEAM_URL")
        self.header = os.environ.get("VEEAM_HEADER_AUTH")

    def createjob(self):
        joburl = self.url + "Organizations/" + self.id + "/Jobs"
        header_dict = json.loads(self.header)
        accessnew = "Bearer " + self.token
        header_dict["Authorization"] = accessnew
        header_dict["Content-Type"] = "application/json"

        response = requests.post(joburl, verify=False, data=json.dumps(self.payload), headers=header_dict).json()

        return response

    def modifyjob(self):
        joburl = self.url + "Jobs/" + self.id
        header_dict = json.loads(self.header)
        accessnew = "Bearer " + self.token
        header_dict["Authorization"] = accessnew
        header_dict["Content-Type"] = "application/json"

        response = requests.put(joburl, verify=False, data=json.dumps(self.payload), headers=header_dict).json()

        return response

    def managejob(self):
        joburl = self.url + "Jobs/" + self.id + "/Action"
        header_dict = json.loads(self.header)
        accessnew = "Bearer " + self.token
        header_dict["Authorization"] = accessnew
        header_dict["Content-Type"] = "application/json"

        response = requests.post(joburl, verify=False, data=json.dumps(self.payload), headers=header_dict).json()

        return response
