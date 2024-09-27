# Copyright 2024 RST Cloud Pty Ltd

import os
from .api import _make_request


class ioclookup(object):
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

    def GetIndicator(self, value):
        endpoint = "/ioc"
        apiurl = self.API_URL + endpoint + "?value=" + value
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

    def SubmitIndicator(self, value, desc="manual submission"):
        endpoint = "/ioc"
        apiurl = self.API_URL + endpoint
        payload = {"ioc_value": value, "description": desc}
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = _make_request(
            self,
            "POST",
            apiurl,
            headers,
            payload,
            self.CONNECT,
            self.READ,
            self.VERIFY,
            self.MAX_RETRIES,
        )
        if "message" in r:
            return r
        else:
            return r.json()

    def SubmitFalsePositive(self, value, desc="manual submission"):
        endpoint = "/ioc"
        payload = {"ioc_value": value, "description": desc}
        apiurl = self.API_URL + endpoint
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = _make_request(
            self,
            "PUT",
            apiurl,
            headers,
            payload,
            self.CONNECT,
            self.READ,
            self.VERIFY,
            self.MAX_RETRIES,
        )
        if "message" in r:
            return r
        else:
            return r.json()
