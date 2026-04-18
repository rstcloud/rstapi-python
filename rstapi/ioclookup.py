# Copyright 2024 RST Cloud Pty Ltd

import os
from urllib.parse import quote

from .api import _env_int, _env_verify, _make_request, _response_or_json


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
        self.CONNECT = _env_int("RST_CONNECT_TIMEOUT", CONNECT)
        self.READ = _env_int("RST_READ_TIMEOUT", READ)
        self.VERIFY = _env_verify("RST_SSL_VERIFY", VERIFY)
        self.MAX_RETRIES = _env_int("RST_MAX_RETRIES", MAX_RETRIES)

    def GetIndicator(self, value):
        endpoint = "/ioc"
        apiurl = self.API_URL + endpoint + "?value=" + quote(value, safe="")
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
        return _response_or_json(r)

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
        return _response_or_json(r)

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
        return _response_or_json(r)
