import json
from typing import Dict, Any

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req_data : dict
        A dictionary containing at least the keys:
            - "headers": a mapping of HTTP header names to values
            - "body": the raw request body (bytes or str)

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type is not 'application/json'.
        If the body cannot be decoded as JSON.
    """
    # ---- Validate Content-Type -------------------------------------------------
    headers = req_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Invalid headers format: expected a mapping")

    # HTTP header names are case‑insensitive
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type. Expected application/json")

    # ---- Retrieve and decode body ---------------------------------------------
    raw_body = req_data.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Ensure we have a string for json.loads
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Body decoding error: {exc}") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes")

    # Use json.loads with strict parsing
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"JSON decoding error: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return payload