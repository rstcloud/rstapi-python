# Copyright 2024 RST Cloud Pty Ltd

import os
from .api import _make_request


class whoisapi(object):
    def __init__(
        self,
        APIKEY="",
        APIURL="https://api.rstcloud.net/v1",
        CONNECT=10,
        READ=20,
        VERIFY=True,
        MAX_RETRIES=1,
    ):
        self.APIKEY = os.environ.get("RST_API_KEY", APIKEY)
        self.API_URL = os.environ.get("RST_API_URL", APIURL)
        self.CONNECT = os.environ.get("RST_CONNECT_TIMEOUT", CONNECT)
        self.READ = os.environ.get("RST_READ_TIMEOUT", READ)
        self.VERIFY = os.environ.get("RST_SSL_VERIFY", VERIFY)
        self.MAX_RETRIES = os.environ.get("RST_MAX_RETRIES", MAX_RETRIES)

    def GetDomainInfo(self, domain, raw=False):
        endpoint = "/whois/"
        if raw:
            endpoint = "/whois/raw/"
        apiurl = self.API_URL + endpoint + domain
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = _make_request(
            self,
            "GET",
            apiurl,
            headers,
            None,
            self.CONNECT,
            self.READ,
            self.VERIFY,
            self.MAX_RETRIES,
        )
        if "message" in r:
            return r
        else:
            return r.json()
