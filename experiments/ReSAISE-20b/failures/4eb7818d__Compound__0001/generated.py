import json
from typing import Dict, Any


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    The function expects a dictionary representing the HTTP request with
    at least two keys:
        * ``headers`` – a mapping of header names to values.
        * ``body``    – the raw request body (bytes or str).

    Security considerations:
        * CSRF protection is performed by requiring an ``X-CSRF-Token`` header
          that must be present and non‑empty.  In a real application this token
          would be compared against the user’s session token; here we simply
          enforce its presence to illustrate the principle.
        * The body is decoded as UTF‑8 and parsed using ``json.loads``.
          Any decoding or parsing error results in a clear ValueError.

    Parameters
    ----------
    request : dict
        The incoming request dictionary containing ``headers`` and ``body``.

    Returns
    -------
    dict
        The parsed JSON body as a Python dictionary.

    Raises
    ------
    ValueError
        If the CSRF token is missing or empty.
        If JSON decoding fails.
        For any other problems with the request structure.
    """
    # Validate request shape
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary.")

    headers = request.get("headers")
    body = request.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Missing or invalid 'headers' in request.")

    if body is None:
        raise ValueError("Missing 'body' in request.")

    # CSRF protection: require a non‑empty X-CSRF-Token header
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not isinstance(csrf_token, str) or csrf_token.strip() == "":
        raise ValueError("Missing or empty CSRF token in request headers.")

    # Decode body to string if it's bytes
    try:
        if isinstance(body, bytes):
            body_str = body.decode("utf-8")
        elif isinstance(body, str):
            body_str = body
        else:
            raise ValueError("Body must be bytes or str.")
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to decode request body: {exc}") from exc

    # Parse JSON
    try:
        parsed_body = json.loads(body_str)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Invalid JSON in request body: {exc}") from exc

    if not isinstance(parsed_body, dict):
        raise ValueError("Parsed JSON must be an object (dict).")

    return parsed_body