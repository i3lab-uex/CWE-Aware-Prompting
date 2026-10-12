import json
from typing import Dict, Any

def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of a FastAPI request represented as a dictionary.

    Parameters
    ----------
    req : dict
        Dictionary containing the HTTP headers and body of an incoming request.
        Expected keys:
            - "headers": a dict mapping header names to values
            - "body": the raw request body (bytes or str)

    Returns
    -------
    dict
        Parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not application/json.
        If JSON decoding fails due to malformed input.
    """
    # Retrieve headers and body
    headers = req.get("headers", {})
    raw_body = req.get("body")

    # Normalise header names to lowercase for case-insensitive lookup
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    # Validate Content-Type header
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Invalid Content-Type: expected 'application/json', got '{content_type}'"
        )

    # Ensure body is a string; if bytes, decode using UTF-8
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc
    elif not isinstance(raw_body, str):
        raise ValueError(f"Body must be a string or bytes, got {type(raw_body).__name__}")

    # Parse JSON safely
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    # Ensure the parsed object is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError(f"Expected JSON object (dict), got {type(parsed).__name__}")

    return parsed