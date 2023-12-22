import os
from datetime import date, timedelta
from pprint import pprint

from rstapi import ioclookup, noisecontrol, reporthub, threatfeed, whoisapi

USER_APIKEY = "REPLACE_ME"

# # # # # # # # # # # # # #
# --- RST Threat Feed --- #
# # # # # # # # # # # # # #

print("\n--- RST Threat Feed ---\n")
# args: APIKEY,APIURL
rst_threatfeed = threatfeed(APIKEY=USER_APIKEY)

# args: ioctype, filetype="csv|json", compressed=True|False,
# fdate="latest|yyyymmdd", path="path_to_your_output_file"
file = rst_threatfeed.GetFeed(ioctype="hash", filetype="csv")
pprint(file)
if "status" in file and file["status"] == "ok":
    os.remove(file["message"])

# # # # # # # # # # # # # #
# --- RST IoC Lookup ---  #
# # # # # # # # # # # # # #

print("\n--- RST IoC Lookup ---\n")

# args: APIKEY,APIURL
rst_ioclookup = ioclookup(APIKEY=USER_APIKEY)

# args: ioc_value
pprint(rst_ioclookup.GetIndicator("7eb800559bfa2c1980b0cc711cec120b"))

# args: ioc_value, description
pprint(rst_ioclookup.SubmitIndicator("1.1.1.1", "detected by sandbox"))
pprint(rst_ioclookup.SubmitFalsePositive("1.1.1.1", "cdn address"))

# # # # # # # # # # # # # #
# --- RST Noise Control ---  #
# # # # # # # # # # # # # #

print("\n--- RST Noise Control ---\n")

# args: APIKEY,APIURL
rst_noisecontrol = noisecontrol(APIKEY=USER_APIKEY)

# args: ioc_value
pprint(rst_noisecontrol.ValueLookup("1.1.1.1"))

# args: ioc_type, list of entries
data = "google.com\nmicrosoft.com\ntest.com"
ioc_type = "domain"
token = rst_noisecontrol.BatchLookup(ioctype=ioc_type, data=data)
pprint(token)

# args: ioctype, token, attempts=5, timeout=1
result = rst_noisecontrol.BatchResult(ioctype=ioc_type, token=token)
pprint(result)

# # # # # # # # # # # # # #
# --- RST Report Hub ---  #
# # # # # # # # # # # # # #

# args: APIKEY,APIURL
print("\n--- RST Report Hub ---\n")

# args: APIKEY,APIURL
rst_reporthub = reporthub(APIKEY=USER_APIKEY)

# args: a string date in format yyyymmdd
startDate = (date.today() - timedelta(days=1)).strftime("%Y%m%d")
report_digest = rst_reporthub.GetReports(startDate)
print(len(report_digest))


if len(report_digest) > 0:
    # args: ID of a report, path to the output file
    report_pdf = rst_reporthub.GetReportPDF(reportid=report_digest[0]["id"])
    print(report_pdf)
    os.remove(report_pdf["message"])

    # args: ID of a report, lang=eng
    report_json = rst_reporthub.GetReportJSON(reportid=report_digest[0]["id"])
    print(report_json["id"])
    # 20231220_malwarebytes_com_report_0x7ea0f65

    # args: ID of a report, lang=eng
    report_stix = rst_reporthub.GetReportSTIX(reportid=report_digest[0]["id"])
    print(report_stix["id"])
    # bundle--f462f3db-52f7-417c-9527-089381ba4d69

# # # # # # # # # # # # # #
# --- RST Whois API ---   #
# # # # # # # # # # # # # #

# args: APIKEY,APIURL
print("\n--- RST Whois API ---\n")
rst_whois = whoisapi(APIKEY=USER_APIKEY)

# args: any domain name, raw=True|False
pprint(rst_whois.GetDomainInfo(domain="domain.com", raw=False))
