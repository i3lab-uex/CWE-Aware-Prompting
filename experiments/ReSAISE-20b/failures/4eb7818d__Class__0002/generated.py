import json
from typing import Any, Dict

MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB limit to avoid large payloads


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        The incoming request object. Expected keys:
            - "headers": a mapping of header names to values
            - "body": the raw request body (str or bytes)

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the content type is not application/json,
        if the body exceeds MAX_BODY_SIZE,
        or if JSON decoding fails.
    """
    # 1. Verify headers exist and are a mapping
    headers = request.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    # 2. Check Content-Type
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type. Expected application/json.")

    # 3. Retrieve body
    raw_body = request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body.")
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc

    # 4. Enforce size limit to mitigate DoS
    if len(raw_body) > MAX_BODY_SIZE:
        raise ValueError("Request body too large.")

    # 5. Parse JSON
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decoding failed: {exc}") from exc

    # 6. Ensure payload is a dict (typical for API bodies)
    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object.")

    return payload