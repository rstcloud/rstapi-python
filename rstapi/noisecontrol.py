# Copyright 2023 RST Cloud Pty Ltd

import os
import time

import requests


class noisecontrol(object):
    def __init__(self, APIKEY="", APIURL="https://api.rstcloud.net/v1"):
        self.APIKEY = os.environ.get("RST_API_KEY", APIKEY)
        self.API_URL = os.environ.get("RST_API_URL", APIURL)

    def ValueLookup(self, value):
        endpoint = "/benign/lookup"
        apiurl = self.API_URL + endpoint + "?value=" + value
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = requests.get(apiurl, headers=headers)
        return r.json()

    def BatchLookup(self, ioctype, data):
        endpoint = f"/benign/batch/{ioctype}"
        apiurl = self.API_URL + endpoint
        payload = data
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = requests.post(apiurl, data=payload, headers=headers)
        return r.json()

    def BatchResult(self, ioctype, token, attempts=5, timeout=1):
        endpoint = f"/benign/result/{ioctype}"
        apiurl = self.API_URL + endpoint
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        n = 0
        while n < attempts:
            r = requests.post(apiurl, json=token, headers=headers)
            if r.status_code == 200:
                # got the results
                return r.json()
            elif r.status_code == 301:
                # retry later
                time.sleep(timeout)
                n += 1
            else:
                # error
                return r.json()
        return {"status": "error", "message": "Timed out"}
