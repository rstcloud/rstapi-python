# Copyright 2023 RST Cloud Pty Ltd

import os

import requests


class whoisapi(object):
    def __init__(self, APIKEY="", APIURL="https://api.rstcloud.net/v1"):
        self.APIKEY = os.environ.get("RST_API_KEY", APIKEY)
        self.API_URL = os.environ.get("RST_API_URL", APIURL)

    def GetDomainInfo(self, domain, raw=False):
        endpoint = "/whois/"
        if raw:
            endpoint = "/whois/raw/"
        apiurl = self.API_URL + endpoint + domain
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = requests.get(apiurl, headers=headers)
        return r.json()
