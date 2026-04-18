# Copyright 2024 RST Cloud Pty Ltd

from unittest.mock import Mock, patch

from rstapi import ioclookup, noisecontrol, reporthub, threatfeed, whoisapi


def test_ioclookup_encodes_value_in_query():
    with patch("rstapi.ioclookup._make_request") as m:
        m.return_value = {"status": "error", "message": "x"}
        c = ioclookup(APIKEY="k")
        c.GetIndicator("a&b=c")
    url = m.call_args[0][2]
    assert "a%26b%3Dc" in url


def test_whoisapi_encodes_domain():
    with patch("rstapi.whoisapi._make_request") as m:
        m.return_value = {"status": "error", "message": "x"}
        c = whoisapi(APIKEY="k")
        c.GetDomainInfo("ex ample.com")
    url = m.call_args[0][2]
    assert "ex%20ample.com" in url


def test_noisecontrol_has_api_url_attribute():
    c = noisecontrol(APIKEY="x")
    assert hasattr(c, "API_URL")
    assert c.API_URL.startswith("http")


def test_noisecontrol_value_lookup_encodes_query():
    with patch("rstapi.noisecontrol._make_request") as m:
        m.return_value = {"status": "error", "message": "x"}
        c = noisecontrol(APIKEY="k")
        c.ValueLookup("1&2")
    url = m.call_args[0][2]
    assert "1%262" in url


def test_reporthub_encodes_report_query_params():
    with patch("rstapi.reporthub._make_request") as m:
        m.return_value = {"status": "error", "message": "x"}
        c = reporthub(APIKEY="k")
        c.GetReportJSON("id&x", lang="en=g")
    url = m.call_args[0][2]
    assert "id%26x" in url
    assert "en%3Dg" in url or "lang=en%3Dg" in url


def test_threatfeed_encodes_feed_query():
    with patch("rstapi.threatfeed._make_request") as m:
        m.return_value = {"status": "error", "message": "x"}
        c = threatfeed(APIKEY="k")
        c.GetFeed("url", filetype="csv", fdate="lat est")
    url = m.call_args[0][2]
    assert "lat+est" in url or "lat%20est" in url


def test_client_env_int_for_timeouts(monkeypatch):
    monkeypatch.setenv("RST_CONNECT_TIMEOUT", "33")
    monkeypatch.setenv("RST_READ_TIMEOUT", "44")
    monkeypatch.setenv("RST_MAX_RETRIES", "7")
    c = ioclookup(APIKEY="k")
    assert c.CONNECT == 33
    assert c.READ == 44
    assert c.MAX_RETRIES == 7


def test_client_rst_ssl_verify_env_false_is_bool(monkeypatch):
    monkeypatch.setenv("RST_SSL_VERIFY", "False")
    c = ioclookup(APIKEY="k")
    assert c.VERIFY is False
    assert isinstance(c.VERIFY, bool)


def test_batch_result_passes_retry_and_timeout_to_make_request():
    with patch("rstapi.noisecontrol._make_request") as m:
        m.return_value = {"status": "error", "message": "x"}
        c = noisecontrol(APIKEY="k")
        c.BatchResult("domain", "tok", attempts=3, timeout=2, retry=False)
    kwargs = m.call_args[1]
    assert m.call_args[0][8] == 1
    assert kwargs["retrycode"] == 301
    assert kwargs["timeout"] == 2
    assert kwargs["retry_on_status_match"] is False


def test_batch_result_retry_true_uses_attempts():
    with patch("rstapi.noisecontrol._make_request") as m:
        m.return_value = {"status": "error", "message": "x"}
        c = noisecontrol(APIKEY="k")
        c.BatchResult("domain", "tok", attempts=9, timeout=0.5, retry=True)
    assert m.call_args[0][8] == 9
    assert m.call_args[1]["retry_on_status_match"] is True


def test_connectivity_check_api_key_method():
    from rstapi import connectivity

    expected = {
        "check": {"name": "CheckApiKey", "status": "valid"},
        "quota": {"used": 1, "limit": 1000, "remaining": 999, "period": "DAY"},
    }
    with patch("rstapi.connectivity._make_request") as m:
        resp = Mock()
        resp.json.return_value = expected
        m.return_value = resp
        c = connectivity(APIKEY="k")
        result = c.CheckApiKey()
    url = m.call_args[0][2]
    assert url.endswith("/auth/check")
    assert result["quota"]["remaining"] == 999
