import json
from typing import Dict, Any

def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req : dict
        Dictionary representing the incoming HTTP request. It must contain:
            - 'headers': a mapping of header names to values
            - 'body': the raw request body as bytes or str

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the request Content-Type is not application/json or
        if JSON decoding fails.

    Notes
    -----
    The function performs minimal CSRF protection by requiring the presence
    of a custom header `X-CSRF-Token`. If this header is missing, a generic
    error is raised. This approach is not foolproof but demonstrates awareness
    of the CWE-352 vulnerability.
    """
    # Ensure headers are present
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary")
    headers = req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")

    # Check for CSRF token header (simple example)
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token:
        raise ValueError("Missing CSRF token header")

    # Validate Content-Type
    content_type = headers.get("Content-Type", "")
    if not isinstance(content_type, str):
        raise ValueError("Invalid Content-Type header")
    # Allow application/json and variants with charset
    allowed_types = ["application/json", "application/ld+json"]
    if not any(content_type.lower().startswith(t) for t in allowed_types):
        raise ValueError("Unsupported Content-Type: must be application/json")

    # Get the body
    body = req.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Decode bytes to str if necessary
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc
    elif not isinstance(body, str):
        raise ValueError("Body must be bytes or string")

    # Parse JSON
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decoding error: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("JSON payload must be an object")

    return data