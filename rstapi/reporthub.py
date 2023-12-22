# Copyright 2023 RST Cloud Pty Ltd

import os

import requests


class reporthub(object):
    def __init__(self, APIKEY="", APIURL="https://api.rstcloud.net/v1"):
        self.APIKEY = os.environ.get("RST_API_KEY", APIKEY)
        self.API_URL = os.environ.get("RST_API_URL", APIURL)

    def GetReports(self, startdate):
        endpoint = f"/reports?date={startdate}"
        apiurl = self.API_URL + endpoint
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = requests.get(apiurl, headers=headers)
        return r.json()

    def GetReportJSON(self, reportid, lang="eng"):
        endpoint = f"/reports/?id={reportid}&lang={lang}&format=json"
        apiurl = self.API_URL + endpoint
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = requests.get(apiurl, headers=headers)
        return r.json()

    def GetReportSTIX(self, reportid, lang="eng"):
        endpoint = f"/reports/?id={reportid}&lang={lang}&format=stix"
        apiurl = self.API_URL + endpoint
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = requests.get(apiurl, headers=headers)
        return r.json()

    def GetReportPDF(self, reportid, path=""):
        if not path:
            path = f"{reportid}.pdf"
        endpoint = f"/reports/?id={reportid}&format=pdf"
        apiurl = self.API_URL + endpoint
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = requests.get(apiurl, headers=headers)
        try:
            with open(path, "wb") as f:
                f.write(r.content)
            return {"status": "ok", "message": path}
        except Exception as ex:
            return {"status": "error", "message": str(ex)}
