# Cloudflare DNS Updater

![Cloudflare Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Cloudflare_Logo.svg/512px-Cloudflare_Logo.svg.png)

## Overview

This Python script updates Cloudflare DNS records based on changes in the public IP address of your network. It is designed to be used in either **service or cron mode**. The script retrieves the current public IP address, compares it with the last known IP address stored in a file, and updates Cloudflare DNS records if there is a change.

## Prerequisites

- Python 3.x
- `requests` library (install using `pip install requests`)
	- Alternatively use `pip install -r requirements.txt` to install all packages needed

## Configuration

Before running the script, you need to configure it by providing the necessary information in the `config.json` file a sample file called `sample_config.json` is provided

### `config.json`

```json
{
  "Application-Config": {
    "MODE": "Service",  # Options: "Service" or "Cron"
    "SERVICE-INTERVAL": 300  # Interval in seconds for checking IP changes (applicable in service mode)
  },
  "Cloudflare-Config": [
    {
      "API_TOKEN": "YOUR_CLOUDFLARE_API_TOKEN",
      "ZONE_ID": "YOUR_CLOUDFLARE_ZONE_ID",
      "SITE": "example.com",  # Your domain
      "RECORD_TYPE": "A",  # DNS record type (A, AAAA, CNAME, TXT, SRV, LOC, MX, NS, SPF)
      "TTL": 1,  # Time to live for the DNS record (1 = auto)
      "PROXIED": false  # Proxy through Cloudflare (true or false)
    }
    // Add more Cloudflare configurations as needed
  ]
}

```

## Usage
### Service Mode
  - If running in service mode, the script will continuously monitor IP changes and update Cloudflare DNS records accordingly.
  

### Cron Mode
  - If running in cron mode, the script will update Cloudflare DNS records only when there is a change in the public IP address. 

### Running once configured
```
python cloudflare_dns_updater.py
```


## Get Cloudflare API Token and Zone ID

**1). Cloudflare API Token:** 

- Go to Cloudflare Dashboard.
- Navigate to "Profile" and select "API Tokens."
- Click on "Create Token" and choose the "Edit zone DNS" template.
- Assign the token a name, and make sure it has the necessary permissions.
- Copy the generated API token.
-  Link
   ```
   https://dash.cloudflare.com/profile/api-tokens
    ```

**2.) Zone ID:**

- Go to Cloudflare Dashboard.
- Select the domain for which you want to update DNS records.
- The Zone ID can be found on the right side of the Overview page under the "Zone Information" section.

## Logging
Logs are written to the **ipchange.log** file in the specified basePath.

## Important Note
This script currently supports only IPV4 addresses. If you have IPV6, you'll need to modify the code to support it.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

