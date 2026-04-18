# Copyright 2024 RST Cloud Pty Ltd

import os
from urllib.parse import quote

from .api import _env_int, _env_verify, _make_request, _response_or_json


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
        self.API_URL = os.environ.get("RST_API_URL", APIURL)
        self.CONNECT = _env_int("RST_CONNECT_TIMEOUT", CONNECT)
        self.READ = _env_int("RST_READ_TIMEOUT", READ)
        self.VERIFY = _env_verify("RST_SSL_VERIFY", VERIFY)
        self.MAX_RETRIES = _env_int("RST_MAX_RETRIES", MAX_RETRIES)

    def ValueLookup(self, value):
        endpoint = "/benign/lookup"
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

    def BatchLookup(self, ioctype, data):
        endpoint = f"/benign/batch/{ioctype}"
        apiurl = self.API_URL + endpoint
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
        return _response_or_json(r)

    def BatchResult(self, ioctype, token, attempts=5, timeout=1, retry=True):
        endpoint = f"/benign/result/{ioctype}"
        apiurl = self.API_URL + endpoint
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        max_retries = attempts if retry else 1
        r = _make_request(
            self,
            "POST",
            apiurl,
            headers,
            token,
            self.CONNECT,
            self.READ,
            self.VERIFY,
            max_retries,
            retrycode=301,
            timeout=timeout,
            retry_on_status_match=retry,
        )
        return _response_or_json(r)
