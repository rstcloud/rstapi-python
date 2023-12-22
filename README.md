# rstapi-python

Python 3 library for using the various threat intelligence RST Cloud APIs:
 - RST Threat Feed
 - RST Report Hub
 - RST Noise Control
 - RST IoC Lookup
 - RST Whois API

## Installation

To install with pip run `pip install rstapi`

## Usage

See GitHub source https://github.com/rstcloud/rstapi-python
for further details and example usage. The file `test.py` includes examples.

See RST Cloud API docs here: https://www.rstcloud.com/api-docs/

An API token is required to use the RST Cloud API. You can request a RST Cloud API token by contacting trial@rstcloud.net, generating it online https://www.rstcloud.com/#free-trial, or reaching out your account representative.


The better way is to setup an environment variable RST_API_KEY and call it without specifing the key in the code.

```
import rstapi
c = rstapi.ioclookup()
c.GetIndicator("1.1.1.1")
```

However, you can explicitly pass a token in the api client constructor:

```
import rstapi
c = rstapi.ioclookup(APIKEY="YOU_API_KEY")
c.GetIndicator("1.1.1.1")
```


## Products

### RST Threat Feed

A comprehensive threat intel feed of indicators (IP, Domain, URL, Hash) with their relationships to malware, TTPs, tools, threat groups, sectors, CVE, and other objects.

Compiled from over 260 sources, including Twitter, Telegram, online sandboxes (Any.Run, Hybrid Analysis, VMRay, etc.), threat reports, CERTs, malware research sites, GitHub, pastebin, closed sources and our global RST Honeypot network.

Read more: https://www.rstcloud.com/rst-threat-feed/

### RST Report Hub

An electronic library of threat reports from hundreds of security companies, individual researchers and cyber communities.

These reports undergo transformation from human-readable formats to machine-readable ones, including STIX 2.1. Extensive multilingual translation, archiving as PDFs, and summarization are conducted. Key data, encompassing threat actors, names, software, CVEs, geolocation, industry, etc., is automatically extracted, with due credit to the original report author.

Read more: https://www.rstcloud.com/rst-report-hub/

### RST Noise Control

A service that can be used with TIP, SOAR, or SIEM solutions to minimise the noise coming from False Positive indicators. Make sure that CDN IPs, known domains, common URLs, or hashes of calc.exe don’t trigger alerts.

This API employs over 110 rulesets and incorporates 12 GB of individual exceptions, to check if indicators are “known-good” and to be considered noise.

Read more: https://www.rstcloud.com/rst-noise-control/

### RST IoC Lookup

An API to check individual values if they are a suspicious or malicious indicator (IP, Domain, URL, Hash). Offering dynamic scoring and automatic decay of outdated indicators, the service ensures fair request rate with low cost.

Ideal for real-time checks in SOAR or be integration into custom applications for online user connection scrutiny.

Read more: https://www.rstcloud.com/rst-ioc-lookup/

### RST Whois API

A service to get actual registration info in JSON format for a given domain without limitations on speed and no ban from WHOIS servers. The results include whenever possible:

- Data in a unified JSON format
- Registrar and registrant info
- Age of the domain
- Dates (registered, updated, expires)
- Raw response from WHOIS servers

Read more: https://www.rstcloud.com/rst-whois-api/
