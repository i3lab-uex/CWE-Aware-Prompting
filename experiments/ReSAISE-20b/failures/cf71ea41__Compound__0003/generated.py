import json
from typing import Dict

def process_json_payload(req_data: Dict) -> Dict:
    """
    Parse and validate a JSON payload from an HTTP request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing the HTTP request headers and body. It must have:
          - 'headers': dict of request headers (case‑insensitive keys)
          - 'body'   : str or bytes representing the raw request body

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content‑Type header is missing or does not indicate a JSON type,
        or if the body cannot be decoded as valid JSON.
    """
    # Normalize headers to lower‑case keys for case‑insensitive lookup
    headers = {k.lower(): v for k, v in req_data.get("headers", {}).items()}

    # Verify Content‑Type is JSON compatible
    content_type = headers.get("content-type", "")
    if not any(ct in content_type.lower() for ct in ("application/json",
                                                    "application/ld+json",
                                                    "application/vnd.api+json")):
        raise ValueError("Content-Type is not JSON-compatible")

    # Retrieve and decode the body
    raw_body = req_data.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # If bytes, decode to str
    if isinstance(raw_body, (bytes, bytearray)):
        try:
            raw_body = raw_body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Body decoding failed: {exc}") from exc

    # Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return parsed