import requests


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
