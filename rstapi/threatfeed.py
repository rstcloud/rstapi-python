# Copyright 2024 RST Cloud Pty Ltd

import os
import zlib
from .api import _make_request


class threatfeed(object):
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

    def GetFeed(
        self, ioctype, filetype="csv", compressed=True, fdate="latest", path=""
    ):
        if not path:
            path = f"threatfeed_{ioctype}_{fdate}.{filetype}"
        apiurl = f"{self.API_URL}/{ioctype}?type={filetype}&date={fdate}"
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
