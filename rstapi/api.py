# Copyright 2024 RST Cloud Pty Ltd

import time
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError


def _make_request(
    self, method, url, headers, data, connect, read, verify, max_retries, retrycode=400, timeout=0
):
    """Helper function to make a request with retry logic."""
    attempt = 0
    request_params = {
        "url": url,
        "headers": headers,
        "timeout": (connect, read),
        "verify": verify,
    }
    while attempt < max_retries:
        try:
            # Determine the request method to use
            if method == "POST":
                if type(data) is dict:
                    r = requests.post(json=data, **request_params)
                else:
                    r = requests.post(data=data, **request_params)
            elif method == "PUT":
                r = requests.put(
                    url,
                    headers=headers,
                    json=data,
                    timeout=(connect, read),
                    verify=verify,
                )
            else:  # Default to GET
                r = requests.get(**request_params)
            r.raise_for_status()  # Raise an HTTPError for bad responses
            return r  # Return the full response for successful requests

        except (Timeout, ConnectionError) as e:
            attempt += 1
            if timeout > 0:
                time.sleep(timeout)
            else:
                time.sleep(1 + attempt)  # Backoff

        except HTTPError as e:
            error_response = (
                r.json()
                if r.status_code >= retrycode
                else {"status": "error", "message": r.text}
            )
            if "message" not in error_response and "error" in error_response:
                error_response["message"] = error_response["error"]
                error_response.pop("error")
            error_response["status"] = "error"
            return error_response  # Return structured error response

        except RequestException as e:
            return {"status": "error", "message": {e}}

    return {"status": "error", "message": "Max retries reached"}
