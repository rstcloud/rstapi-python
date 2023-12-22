# Copyright 2023 RST Cloud Pty Ltd

import os
import zlib

import requests


class threatfeed(object):
    def __init__(self, APIKEY="", APIURL="https://api.rstcloud.net/v1"):
        self.APIKEY = os.environ.get("RST_API_KEY", APIKEY)
        self.API_URL = os.environ.get("RST_API_URL", APIURL)

    def GetFeed(
        self, ioctype, filetype="csv", compressed=True, fdate="latest", path=""
    ):
        if not path:
            path = f"threatfeed_{ioctype}_{fdate}.{filetype}"
        apiurl = f"{self.API_URL}/{ioctype}?type={filetype}&date={fdate}"
        headers = {"Accept": "*/*", "X-Api-Key": self.APIKEY}
        r = requests.get(apiurl, headers=headers)
        try:
            if r.status_code == 200:
                if compressed:
                    data = r.content
                    path = path + ".gz"
                else:
                    data = zlib.decompress(r.content, 16 + zlib.MAX_WBITS)
                with open(path, "wb") as f:
                    f.write(data)
                return {"status": "ok", "message": path}
            else:
                return r.json()
        except Exception as ex:
            return {"status": "error", "message": str(ex)}
