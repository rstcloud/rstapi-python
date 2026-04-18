# Copyright 2024 RST Cloud Pty Ltd

import os
import zlib
from urllib.parse import quote, urlencode

from .api import _env_int, _env_verify, _make_request, _response_or_json


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
        self.CONNECT = _env_int("RST_CONNECT_TIMEOUT", CONNECT)
        self.READ = _env_int("RST_READ_TIMEOUT", READ)
        self.VERIFY = _env_verify("RST_SSL_VERIFY", VERIFY)
        self.MAX_RETRIES = _env_int("RST_MAX_RETRIES", MAX_RETRIES)

    def GetFeed(
        self, ioctype, filetype="csv", compressed=True, fdate="latest", path=""
    ):
        if not path:
            path = f"threatfeed_{ioctype}_{fdate}.{filetype}"
        query = urlencode({"type": filetype, "date": fdate})
        apiurl = f"{self.API_URL}/{quote(str(ioctype), safe='')}?{query}"
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
            if r.status_code == 200:
                if compressed:
                    data = r.content
                    path = path + ".gz"
                else:
                    data = zlib.decompress(r.content, 16 + zlib.MAX_WBITS)
                with open(path, "wb") as f:
                    f.write(data)
                return {"status": "ok", "message": path}
            return _response_or_json(r)
        except (OSError, zlib.error) as ex:
            return {"status": "error", "message": str(ex)}
