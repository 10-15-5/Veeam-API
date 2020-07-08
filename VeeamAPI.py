import re
from API import *


def welcomeScreen():
    print("Welcome to the Veeam API requests program what would you like to do?")
    print("1) Create a Repo\n2) Display Repos")
    ans = input()

    if ans == "1":
        createarepo()
    elif ans == "2":
        displayrepos()


def token():
    token = Token()
    access = Token.getToken(token)

    return access


def proxy(access):
    proxy = Proxies(access)
    r = Proxies.getProxies(proxy)

    response = cleanup(r)

    for item in range(len(response)):
        if response[item] == "id":
            proxyid = response[item + 1]

    return proxyid


def createarepo():
    access = token()
    proxyid = proxy(access)

    payload = {}

    name = input("Name of repo:\t")
    path = input("Path of repo:\t")
    description = input("Description of repo:\t")
    retentiontype = input("Retention Type (ItemLevel or SnapshotBased):\t")
    retentionperiodtype = input("Retention Period Type (Daily, Monthly, Yearly):\t")
    retentionperiod = input("Retention Period ('Daily' - '14', 'Monthly' - '3', 'Yearly' - 'Years4'):\t")
    retentionfrequency = input("Retention Frequency Type (Daily or Monthly):\t")

    payload["Name"] = name
    payload["ProxyId"] = proxyid
    payload["Path"] = path
    payload["Description"] = description
    payload["RetentionType"] = retentiontype
    payload["RetentionPeriodType"] = retentionperiodtype
    payload["RetentionPeriod"] = retentionperiod
    payload["RetentionFrequency"] = retentionfrequency

    if retentionfrequency == 'Daily':
        dailytime = input("Daily Time (08:00:00):\t")
        dailytype = input("Daily Type (Sunday, Everyday, Workdays):\t")
        payload["DailyTime"] = dailytime
        payload["DailyType"] = dailytype
    else:
        monthlytime = input("Monthly Time (08:00:00):\t")
        monthlydaynumber = input("Monthly Day Number (First, Third, Last):\t")
        monthlydayofweek = input("Monthly Day of Week (Sunday, Tuesday):\t")
        payload["MonthlyTime"] = monthlytime
        payload["MonthlyDayNumber"] = monthlydaynumber
        payload["MonthlyDayOfWeek"] = monthlydayofweek

    repo = CreateRepo(payload)
    r = CreateRepo.create(repo)


def cleanup(r):
    strR = str(r)
    newstring = (strR.replace('"', '').replace(' ', '').replace("'", '').replace('{', '').replace('}',
                                                               '').replace('[','').replace( "]", ""))
    list = re.split(":|,", newstring)

    return list



def displayrepos():
    access = token()

    repo = DisplayRepo(access)
    r = DisplayRepo.displayRepos(repo)
    cleaned = cleanup(r)

    repos = []
    for item in range(len(cleaned)):
        if cleaned[item] == "name":
            repos.append(cleaned[item + 1])

    print(repos)




welcomeScreen()