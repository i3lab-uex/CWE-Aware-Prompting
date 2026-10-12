import json
from typing import Dict

def process_json_input(req: Dict) -> Dict:
    """
    Parse a JSON request body from a FastAPI-like request dictionary.

    Parameters
    ----------
    req : dict
        A dictionary containing HTTP headers and body of the incoming request.
        Expected keys:
            - "headers" : dict
            - "body"    : bytes or str

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not JSON, or if the body cannot
        be decoded as valid JSON.  The error message is specific to aid debugging.
    """
    # Ensure the request has headers and body
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary.")
    headers = req.get("headers")
    body   = req.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")
    if body is None:
        raise ValueError("Request body is missing.")

    # Check Content-Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    if "application/json" not in content_type.lower():
        raise ValueError(f"Unsupported Content-Type: {content_type}. Expected application/json.")

    # Optional CSRF protection: require a token header
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token is None:
        raise ValueError("Missing CSRF token header (X-CSRF-Token).")

    # Decode body to string if bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be bytes or str.")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("Parsed JSON must be an object (dictionary).")

    return parsed