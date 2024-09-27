# Copyright 2024 RST Cloud Pty Ltd

import os
from .api import _make_request


class noisecontrol(object):
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
        self.APIURL = os.environ.get("RST_API_URL", APIURL)
        self.CONNECT = os.environ.get("RST_CONNECT_TIMEOUT", CONNECT)
        self.READ = os.environ.get("RST_READ_TIMEOUT", READ)
        self.VERIFY = os.environ.get("RST_SSL_VERIFY", VERIFY)
        self.MAX_RETRIES = os.environ.get("RST_MAX_RETRIES", MAX_RETRIES)

    def ValueLookup(self, value):
        endpoint = "/benign/lookup"
        apiurl = self.APIURL + endpoint + "?value=" + value
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

    def BatchLookup(self, ioctype, data):
        endpoint = f"/benign/batch/{ioctype}"
        apiurl = self.APIURL + endpoint
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = _make_request(
            self,
            "POST",
            apiurl,
            headers,
            data,
            self.CONNECT,
            self.READ,
            self.VERIFY,
            self.MAX_RETRIES,
        )
        if "message" in r:
            return r
        else:
            return r.json()

    def BatchResult(self, ioctype, token, attempts=5, timeout=1, retry=True):
        endpoint = f"/benign/result/{ioctype}"
        apiurl = self.APIURL + endpoint
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = _make_request(
            self,
            "POST",
            apiurl,
            headers,
            token,
            self.CONNECT,
            self.READ,
            self.VERIFY,
            attempts,
            retrycode=301,
        )
        if "message" in r:
            return r
        else:
            return r.json()
