from __future__ import annotations

import json
from typing import Any, Dict


def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req : dict
        Dictionary representing the HTTP request. It must contain at least:
            - ``headers`` : mapping of header names to values
            - ``body``   : raw request body as bytes or string

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the request Content‑Type is not application/json or if JSON decoding fails.
    """
    # 1. Validate presence of required keys
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary")

    headers = req.get("headers")
    body = req.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Request missing headers")

    if body is None:
        raise ValueError("Request missing body")

    # 2. Check Content‑Type header (case‑insensitive)
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. Expected application/json"
        )

    # 3. Verify CSRF token (basic protection)
    csrf_token = None
    for key, value in headers.items():
        if key.lower() == "x-csrf-token":
            csrf_token = value
            break

    if not csrf_token:
        raise ValueError("Missing CSRF token header (X-CSRF-Token)")

    # 4. Decode body to JSON
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to decode request body bytes") from exc
    else:
        body_text = str(body)

    try:
        data = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(data, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return data