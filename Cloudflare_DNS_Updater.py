import json
import os.path
import requests
from utils.ip_utils import *

last_ip_file = "last_ip.txt" #if running as a service or cron job you have to use the full path otherwise it will use the root or /
current_ip = ""
last_ip = ""

if os.path.isfile(last_ip_file):
    with open(last_ip_file) as f:
        last_ip = f.read()
    if isIPV4(last_ip) == False: #So if the file is empty or has an erroneous entry ill just use the current thing
        print("No IP or Invalid IP Recreating file")
        current_ip = getCurrentIP()
        updateLastKnownIP(last_ip_file,current_ip)
else:
    print("No last IP found, creating file")
    current_ip = getCurrentIP()
    updateLastKnownIP(last_ip_file,current_ip)

#load the config for clood flare
with open('config.json') as f:
    config = json.load(f)
cloudflare_config = config['Cloudflare-Config']

def getDNSIdentifier(Cloudflare_Token:str="",zone_id:str="",site_name:str=""):
    try:
        headers = {'Authorization': 'Bearer ' + Cloudflare_Token}
        r = requests.get('https://api.cloudflare.com/client/v4/zones/'+zone_id+'/dns_records', headers=headers)
        if r.status_code != 200:
            print("Error getting DNS identifier: " + str(r.status_code))
            #message body
            #print(r.json())
            return False

        for zone in r.json()['result']:
            if zone['name'] == site_name:
                return zone['id']
        return False
    except Exception as e:
        print("Error getting DNS identifier: " + str(e))
        return False
def setNewDNSIP(Cloudflare_Token:str="",zone_id:str="",site_identifier:str="",sitename:str="",dns_record_data:dict={}):
    try:
        headers = {'Authorization': 'Bearer ' + Cloudflare_Token}
        data = dns_record_data
        r = requests.put('https://api.cloudflare.com/client/v4/zones/'+zone_id+'/dns_records/'+site_identifier, headers=headers,data=data)
        if r.status_code != 200:
            print("Error setting new DNS IP: " + str(r.status_code))
            #message body
            #print(r.json())
            return False
        return True
    except Exception as e:
        print("Error setting new DNS IP: " + str(e))
        return False

#if last_ip != getCurrentIP():
   # print("IP has changed, updating DNS......")
    #https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-update-dns-record

    #update the DNS
    #https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record
    #curl -X PUT "https://api.cloudflare.com/client/v4/zones/023e105f4ecef8ad9ca31a8372d0c353/dns_records/372e67954025e0ba6aaa6d586b9e0b59" \
    #-H "X-Auth-Email:


print(getDNSIdentifier(cloudflare_config['API_TOKEN'],cloudflare_config['ZONE_ID'],"ipchange.zerosystems.org"))



