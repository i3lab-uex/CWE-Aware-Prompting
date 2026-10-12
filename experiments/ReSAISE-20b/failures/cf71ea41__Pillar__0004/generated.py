import json
from typing import Dict, Any

def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse a JSON payload from an HTTP request.

    Parameters
    ----------
    req_data : dict
        A dictionary containing at least two keys:
            - 'headers': a mapping of HTTP headers (case‑insensitive)
            - 'body'   : the raw request body as a string

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content‑Type header is missing or not JSON compatible.
        If the body cannot be parsed as valid JSON.
    """
    # 1. Extract headers and body
    try:
        headers = req_data["headers"]
        raw_body = req_data["body"]
    except KeyError as exc:
        raise ValueError("Request data must contain 'headers' and 'body'") from exc

    # 2. Normalize header names to lower case for case‑insensitive lookup
    headers_lower = {k.lower(): v for k, v in headers.items()}

    # 3. Verify Content‑Type header
    content_type = headers_lower.get("content-type", "")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept common JSON MIME types
    json_mime_types = {"application/json", "application/ld+json"}
    # Allow charset parameters (e.g., application/json; charset=utf-8)
    if not any(ct.split(";")[0].strip() in json_mime_types for ct in content_type.split(",")):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # 4. Parse JSON safely
    try:
        parsed = json.loads(raw_body)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError("Malformed JSON payload") from exc

    # 5. Ensure the result is a dictionary (object in JSON)
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object")

    return parsed