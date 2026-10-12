import json
from typing import Dict, Any


def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like request dictionary.

    Parameters
    ----------
    req : dict
        A dictionary that must contain a 'headers' key (dict of HTTP headers)
        and a 'body' key (the raw request payload as bytes or string).

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or does not indicate JSON,
        or if the body cannot be decoded as valid JSON.
    """
    # Validate presence of headers
    headers = req.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Missing or invalid 'headers' in request")

    # Check Content-Type
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Content-Type must be application/json")

    # Retrieve body
    body = req.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Convert bytes to string if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be bytes or str")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    # Ensure the parsed result is a dict (JSON object)
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed