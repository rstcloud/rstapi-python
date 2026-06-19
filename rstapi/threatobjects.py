# Copyright 2024 RST Cloud Pty Ltd

import os
from urllib.parse import quote, urlencode

from .api import _env_int, _env_verify, _make_request, _response_or_json

# Threat object types served by GET /threat-objects/{object_type}.
OBJECT_TYPES = ("intrusion-sets", "malware", "tools", "campaigns")


class threatobjects(object):
    """RST Threat Library access (``GET /threat-objects/{object_type}``).

    Returns threat object definitions — ``intrusion-sets``, ``malware``,
    ``tools`` and ``campaigns`` — with optional pagination, filtering and
    sorting. These are the building blocks for MISP galaxies / OpenCTI
    knowledge objects.

    Constructor and environment variables match the other clients
    (``APIKEY``, ``APIURL``, ``RST_API_KEY``, timeouts, ``RST_SSL_VERIFY``).
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

    def GetThreatObjects(
        self,
        object_type,
        limit=None,
        offset=None,
        id=None,
        name=None,
        filter=None,
        orderBy=None,
        orderMode=None,
    ):
        """One request to ``/threat-objects/{object_type}``.

        Any of ``limit``/``offset`` (pagination), ``id``/``name`` (single
        lookup), ``filter`` (search expression), ``orderBy``
        (``created_at``/``modified``/``updated_at``) and ``orderMode``
        (``asc``/``desc``) may be supplied. Returns the parsed JSON, or an
        error dict ``{"status": "error", "message": ...}``.
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if id is not None:
            params["id"] = id
        if name is not None:
            params["name"] = name
        if filter is not None:
            params["filter"] = filter
        if orderBy is not None:
            params["orderBy"] = orderBy
        if orderMode is not None:
            params["orderMode"] = orderMode

        apiurl = f"{self.API_URL}/threat-objects/{quote(str(object_type), safe='')}"
        if params:
            apiurl = apiurl + "?" + urlencode(params)
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

    def GetThreatObjectById(self, object_type, id):
        """Fetch a single object by its id."""
        return self.GetThreatObjects(object_type, id=id)

    def GetThreatObjectByName(self, object_type, name):
        """Fetch a single object by its name."""
        return self.GetThreatObjects(object_type, name=name)

    def IterThreatObjects(
        self,
        object_type,
        page_size=100,
        filter=None,
        orderBy=None,
        orderMode=None,
    ):
        """Generator that paginates through every object of ``object_type``.

        Yields objects one at a time so large libraries stay memory-friendly.
        Raises ``RuntimeError`` if a page returns an API error, so callers do
        not silently truncate the result set.
        """
        offset = 0
        while True:
            page = self.GetThreatObjects(
                object_type,
                limit=page_size,
                offset=offset,
                filter=filter,
                orderBy=orderBy,
                orderMode=orderMode,
            )
            if isinstance(page, dict) and page.get("status") == "error":
                raise RuntimeError(
                    "threat-objects error at offset %s: %s"
                    % (offset, page.get("message"))
                )
            data, total = self._page_items(page)
            if not data:
                break
            for obj in data:
                yield obj
            offset += len(data)
            if total is not None and offset >= total:
                break
            if len(data) < page_size:
                break

    @staticmethod
    def _page_items(page):
        """Normalise a page response into ``(items, total_or_None)``.

        Tolerates a bare list, ``{"data": [...], "total": N}``, or an
        ``{"objects": [...]}`` envelope.
        """
        if isinstance(page, list):
            return page, None
        if isinstance(page, dict):
            data = page.get("data")
            if data is None:
                data = page.get("objects") or []
            return data, page.get("total")
        return [], None
