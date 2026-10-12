import json
from typing import Any, Dict

def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse the JSON payload from an HTTP request.

    Parameters
    ----------
    req_data : dict
        A dictionary containing the headers and body of an HTTP request.
        Expected keys:
            - 'headers': a dict of header names to values
            - 'body'   : the raw request body (bytes or str)

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not JSON-compatible.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = req_data.get("headers", {})
    body = req_data.get("body")

    if not headers:
        raise ValueError("Missing request headers.")

    # Normalise header names to lowercase for case‑insensitive lookup
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")

    # Accept common JSON media types
    json_media_types = {
        "application/json",
        "application/ld+json",
        "application/vnd.api+json",
    }
    # Allow charset parameters, e.g. application/json; charset=utf-8
    media_type = content_type.split(";")[0].strip().lower()
    if media_type not in json_media_types:
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Ensure body is a string for json.loads
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF‑8.") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Request body must be bytes or str.")

    # Parse JSON
    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return payload