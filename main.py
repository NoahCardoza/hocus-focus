import os

INIT_MARKER = """
##> Focus
##< Focus
"""

REDIRECT_ADDR = '0.0.0.0'

def refreshDNS():
    os.system("sudo killall -HUP mDNSResponder")
    os.system("dscacheutil -flushcache")

def getTrackedRange(lines):
    return (lines.index("##> Focus\n") + 1, lines.index("##< Focus\n"))

def insureFocusInit(file):
    if "##> Focus\n" not in file.readlines():
        file.write(INIT_MARKER)
    file.seek(0)

def updateTrackedHostes(updatedHosts):
    # add newlines to the end of the ips for the hosts file
    # REDIRECT_ADDR + ' ' +
    updatedHosts = [(h + ('\n' if h and h[-1] != '\n' else '')) for h in updatedHosts]

    with open('/etc/hosts', 'r+') as file:
        insureFocusInit(file)
        hosts = file.readlines()
        focusRange = getTrackedRange(hosts)
        del hosts[slice(*focusRange)]
        for h in updatedHosts:
            hosts.insert(focusRange[0], h)
        file.seek(0)
        file.write("".join(hosts))
        file.truncate()
        file.close()


def fetchTrackedHosts():
    tracked = []
    with open('/etc/hosts', 'r+') as file:
        insureFocusInit(file)
        hosts = file.readlines()
        tracked = hosts[slice(*getTrackedRange(hosts))]
    return tracked

# print(fetchTrackedHosts())

# updateTrackedHostes(['google.com', 'gmail.com', 'mail.google.com'])
updateTrackedHostes([])
# updateTrackedHostes(ips.splitlines())
# refreshDNS()
