from API import *
import warnings


def welcomeScreen():
    print("Welcome to the Veeam API requests program are you Client or Admin")
    ans = input().lower()

    if ans == "c":
        print("1) Create a Repo\t2) Display Repos\n3) Create Org\t\t4) Display Orgs\n5) Create a Job\t\t"
              "6) Display all Jobs\t\t7) Modify a Job")
    elif ans == "a":
        print("1) Create a Repo\t\t2) Display Repos\n3) Create Org\t\t\t4) Display Org\n5) Create a Job\t\t\t"
              "6) Display all Jobs\n7) Mod a Job's Settings\t8) Display Org Jobs\n9) Remove Repo\t\t\t10) Remove Org"
              "\n11) Manage Jobs")
    ans = input()

    if ans == "1":
        createarepo()
    elif ans == "2":
        displayrepos()
    elif ans == "3":
        createorg()
    elif ans == "4":
        displayorgs()
    elif ans == "5":
        createjob()
    elif ans == "6":
        displayalljobs()
    elif ans == "7":
        modifyjobsettings()
    elif ans == "8":
        displayorgjobs()
    elif ans == "9":
        removerepo()
    elif ans == "10":
        removeorg()
    elif ans == "11":
        managejobs()


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


def cleanup(r):
    strR = str(r)
    newstring = (strR.replace('"', '').replace(' ', '').replace("'", '').replace('{', '').replace('}',
                                                          '').replace('[', '').replace("]", ""))
    list = re.split("[:,]", newstring)

    return list


def getrepodict(access):
    temp = []
    temp2 = []
    repos = {}

    repo = Display(access)
    r = Display.repo(repo)
    cleaned = cleanup(r)

    for item in range(len(cleaned)):
        if cleaned[item] == "name":
            temp.append(cleaned[item + 1])
    for item in range(len(cleaned)):
        if cleaned[item] == "id":
            temp2.append(cleaned[item + 1])

    for item in range(len(temp)):
        repos[temp[item]] = temp2[item]

    return repos


def getorgdict(access):
    org = {}
    temp = []
    temp2 = []

    orgs = Display(access)
    r = Display.org(orgs)
    cleaned = cleanup(r)

    for item in range(len(cleaned)):
        if cleaned[item] == "name":
            temp.append(cleaned[item + 1])
    for item in range(len(cleaned)):
        if cleaned[item] == "id":
            temp2.append(cleaned[item + 1])

    for item in range(len(temp)):
        org[temp[item]] = temp2[item]

    return org


def getalljobs(access):
    jobs = {}
    temp = []
    temp2 = []
    org = getorgdict(access)

    for key in org:
        job = DisplayJobs(access, org.get(key))
        r = DisplayJobs.jobs(job)
        cleaned = cleanup(r)
        for item in range(len(cleaned)):
            if cleaned[item] == "name":
                temp.append(cleaned[item + 1])
        for item in range(len(cleaned)):
            if cleaned[item] == "id":
                temp2.append(cleaned[item + 1])

        for item in range(len(temp)):
            jobs[temp[item]] = temp2[item]

    return jobs

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
    payload["DailyRetentionPeriod"] = retentionperiod
    payload["RetentionFrequencyType"] = retentionfrequency

    if payload.get("RetentionFrequencyType") == "Daily":
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

    repo = Creation(payload, access)
    r = Creation.repo(repo)

    print(r)


def createorg():
    access = token()
    payload = {}
    exchangeOnlineSettings = {}
    sharePointOnlineSettings = {}

    #    type = input("Type of org (Office365, OnPremises, Hybrid):\t")
    #    region = input("Microsoft Azure region (Worldwide, China):\t")
    isExchangeOnline = input("Add an Exchange Online org (True or False):\t").lower()
    isSharePointOnline = input("Add a SharePoint Online org (True or False):\t").lower()

    payload["type"] = "Office365"
    payload["region"] = "Worldwide"
    payload["isExchangeOnline"] = isExchangeOnline
    payload["isSharePointOnline"] = isSharePointOnline

    if isExchangeOnline == "true":
        accountEO = input("Account:\t")
        passwordEO = input("Password:\t")
        grantAdminAccessEO = input("Give admin access:\t")
        useMFAEO = input("Use MFA:\t")
        customVeeamEO = input("Use custom Veeam AD application:\t")
        exchangeOnlineSettings["account"] = accountEO
        exchangeOnlineSettings["password"] = passwordEO
        exchangeOnlineSettings["grantAdminAccess"] = grantAdminAccessEO
        exchangeOnlineSettings["useMFA"] = useMFAEO
        exchangeOnlineSettings["useCustomVeeamAADApplication"] = customVeeamEO
        payload["ExchangeOnlineSettings"] = exchangeOnlineSettings

    if isSharePointOnline == "true":
        if isExchangeOnline == "true":
            samelogin = input("Use same login details as Exchange Online?\t")
            if samelogin == "True":
                sharePointOnlineSettings["account"] = exchangeOnlineSettings.get("account")
                sharePointOnlineSettings["password"] = exchangeOnlineSettings.get("password")
            else:
                accountSP = input("Account:\t")
                passwordSP = input("Password:\t")
                sharePointOnlineSettings["account"] = accountSP
                sharePointOnlineSettings["password"] = passwordSP

        else:
            accountSP = input("Account:\t")
            passwordSP = input("Password:\t")
            sharePointOnlineSettings["account"] = accountSP
            sharePointOnlineSettings["password"] = passwordSP

        grantAdminAccessSP = input("Give admin access:\t")
        useMFASP = input("Use MFA:\t")
        customVeeamSP = input("Use custom Veeam AD application:\t")
        sharePointOnlineSettings["grantAdminAccess"] = grantAdminAccessSP
        sharePointOnlineSettings["useMFA"] = useMFASP
        sharePointOnlineSettings["useCustomVeeamAADApplication"] = customVeeamSP
        payload["SharePointOnlineSettings"] = sharePointOnlineSettings

    org = Creation(payload, access)
    r = Creation.org(org)

    print(r)

def displayrepos():
    access = token()
    repos = getrepodict(access)

    print(repos)


def displayorgs():
    access = token()
    org = getorgdict(access)

    print(org)


def removerepo():
    access = token()
    repos = getrepodict(access)
    print(repos)

    remove = input("What repo would you like to remove?\t")

    try:
        rem = Removal(access, repos.get(remove))
        r = Removal.repo(rem)

        print(r)
    except ValueError:
        print("Repo Deleted")
    except TypeError:
        print("Repo doesn't exist")


def removeorg():
    access = token()
    org = getorgdict(access)
    print(org)

    remove = input("What org would you like to remove?\t")

    try:
        rem = Removal(access, org.get(remove))
        r = Removal.org(rem)

        print(r)
    except ValueError:
        print("Org Deleted")
    except TypeError:
        print("Org doesn't exist")


def displayorgjobs():
    access = token()
    org = getorgdict(access)
    print(org)

    ans = input("See jobs for what org?\t")
    job = DisplayJobs(access, org.get(ans))
    r = DisplayJobs.jobs(job)

    print(r)


def createjob():
    payload = {}
    schedulepolicy = {}

    access = token()
    proxyid = proxy(access)
    org = getorgdict(access)
    repo = getrepodict(access)

    schedulepolicy["BackupWindowEnabled"] = "False"
    schedulepolicy["Type"] = "Periodically"
    schedulepolicy["PeriodicInterval"] = "Minutes5"
    schedulepolicy["RetryEnabled"] = "True"
    schedulepolicy["RetryNumber"] = "3"
    schedulepolicy["RetryWaitInterval"] = "5"

    print(org)
    orgid = input("Create a job for what org?\t")
    print(repo)
    repoid = input("Backed up to what repository?\t")
    orgid = org.get(orgid)
    name = input("Name:\t")
    description = input("Desciption:\t")

    payload["Name"] = name
    payload["Description"] = description
    payload["BackupType"] = "entireOrganization"
    payload["SchedulePolicy"] = schedulepolicy
    payload["ProxyId"] = proxyid
    payload["RepositoryId"] = repo.get(repoid)
    payload["RunNow"] = "True"

    job = Organization(access, orgid, payload)
    r = Organization.createjob(job)

    print(r)


def displayalljobs():
    access = token()
    jobs = getalljobs(access)

    print(jobs)


def modifyjobsettings():
    payload = {}
    schedulepolicy = {}

    access = token()
    proxyid = proxy(access)
    jobs = getalljobs(access)
    repos = getrepodict(access)
    print(jobs)
    ans = input("Modify what job?\t")
    jobid = jobs.get(ans)

    name = input("Change name to what?\t")
    description = input("New description:\t")
    print(repos)
    repo = input("Backup to what repo:\t")

    schedulepolicy["BackupWindowEnabled"] = "False"
    schedulepolicy["Type"] = "Periodically"
    schedulepolicy["PeriodicallyEvery"] = "Minutes5"
    schedulepolicy["RetryEnabled"] = "True"
    schedulepolicy["RetryNumber"] = "3"
    schedulepolicy["RetryWaitInterval"] = "5"

    payload["Name"] = name
    payload["Description"] = description
    payload["BackupType"] = "entireOrganization"
    payload["SchedulePolicy"] = schedulepolicy
    payload["ProxyId"] = proxyid
    payload["RepositoryId"] = repos.get(repo)
    payload["RunNow"] = "True"

    mod = Organization(access, jobid, payload)
    r = Organization.modifyjob(mod)

    print(r)


def managejobs():
    payload = {}
    access = token()
    jobs = getalljobs(access)
    print(jobs)
    ans = input("Modify what job?\t")
    jobid = jobs.get(ans)

    ans = input("Perform what action?\nenable\nstart\nstop\ndisable\nexplore\n")
    if ans == "explore":
        explorepayload = {"Datetime": "2012-07-20T10:54:40.2794046Z", "type": "vex"}
        payload[ans] = explorepayload

    payload[ans] = "null"

    man = Organization(access, jobid, payload)
    r = Organization.managejob(man)

    print(r)

warnings.filterwarnings("ignore")
welcomeScreen()
