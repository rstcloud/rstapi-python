# Copyright 2024 RST Cloud Pty Ltd

from unittest.mock import Mock, patch

from requests.exceptions import RequestException

from rstapi.api import (
    _env_bool,
    _env_int,
    _env_verify,
    _make_request,
    _response_or_json,
    _timeout,
)


def test_env_int_uses_default_when_missing(monkeypatch):
    monkeypatch.delenv("RST_CONNECT_TIMEOUT", raising=False)
    assert _env_int("RST_CONNECT_TIMEOUT", 10) == 10


def test_env_int_parses_integer(monkeypatch):
    monkeypatch.setenv("RST_CONNECT_TIMEOUT", "45")
    assert _env_int("RST_CONNECT_TIMEOUT", 10) == 45


def test_env_int_invalid_falls_back(monkeypatch):
    monkeypatch.setenv("RST_CONNECT_TIMEOUT", "not-a-number")
    assert _env_int("RST_CONNECT_TIMEOUT", 10) == 10


def test_env_int_strips_whitespace(monkeypatch):
    monkeypatch.setenv("RST_READ_TIMEOUT", "  99  ")
    assert _env_int("RST_READ_TIMEOUT", 20) == 99


def test_env_bool_true_and_false(monkeypatch):
    monkeypatch.setenv("RST_TEST_FLAG", "yes")
    assert _env_bool("RST_TEST_FLAG", False) is True
    monkeypatch.setenv("RST_TEST_FLAG", "off")
    assert _env_bool("RST_TEST_FLAG", True) is False


def test_env_bool_non_bool_falls_back_to_default(monkeypatch):
    monkeypatch.setenv("RST_TEST_FLAG", "/not/a/bool")
    assert _env_bool("RST_TEST_FLAG", True) is True


def test_env_verify_false_string(monkeypatch):
    monkeypatch.setenv("RST_SSL_VERIFY", "False")
    assert _env_verify("RST_SSL_VERIFY", True) is False


def test_env_verify_true_string(monkeypatch):
    monkeypatch.setenv("RST_SSL_VERIFY", "True")
    assert _env_verify("RST_SSL_VERIFY", False) is True


def test_env_verify_zero(monkeypatch):
    monkeypatch.setenv("RST_SSL_VERIFY", "0")
    assert _env_verify("RST_SSL_VERIFY", True) is False


def test_env_verify_ca_bundle_path(monkeypatch):
    monkeypatch.setenv("RST_SSL_VERIFY", "/etc/ssl/certs/ca.pem")
    assert _env_verify("RST_SSL_VERIFY", True) == "/etc/ssl/certs/ca.pem"


def test_env_verify_missing_uses_default(monkeypatch):
    monkeypatch.delenv("RST_SSL_VERIFY", raising=False)
    assert _env_verify("RST_SSL_VERIFY", False) is False


def test_response_or_json_passes_through_dict():
    err = {"status": "error", "message": "x"}
    assert _response_or_json(err) is err


def test_response_or_json_parses_response():
    resp = Mock()
    resp.json.return_value = {"id": "1"}
    assert _response_or_json(resp) == {"id": "1"}


def test_timeout_positive_sleeps_fixed_delay():
    with patch("rstapi.api.time.sleep") as sl:
        assert _timeout(2.0, 0) == 1
    sl.assert_called_once_with(2.0)


def test_timeout_zero_uses_backoff():
    with patch("rstapi.api.time.sleep") as sl:
        assert _timeout(0, 2) == 3
    sl.assert_called_once_with(4)


def test_make_request_returns_response_on_success():
    ok = Mock()
    ok.status_code = 200
    ok.raise_for_status = Mock()
    ok.json.return_value = {"ok": True}
    with patch("rstapi.api.requests.get", return_value=ok):
        r = _make_request(
            None,
            "GET",
            "https://example.com/x",
            {},
            None,
            10,
            20,
            True,
            1,
        )
    assert r is ok


def test_make_request_retry_false_returns_immediately_on_retry_code():
    pending = Mock()
    pending.status_code = 301
    with patch("rstapi.api.requests.get", return_value=pending) as g:
        r = _make_request(
            None,
            "GET",
            "https://example.com/x",
            {},
            None,
            10,
            20,
            True,
            5,
            retrycode=301,
            timeout=0,
            retry_on_status_match=False,
        )
    assert r is pending
    g.assert_called_once()


def test_make_request_retries_on_retry_code_then_succeeds():
    r301 = Mock()
    r301.status_code = 301
    ok = Mock()
    ok.status_code = 200
    ok.raise_for_status = Mock()
    ok.json.return_value = {"done": True}

    with patch("rstapi.api.requests.get", side_effect=[r301, ok]) as g:
        with patch("rstapi.api._timeout", side_effect=[1, 2]):
            r = _make_request(
                None,
                "GET",
                "https://example.com/x",
                {},
                None,
                10,
                20,
                True,
                3,
                retrycode=301,
                timeout=1,
                retry_on_status_match=True,
            )
    assert r is ok
    assert g.call_count == 2


def test_make_request_request_exception_message_is_string():
    with patch(
        "rstapi.api.requests.get",
        side_effect=RequestException("network down"),
    ):
        r = _make_request(
            None,
            "GET",
            "https://example.com/x",
            {},
            None,
            10,
            20,
            True,
            1,
        )
    assert r == {"status": "error", "message": "network down"}


def test_make_request_post_uses_json_for_dict():
    ok = Mock()
    ok.status_code = 200
    ok.raise_for_status = Mock()
    with patch("rstapi.api.requests.post", return_value=ok) as p:
        _make_request(
            None,
            "POST",
            "https://example.com/x",
            {},
            {"a": 1},
            10,
            20,
            True,
            1,
        )
    kwargs = p.call_args[1]
    assert kwargs.get("json") == {"a": 1}
