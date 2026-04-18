# Copyright 2024 RST Cloud Pty Ltd

import os

from .api import _env_int, _env_verify, _make_request, _response_or_json


class connectivity(object):
    """
    RST Cloud connectivity and API key validation.

    ``GET /auth/check`` returns key validity plus **quota** stats (``used``, ``limit``,
    ``remaining``, ``period``) so callers can read how many requests remain in the current window.
    """

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

    def CheckApiKey(self):
        """
        GET /auth/check — validate the API key and return quota usage.

        On success the JSON body includes ``check`` (e.g. ``status: valid``) and ``quota``
        with ``used``, ``limit``, ``remaining``, and ``period`` (e.g. ``DAY``).
        """
        apiurl = self.API_URL + "/auth/check"
        headers = {"Accept": "application/json", "X-Api-Key": self.APIKEY}
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
