# Copyright 2024 RST Cloud Pty Ltd

import os
from urllib.parse import urlencode

from .api import _env_int, _env_verify, _make_request, _response_or_json


class reporthub(object):
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

    def GetReports(self, startdate):
        endpoint = "/reports?" + urlencode({"date": startdate})
        apiurl = self.API_URL + endpoint
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

    def GetReportJSON(self, reportid, lang="eng"):
        endpoint = "/reports/?" + urlencode(
            {"id": reportid, "lang": lang, "format": "json"}
        )
        apiurl = self.API_URL + endpoint
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

    def GetReportSTIX(self, reportid, lang="eng"):
        endpoint = "/reports/?" + urlencode(
            {"id": reportid, "lang": lang, "format": "stix"}
        )
        apiurl = self.API_URL + endpoint
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

    def GetReportPDF(self, reportid, path=""):
        if not path:
            path = f"{reportid}.pdf"
        endpoint = "/reports/?" + urlencode({"id": reportid, "format": "pdf"})
        apiurl = self.API_URL + endpoint
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
        if isinstance(r, dict):
            return r
        try:
            with open(path, "wb") as f:
                f.write(r.content)
            return {"status": "ok", "message": path}
        except OSError as ex:
            return {"status": "error", "message": str(ex)}
