import json
from typing import Dict, Any

def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse a JSON payload from an HTTP request.

    Parameters
    ----------
    req_data : dict
        A dictionary containing the request headers under the key 'headers'
        and the raw body string under the key 'body'.

    Returns
    -------
    dict
        The parsed JSON content.

    Raises
    ------
    ValueError
        If the request does not contain a JSON-compatible Content-Type header.
        If the body cannot be decoded as valid JSON.
    """
    if not isinstance(req_data, dict):
        raise ValueError("req_data must be a dictionary")

    headers = req_data.get("headers", {})
    body = req_data.get("body", "")

    # Ensure headers is a dict
    if not isinstance(headers, dict):
        raise ValueError("headers must be a dictionary")

    # Normalize header keys to lowercase for case‑insensitive lookup
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = str(value).lower()
            break

    if not content_type or "application/json" not in content_type:
        raise ValueError("Content-Type must be application/json or compatible")

    # Reject empty body early
    if not isinstance(body, str) or body.strip() == "":
        raise ValueError("Request body is empty")

    # Optionally limit size (e.g., 1MB) to mitigate large payload attacks
    MAX_BODY_SIZE = 1_048_576  # 1 MiB
    if len(body.encode("utf-8")) > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds maximum size of {MAX_BODY_SIZE} bytes")

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed