# Copyright 2024 RST Cloud Pty Ltd

from unittest.mock import patch

from rstapi import threatobjects


def _resp(payload):
    """A fake requests.Response whose .json() returns ``payload``."""
    class _R:
        def json(self):
            return payload

    return _R()


def test_path_includes_object_type():
    with patch("rstapi.threatobjects._make_request") as m:
        m.return_value = {"status": "error", "message": "x"}
        threatobjects(APIKEY="k").GetThreatObjects("malware")
    url = m.call_args[0][2]
    assert url.endswith("/threat-objects/malware")
    assert m.call_args[0][1] == "GET"


def test_query_params_encoded():
    with patch("rstapi.threatobjects._make_request") as m:
        m.return_value = {"status": "error", "message": "x"}
        threatobjects(APIKEY="k").GetThreatObjects(
            "intrusion-sets", limit=50, offset=100, orderBy="modified", orderMode="desc"
        )
    url = m.call_args[0][2]
    assert "limit=50" in url and "offset=100" in url
    assert "orderBy=modified" in url and "orderMode=desc" in url


def test_by_name_encodes_value():
    with patch("rstapi.threatobjects._make_request") as m:
        m.return_value = {"status": "error", "message": "x"}
        threatobjects(APIKEY="k").GetThreatObjectByName("campaigns", "a&b")
    url = m.call_args[0][2]
    assert "name=a%26b" in url


def test_iter_paginates_and_stops_on_short_page():
    pages = [
        _resp({"data": [{"id": 1}, {"id": 2}], "total": 3}),
        _resp({"data": [{"id": 3}], "total": 3}),
    ]
    with patch("rstapi.threatobjects._make_request", side_effect=pages) as m:
        out = list(threatobjects(APIKEY="k").IterThreatObjects("malware", page_size=2))
    assert [o["id"] for o in out] == [1, 2, 3]
    assert m.call_count == 2


def test_iter_raises_on_api_error():
    with patch("rstapi.threatobjects._make_request") as m:
        m.return_value = {"status": "error", "message": "boom"}
        gen = threatobjects(APIKEY="k").IterThreatObjects("tools")
        try:
            list(gen)
            assert False, "expected RuntimeError"
        except RuntimeError as exc:
            assert "boom" in str(exc)


def test_page_items_tolerates_bare_list():
    items, total = threatobjects._page_items([{"id": 1}])
    assert items == [{"id": 1}] and total is None


def test_exported_from_package():
    import rstapi

    assert hasattr(rstapi, "threatobjects")
