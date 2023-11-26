import json
import os.path
import logging
import time
from utils.ip_utils import *
from utils.cloudflare_handler import *

#Note this program only works with IPV4 addresses which is most of the internet
#If you have IPV6 you will have to modify the code to support it im not going to do that :P
basePath = "" #Define the full path to the directory where you want the files to be stored
last_ip_file = basePath+"last_ip.txt" #if running as a service or cron job you have to use the full path otherwise it will use the root or /
config_file = basePath+"config.json" #Full path again beat that dead horse
current_ip = ""
last_ip = ""
logfile = basePath+"ipchange.log" #Again this needs to be the full path if running as a service or cron job
logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(levelname)-8s %(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

with open(config_file) as f:
    config = json.load(f)

application_config = config['Application-Config']
app_mode = application_config['MODE'] #Service or Cron
if app_mode == "Service":
    logging.info("Running in service mode")
    service_interval = application_config['SERVICE-INTERVAL'] #How often to check for IP changes in seconds
elif app_mode == "Cron":
    logging.info("Running in cron mode")
else:
    logging.error("Invalid Mode")
    exit()

def getLastIP(last_ip_file:str="last_ip.txt"):
    ip=""
    if os.path.isfile(last_ip_file):
        with open(last_ip_file) as f:
            ip = f.read()
        if isIPV4(ip) == False: #So if the file is empty or has an erroneous entry ill just use the current thing
            logging.info("IP file has invalid IP creating one")
            ip = getCurrentIP()
            updateLastKnownIP(last_ip_file,ip)
        else:
            current_ip = getCurrentIP()
    else:
        logging.info("No IP file found creating one")
        ip = getCurrentIP()
        updateLastKnownIP(last_ip_file,ip)
    return ip

def updateDNSRecord(ip:str=""):
    try:
        #load the config for clood flare
        with open(config_file) as f:
            config = json.load(f)
        cloudflare_config = config['Cloudflare-Config']

        dns_site_identifier = getDNSIdentifier(cloudflare_config['API_TOKEN'],cloudflare_config['ZONE_ID'],cloudflare_config['SITE'])
        print("IP has changed, updating DNS")
        record_data = {
                        "type":cloudflare_config['RECORD_TYPE'], #A, AAAA, CNAME, TXT, SRV, LOC, MX, NS, SPF
                        "name":cloudflare_config['SITE'],
                        "content":ip,
                        "ttl":cloudflare_config['TTL'],#Time to live 1 = auto
                        "proxied":cloudflare_config['PROXIED']#Proxy through cloudflare
                        }

        if setNewDNSIP(cloudflare_config['API_TOKEN'],cloudflare_config['ZONE_ID'],dns_site_identifier,record_data):
            logging.info("DNS Updated")
            updateLastKnownIP(last_ip_file,ip)
        else:
            logging.error("DNS Update Failed")
        updateLastKnownIP(last_ip_file,current_ip)
    except Exception as e:
        logging.error("Error Updating DNS: " + str(e))



last_ip=getLastIP(last_ip_file)
current_ip = getCurrentIP()

logging.info("Current IP: " + current_ip)
logging.info("Last IP: " + last_ip)

if app_mode == "Service":
    while True:
        current_ip = getCurrentIP()
        if str(current_ip) != str(last_ip):
            updateDNSRecord(current_ip)
            last_ip = current_ip
        time.sleep(service_interval)
elif app_mode == "Cron":
    if str(current_ip) != str(last_ip):
        updateDNSRecord(current_ip)
else:
    logging.error("Invalid Mode")


logging.info("Exiting....")



