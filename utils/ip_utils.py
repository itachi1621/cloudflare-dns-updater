import requests
import re


def isIPV4(ip:str=""):
    try:
        return bool(re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ip))
    except Exception as e:
        print("Error checking if IP is IPV4: " + str(e))
        return False

def getCurrentIP():
    try:
        r = requests.get('https://api.ipify.org?format=json')
        if r.status_code != 200:
            print("Error getting current IP: " + str(r.status_code))
            return False

        return r.json()['ip']
    except Exception as e:
        print("Error getting current IP: " + str(e))
        return False

def getLastKnownIP():
    try:
        with open('last_ip.txt', 'r') as f:
            return f.read()
    except Exception as e:
        print("Error getting last known IP: " + str(e))
        return False


def updateLastKnownIP(filePath:str="",ip:str=""):
    try:
        with open(filePath, 'w') as f:
            f.write(ip)
        return True
    except Exception as e:
        print("Error updating last known IP: " + str(e))
        return False

