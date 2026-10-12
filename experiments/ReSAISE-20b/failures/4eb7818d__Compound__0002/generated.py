import json
from typing import Dict, Any

def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    The function expects the incoming `request` dictionary to contain at least
    a `'headers'` mapping and a `'body'` string.  It performs the following
    steps:

    1. **CSRF protection** – checks for a custom header ``X-CSRF-Token``.
       If the header is missing or empty, a :class:`ValueError` is raised.
    2. **JSON decoding** – attempts to decode the request body using
       :func:`json.loads`.  If decoding fails a :class:`ValueError` with a
       descriptive message is raised.
    3. **Return** – returns the decoded JSON as a Python dictionary.

    Parameters
    ----------
    request : dict
        The incoming request object.  It must contain:
          - ``headers``: a mapping of header names to values.
          - ``body``: the raw request body as a string.

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the CSRF token is missing/empty or if JSON decoding fails.
    """
    # 1. Basic request structure validation
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary.")

    headers = request.get("headers")
    body = request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")
    if body is None:
        raise ValueError("Request body is missing.")

    # 2. CSRF protection – enforce presence of a non-empty token header
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if not csrf_token:
        raise ValueError("Missing CSRF token. Request rejected.")

    # 3. JSON decoding
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    # 4. Ensure the payload is a dictionary
    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return payload