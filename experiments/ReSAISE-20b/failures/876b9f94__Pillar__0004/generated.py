import json
from typing import Dict, Any

def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like request dictionary.

    Parameters
    ----------
    req : dict
        Dictionary containing the HTTP headers and body of the incoming request.
        Expected keys:
            - "headers": dict (case-insensitive header names)
            - "body": str or bytes

    Returns
    -------
    dict
        The parsed JSON body.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not 'application/json'.
        If JSON decoding fails due to malformed data.
    """
    # Retrieve headers, normalizing key names for case-insensitivity
    raw_headers = req.get("headers", {})
    if not isinstance(raw_headers, dict):
        raise ValueError("Request headers must be a dictionary")

    # Convert header names to lowercase for robust lookup
    headers = {k.lower(): v for k, v in raw_headers.items()}

    content_type = headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Allow for charset or other parameters after the MIME type
    mime_type = content_type.split(";")[0].strip().lower()
    if mime_type != "application/json":
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Retrieve body
    body = req.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Ensure body is a string; if bytes, decode using utf-8
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Body bytes could not be decoded as UTF-8") from exc

    if not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes")

    # Attempt JSON parsing
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    # Ensure the result is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dictionary)")

    return parsed