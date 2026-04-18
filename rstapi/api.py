# Copyright 2024 RST Cloud Pty Ltd

import os
import time

import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import HTTPError, RequestException, Timeout


def _env_int(name, default):
    """Read an int from the environment; invalid or missing values use ``default``."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(str(raw).strip())
    except ValueError:
        return default


def _parse_bool_env_token(s):
    """
    If ``s`` is a boolean-like string, return ``True`` or ``False``.
    Otherwise return ``None`` (caller may treat the value as non-boolean, e.g. a file path).
    """
    lower = s.lower()
    if lower in ("true", "1", "yes", "on"):
        return True
    if lower in ("false", "0", "no", "off"):
        return False
    return None


def _env_bool(name, default):
    """
    Read a boolean from the environment, same idea as :func:`_env_int`.

    Recognises ``true``/``false``, ``1``/``0``, ``yes``/``no``, ``on``/``off`` (case-insensitive).
    Missing, empty, or non-boolean values use ``default``.
    """
    raw = os.environ.get(name)
    if raw is None:
        return default
    s = str(raw).strip()
    if not s:
        return default
    parsed = _parse_bool_env_token(s)
    return default if parsed is None else parsed


def _env_verify(name, default):
    """
    Resolve ``requests`` TLS ``verify`` from the environment: a boolean, or a path to a CA bundle.

    Unlike :func:`_env_bool`, a value that is not a boolean token is returned as a string (CA bundle path).
    """
    raw = os.environ.get(name)
    if raw is None:
        return default
    s = str(raw).strip()
    if not s:
        return default
    parsed = _parse_bool_env_token(s)
    if parsed is not None:
        return parsed
    return s


def _response_or_json(r):
    """Return error dicts unchanged; parse JSON from successful ``requests.Response``."""
    if isinstance(r, dict):
        return r
    return r.json()


def _timeout(retry_delay, attempt):
    attempt += 1
    if retry_delay > 0:
        time.sleep(retry_delay)
    else:
        time.sleep(1 + attempt)  # Backoff
    return attempt


def _make_request(
    _instance,
    method,
    url,
    headers,
    data,
    connect,
    read,
    verify,
    max_retries,
    retrycode=429,
    timeout=0,
    retry_on_status_match=True,
):
    """Helper function to make a request with retry logic."""
    attempt = 0
    req_timeout = (connect, read)
    while attempt < max_retries:
        try:
            if method == "POST":
                if isinstance(data, dict):
                    r = requests.post(
                        url,
                        headers=headers,
                        json=data,
                        timeout=req_timeout,
                        verify=verify,
                    )
                else:
                    r = requests.post(
                        url,
                        headers=headers,
                        data=data,
                        timeout=req_timeout,
                        verify=verify,
                    )
            elif method == "PUT":
                r = requests.put(
                    url,
                    headers=headers,
                    json=data,
                    timeout=req_timeout,
                    verify=verify,
                )
            else:
                r = requests.get(
                    url,
                    headers=headers,
                    timeout=req_timeout,
                    verify=verify,
                )
            if r.status_code != retrycode:
                r.raise_for_status()
                return r
            if not retry_on_status_match:
                return r
            attempt = _timeout(timeout, attempt)

        except (Timeout, RequestsConnectionError):
            attempt = _timeout(timeout, attempt)

        except HTTPError:
            error_response = (
                r.json()
                if r.status_code >= 400
                else {"status": "error", "message": r.text}
            )
            if "message" not in error_response and "error" in error_response:
                error_response["message"] = error_response["error"]
                error_response.pop("error")
            error_response["status"] = "error"
            return error_response

        except RequestException as e:
            return {"status": "error", "message": str(e)}

    return {"status": "error", "message": "Max retries reached"}
