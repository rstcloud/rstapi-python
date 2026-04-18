# Copyright 2024 RST Cloud Pty Ltd

from unittest.mock import patch

from rstapi.connectivity import connectivity


def test_check_api_key_calls_auth_check():
    with patch("rstapi.connectivity._make_request") as m:
        m.return_value = {
            "check": {"name": "CheckApiKey", "status": "valid"},
            "quota": {
                "used": 1,
                "limit": 1000,
                "remaining": 999,
                "period": "DAY",
            },
        }
        c = connectivity(APIKEY="secret")
        out = c.CheckApiKey()
    url = m.call_args[0][2]
    assert url.endswith("/auth/check")
    assert m.call_args[0][1] == "GET"
    assert out["quota"]["remaining"] == 999
    assert out["check"]["status"] == "valid"
