# Copyright 2024 RST Cloud Pty Ltd

import base64
import binascii
import os
from urllib.parse import urlencode

from .api import _env_int, _env_verify, _make_request, _response_or_json


def _response_text_or_json_from_response(r):
    """Parse JSON when possible; otherwise return decoded text (HTML/JS/plain)."""
    try:
        return r.json()
    except ValueError:
        return r.text


def _maybe_save_base64_field(data, field_name, path):
    """
    If ``path`` is set and ``data`` is a dict containing ``field_name`` (base64),
    decode and write bytes to ``path``, then return a copy of ``data`` with
    ``saved_image_path`` set. On failure returns an error dict.
    """
    if not path or not isinstance(data, dict):
        return data
    b64 = data.get(field_name)
    if not b64:
        return data
    try:
        raw = base64.b64decode(b64)
        with open(path, "wb") as f:
            f.write(raw)
    except (binascii.Error, ValueError, TypeError, OSError) as e:
        return {"status": "error", "message": str(e)}
    out = dict(data)
    out["saved_image_path"] = path
    return out


def _maybe_save_raw_body(r, path):
    """Write response body to ``path``; return ok/error dict. Caller ensures ``r`` is Response."""
    try:
        with open(path, "wb") as f:
            f.write(r.content)
    except OSError as e:
        return {"status": "error", "message": str(e)}
    return {"status": "ok", "message": path}


class scan(object):
    """RST Cloud Scan API: Cobalt Strike beacon, SSL certificate, favicon, HTML body/JS, screenshots."""

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

    def _headers(self):
        return {"Accept": "*/*", "X-Api-Key": self.APIKEY}

    def GetCsBeacon(self, target):
        """GET /scan/cs-beacon — Cobalt Strike beacon scan (x86/x64 metadata)."""
        q = urlencode({"target": target})
        apiurl = f"{self.API_URL}/scan/cs-beacon?{q}"
        r = _make_request(
            self,
            "GET",
            apiurl,
            self._headers(),
            None,
            self.CONNECT,
            self.READ,
            self.VERIFY,
            self.MAX_RETRIES,
        )
        return _response_or_json(r)

    def GetSslCertificate(self, target):
        """GET /scan/ssl/certificate — SSL certificate details for IP:port."""
        q = urlencode({"target": target})
        apiurl = f"{self.API_URL}/scan/ssl/certificate?{q}"
        r = _make_request(
            self,
            "GET",
            apiurl,
            self._headers(),
            None,
            self.CONNECT,
            self.READ,
            self.VERIFY,
            self.MAX_RETRIES,
        )
        return _response_or_json(r)

    def GetFavicon(self, target, include_base64=False, path=""):
        """
        GET /scan/favicon — Favicon metadata and hashes.

        If ``include_base64`` is True the API may include ``base64_image``. When ``path`` is set and
        that field is present, the image is decoded and written to ``path``; the returned
        dict includes ``saved_image_path``.
        """
        params = {"target": target}
        if include_base64:
            params["base64"] = "true"
        q = urlencode(params)
        apiurl = f"{self.API_URL}/scan/favicon?{q}"
        r = _make_request(
            self,
            "GET",
            apiurl,
            self._headers(),
            None,
            self.CONNECT,
            self.READ,
            self.VERIFY,
            self.MAX_RETRIES,
        )
        if isinstance(r, dict):
            return r
        data = r.json()
        if path:
            data = _maybe_save_base64_field(data, "base64_image", path)
        return data

    def GetHtmlBody(self, target, path=""):
        """
        GET /scan/html/body — HTML body for a public URL.

        If ``path`` is set, the raw response body is written to that file and
        ``{"status": "ok", "message": <path>}`` is returned. Otherwise returns
        parsed JSON or text.
        """
        q = urlencode({"target": target})
        apiurl = f"{self.API_URL}/scan/html/body?{q}"
        r = _make_request(
            self,
            "GET",
            apiurl,
            self._headers(),
            None,
            self.CONNECT,
            self.READ,
            self.VERIFY,
            self.MAX_RETRIES,
        )
        if isinstance(r, dict):
            return r
        if path:
            return _maybe_save_raw_body(r, path)
        return _response_text_or_json_from_response(r)

    def GetHtmlBodyJs(self, target, path=""):
        """
        GET /scan/html/body/js — JavaScript extracted from the page.

        If ``path`` is set, the raw body is saved to ``path``; otherwise JSON or text.
        """
        q = urlencode({"target": target})
        apiurl = f"{self.API_URL}/scan/html/body/js?{q}"
        r = _make_request(
            self,
            "GET",
            apiurl,
            self._headers(),
            None,
            self.CONNECT,
            self.READ,
            self.VERIFY,
            self.MAX_RETRIES,
        )
        if isinstance(r, dict):
            return r
        if path:
            return _maybe_save_raw_body(r, path)
        return _response_text_or_json_from_response(r)

    def GetHtmlScreenshotFirst(self, target, path=""):
        """GET /scan/html/screenshot/first — JSON with ``image_base64``; optional PNG file via ``path``."""
        return self._screenshot("/scan/html/screenshot/first", target, path)

    def GetHtmlScreenshotFull(self, target, path=""):
        """GET /scan/html/screenshot/full — full-page screenshot."""
        return self._screenshot("/scan/html/screenshot/full", target, path)

    def GetHtmlScreenshotLast(self, target, path=""):
        """GET /scan/html/screenshot/last — last frame screenshot."""
        return self._screenshot("/scan/html/screenshot/last", target, path)

    def _screenshot(self, endpoint, target, path=""):
        q = urlencode({"target": target})
        apiurl = f"{self.API_URL}{endpoint}?{q}"
        r = _make_request(
            self,
            "GET",
            apiurl,
            self._headers(),
            None,
            self.CONNECT,
            self.READ,
            self.VERIFY,
            self.MAX_RETRIES,
        )
        if isinstance(r, dict):
            return r
        data = r.json()
        if path:
            data = _maybe_save_base64_field(data, "image_base64", path)
        return data
