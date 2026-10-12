import json
from typing import Dict, Any

def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse the JSON body of an HTTP request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing at least two keys:
            - 'headers': a mapping of request headers (case-insensitive)
            - 'body'   : the raw body bytes or string

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not JSON-compatible,
        or if the body cannot be decoded as valid JSON.
    """
    # Retrieve headers and body
    headers = req_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Normalise header names to lowercase for case‑insensitive lookup
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Ensure the content type indicates JSON
    if not isinstance(content_type, str) or "application/json" not in content_type.lower():
        raise ValueError(f"Unsupported Content-Type: {content_type!r}")

    # Retrieve the raw body
    body = req_data.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Decode bytes to string if necessary
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF‑8") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object")

    return parsed