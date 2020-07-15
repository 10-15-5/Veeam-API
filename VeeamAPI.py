from API import *
import warnings


def welcomeScreen():
    print("Welcome to the Veeam API requests program what would you like to do?")
    print("1) Create a Repo\n2) Display Repos\n3) Display Orgs\n4) Create Organization\n5) Remove Repo")
    ans = input()

    if ans == "1":
        createarepo()
    elif ans == "2":
        displayrepos()
    elif ans == "3":
        displayorgs()
    elif ans == "4":
        createorg()
    elif ans == "5":
        removeRepo()


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
                                                                                                  '').replace('[',
                                                                                                              '').replace(
        "]", ""))
    list = re.split("[:,]", newstring)

    return list


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

    repo = CreateRepo(payload, access)
    r = CreateRepo.create(repo)

    print(r)


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


def displayorgs():
    access = token()

    repo = DisplayRepo(access)
    r = DisplayRepo.displayRepos(repo)
    cleaned = cleanup(r)

    repoid = []
    for item in range(len(cleaned)):
        if cleaned[item] == "id":
            repoid.append(cleaned[item + 1])

    orgs = []
    for item in range(len(repoid)):
        org = GetOrgs(access, repoid[item])
        r = GetOrgs.orgs(org)

        cleaned = cleanup(r)
        if len(cleaned) > 1:
            orgs.append(cleaned[1])

    print(orgs)


def createorg():
    access = Token()
    payload = {}
    excahngeOnlineSettings = {}
    sharePointOnlineSettings = {}

    type = input("Type of org (Office365, OnPremises, Hybrid):\t")
    region = input("Microsoft Azure region (Worldwide, China):\t")
    isExchangeOnline = input("Add an Exchange Online org (True or False):\t").lower()
    isSharePointOnline = input("Add a SharePoint Online org (True or False):\t").lower()

    payload["type"] = type
    payload["region"] = region
    payload["isExchangeOnline"] = isExchangeOnline
    payload["isSharePointOnline"] = isSharePointOnline

    if isExchangeOnline == "true":
        accountEO = input("Account:\t")
        passwordEO = input("Password:\t")
        grantAdminAccessEO = input("Give admin access:\t")
        useMFAEO = input("Use MFA:\t")
        customVeeamEO = input("Use custom Veeam AD application:\t")
        excahngeOnlineSettings["account"] = accountEO
        excahngeOnlineSettings["password"] = passwordEO
        excahngeOnlineSettings["grantAdminAccess"] = grantAdminAccessEO
        excahngeOnlineSettings["useMFA"] = useMFAEO
        excahngeOnlineSettings["useCustomVeeamAADApplication"] = customVeeamEO
        payload["ExchangeOnlineSettings"] = excahngeOnlineSettings

    if isSharePointOnline == "true":
        accountSP = input("Account:\t")
        passwordSP = input("Password:\t")
        grantAdminAccessSP = input("Give admin access:\t")
        useMFASP = input("Use MFA:\t")
        customVeeamSP = input("Use custom Veeam AD application:\t")
        sharePointOnlineSettings["account"] = accountSP
        sharePointOnlineSettings["password"] = passwordSP
        sharePointOnlineSettings["grantAdminAccess"] = grantAdminAccessSP
        sharePointOnlineSettings["useMFA"] = useMFASP
        sharePointOnlineSettings["useCustomVeeamAADApplication"] = customVeeamSP
        payload["SharePointOnlineSettings"] = sharePointOnlineSettings

    org = CreateOrg(payload, access)
    r = CreateOrg.create(org)

    print(r)


def removeRepo():
    access = token()

    repo = DisplayRepo(access)
    r = DisplayRepo.displayRepos(repo)
    cleaned = cleanup(r)

    repos = {}
    temp = []
    temp2 = []
    for item in range(len(cleaned)):
        if cleaned[item] == "name":
            temp.append(cleaned[item + 1])
    for item in range(len(cleaned)):
        if cleaned[item] == "id":
            temp2.append(cleaned[item + 1])

    for item in range(len(temp)):
        repos[temp[item]] = temp2[item]

    print(repos)

    remove = input("What repo would you like to remove?\t")

    rem = RemoveRepo(access, repos.get(remove))
    r = RemoveRepo.remove(rem)

    print(r)


warnings.filterwarnings("ignore")
welcomeScreen()
