# Copyright 2024 RST Cloud Pty Ltd

import base64
from unittest.mock import Mock, patch

from rstapi.scan import (
    _maybe_save_base64_field,
    _maybe_save_raw_body,
    _response_text_or_json_from_response,
    scan,
)


def test_maybe_save_base64_field_writes_and_adds_path(tmp_path):
    png = b"\x89PNG\r\n"
    data = {"image_base64": base64.b64encode(png).decode("ascii")}
    out_path = tmp_path / "out.png"
    result = _maybe_save_base64_field(data, "image_base64", str(out_path))
    assert result["saved_image_path"] == str(out_path)
    assert out_path.read_bytes() == png


def test_maybe_save_base64_field_skips_without_path():
    data = {"image_base64": "abc"}
    assert _maybe_save_base64_field(data, "image_base64", "") == data


def test_maybe_save_base64_field_invalid_base64_returns_error_dict(tmp_path):
    """Malformed base64 raises binascii.Error from b64decode; must not propagate."""
    data = {"image_base64": "@@@not-valid-base64@@@"}
    out_path = tmp_path / "x.bin"
    result = _maybe_save_base64_field(data, "image_base64", str(out_path))
    assert result["status"] == "error"
    assert "message" in result
    assert not out_path.exists()


def test_maybe_save_raw_body(tmp_path):
    r = Mock()
    r.content = b"<html></html>"
    path = tmp_path / "a.html"
    assert _maybe_save_raw_body(r, str(path)) == {
        "status": "ok",
        "message": str(path),
    }
    assert path.read_bytes() == b"<html></html>"


def test_response_text_or_json_prefers_json():
    r = Mock()
    r.json.return_value = {"a": 1}
    assert _response_text_or_json_from_response(r) == {"a": 1}


def test_response_text_or_json_falls_back_to_text():
    r = Mock()
    r.json.side_effect = ValueError()
    r.text = "<html>"
    assert _response_text_or_json_from_response(r) == "<html>"


def test_scan_get_cs_beacon_url():
    with patch("rstapi.scan._make_request") as m:
        m.return_value = {"status": "error", "message": "x"}
        c = scan(APIKEY="k")
        c.GetCsBeacon("1.2.3.4:443")
    url = m.call_args[0][2]
    assert "/scan/cs-beacon" in url
    assert "target=" in url


def test_scan_screenshot_saves_image(tmp_path):
    png = b"\x89PNG\r\n\x00"
    body = {
        "url": "https://example.com",
        "image_base64": base64.b64encode(png).decode("ascii"),
    }
    r = Mock()
    r.json.return_value = body
    out = tmp_path / "cap.png"
    with patch("rstapi.scan._make_request", return_value=r):
        c = scan(APIKEY="k")
        result = c.GetHtmlScreenshotFirst("https://example.com", path=str(out))
    assert result["saved_image_path"] == str(out)
    assert out.read_bytes() == png


def test_scan_favicon_include_base64_query():
    resp = Mock()
    resp.json.return_value = {"req_url": "http://x"}
    with patch("rstapi.scan._make_request", return_value=resp) as m:
        c = scan(APIKEY="k")
        c.GetFavicon("51.1.1.1:80", include_base64=True)
    url = m.call_args[0][2]
    assert "base64=true" in url
    assert "/scan/favicon" in url


def test_scan_html_body_save_to_file(tmp_path):
    r = Mock()
    r.content = b"<!doctype html><title>x</title>"
    path = tmp_path / "body.html"
    with patch("rstapi.scan._make_request", return_value=r):
        c = scan(APIKEY="k")
        result = c.GetHtmlBody("https://example.com", path=str(path))
    assert result == {"status": "ok", "message": str(path)}
    assert path.read_bytes() == r.content
