1.2.0 (2026-06-19)
------------------

- **`threatobjects` client** (`rstapi.threatobjects`) for the **RST Threat Library**: `GET /threat-objects/{object_type}` over `intrusion-sets`, `malware`, `tools`, and `campaigns`. `GetThreatObjects(object_type, ...)` supports `limit`/`offset` pagination, single lookups via `id`/`name`, `filter` search expressions, and sorting (`orderBy` = `created_at`/`modified`/`updated_at`, `orderMode` = `asc`/`desc`). Convenience helpers `GetThreatObjectById` / `GetThreatObjectByName`.
- **Threat Library pagination helper**: `IterThreatObjects(object_type, page_size=100, ...)` is a generator that walks every page (stopping on `total` or a short page) and raises on an API error so callers never silently truncate. Tolerant of `{"data": [...], "total": N}`, bare-list, and `{"objects": [...]}` response shapes. Constructor and environment variables (`APIKEY`, `APIURL`, `RST_API_KEY`, timeouts, `RST_SSL_VERIFY`) match the other clients; query params and the object-type path segment are URL-encoded.


1.1.0 (2026-04-09)
------------------

- **`scan` client** (`rstapi.scan`) for the RST Cloud Scan API: Cobalt Strike beacon (`/scan/cs-beacon`), SSL certificate (`/scan/ssl/certificate`), favicon (`/scan/favicon`), HTML body (`/scan/html/body`), HTML body JavaScript (`/scan/html/body/js`), and HTML screenshots — first, full-page, and last frame (`/scan/html/screenshot/*`). Constructor and environment variables match other clients (`APIKEY`, `APIURL`, `RST_API_KEY`, timeouts, etc.).
- **Scan — optional file output**: pass **`path`** to save binary or text — PNG from `image_base64` / `base64_image` (screenshots and favicon with **`include_base64=True`** for the favicon API’s `base64` query flag), or raw response bytes for HTML body and JS endpoints. Successful file writes add **`saved_image_path`** to JSON responses where applicable, or return **`{"status": "ok", "message": path}`** for raw body saves (same pattern as threat feed / report PDF).
- **`connectivity` client** (`rstapi.connectivity`) with **`CheckApiKey()`** calling **`GET /auth/check`**. The JSON response includes **`quota`** (`used`, `limit`, **`remaining`**, `period`) and **`check`** (`status`, etc.) so applications can read how many requests are left in the current quota window.
- **URL encoding**: query parameters and path segments use `urllib.parse` (`quote` / `urlencode`). IoC lookup, Noise Control lookup, Whois domain paths, Report Hub report URLs, and Threat Feed query strings encode reserved characters (`&`, `=`, `%`, spaces, Unicode, etc.) correctly. Simple ASCII-only values behave as before.
- **Environment variables**: `RST_CONNECT_TIMEOUT`, `RST_READ_TIMEOUT`, and `RST_MAX_RETRIES` are parsed as integers; invalid values fall back to the constructor default. **`RST_SSL_VERIFY`** is resolved for `requests` TLS **`verify`**: common boolean strings (`true`/`false`, `1`/`0`, `yes`/`no`, `on`/`off`) become real booleans; any other non-empty value is used as a CA bundle path string.
- **`noisecontrol`**: instance attribute `APIURL` renamed to **`API_URL`** for consistency with other clients (constructor parameter name `APIURL` is unchanged). Any code that read **`noisecontrol.APIURL`** must use **`API_URL`** instead.
- **`noisecontrol.BatchResult`**: parameters **`timeout`** and **`retry`** are honored — `timeout` is the delay between retries when the server responds with HTTP 301 (pending); `retry=False` returns the first response immediately without waiting on 301 (including a single JSON body from a 301 response).
- **Internals**: success vs error detection uses `isinstance(..., dict)` instead of probing `requests.Response` with `in`. `RequestException` errors are surfaced with `message` as a string. POST JSON bodies use `isinstance(data, dict)`.


1.0.4 (2024-09-27)
------------------

- timeout bugfix
  

1.0.3 (2024-09-27)
------------------

- Added retry logic for all API endpoints
- Added connect/read timeouts and an ability to ignose SSL certs
- Noise Control Batch result API has its own retry parameter
- All errors are standardised as {"status": "error", "message": "Reason"}


1.0.2 (2023-12-22)
------------------

- Package updates

1.0.1 (2023-12-22)
------------------

- Package updates

1.0.0 (2023-12-22)
------------------

- Move beta to version 1.0.0
