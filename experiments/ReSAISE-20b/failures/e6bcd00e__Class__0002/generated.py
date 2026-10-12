import json
from typing import Dict, Any

def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body from an incoming FastAPI-like request.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing the HTTP headers under the key ``"headers"``
        and the raw request body under the key ``"body"``.  The headers
        dictionary is expected to be case‑insensitive (e.g., keys may be
        lower‑case or title‑cased).

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the ``Content-Type`` header is missing or does not contain
        ``application/json``.
        If the request body cannot be decoded as valid JSON.
    """
    # 1. Verify headers exist and are a mapping
    if not isinstance(incoming_request, dict):
        raise ValueError("Request must be a dictionary")

    headers = incoming_request.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Headers must be provided as a dictionary")

    # 2. Normalize header names for case‑insensitive lookup
    normalized_headers = {k.lower(): v for k, v in headers.items()}

    # 3. Ensure Content-Type is application/json
    content_type = normalized_headers.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Invalid or missing Content-Type; expected application/json")

    # 4. Retrieve the body
    raw_body = incoming_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # 5. Decode JSON
    try:
        decoded = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from None

    # 6. Ensure the result is a dictionary
    if not isinstance(decoded, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return decoded