import json
from typing import Dict, Any


def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body from a FastAPI-like incoming_request dict.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing at least two keys:
            - "headers": a mapping of header names to values
            - "body"   : the raw request body (bytes or str)

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not JSON,
        or if the body cannot be decoded as valid JSON.
    """
    # 1. Validate headers presence and type
    if not isinstance(incoming_request, dict):
        raise ValueError("incoming_request must be a dictionary")

    headers = incoming_request.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Missing or invalid 'headers' in request")

    # 2. Check Content-Type header (case-insensitive)
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if not content_type:
        raise ValueError("Content-Type header is missing")

    # Accept only application/json (allow charset parameter)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type}. Expected application/json"
        )

    # 3. Retrieve body
    raw_body = incoming_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # 4. Ensure body is a string for json.loads
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes")

    # 5. Parse JSON safely
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed