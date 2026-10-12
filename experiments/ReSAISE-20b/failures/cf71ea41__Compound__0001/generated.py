import json
from typing import Dict, Any


def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON payload from an incoming HTTP request.

    Parameters
    ----------
    req_data : dict
        Dictionary containing the HTTP request data.  It must contain at least two keys:
            - ``headers``: a mapping of header names to values.
            - ``body``: the raw request body (bytes or str).

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        * If the request body is not valid JSON.
        * If the ``Content-Type`` header does not indicate a JSON payload
          (e.g., missing or not starting with ``application/json``).
        * If a CSRF token header is expected but missing or empty.
    """
    # Ensure required keys are present
    if not isinstance(req_data, dict):
        raise ValueError("Request data must be a dictionary")

    headers = req_data.get("headers")
    body = req_data.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")
    if body is None:
        raise ValueError("Request body is missing")

    # Normalise header keys to lowercase for case‑insensitive lookup
    headers = {k.lower(): v for k, v in headers.items()}

    # Verify Content‑Type
    content_type = headers.get("content-type", "")
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. "
            "Expected application/json."
        )

    # Optional CSRF protection: require X-CSRF-Token header
    csrf_token = headers.get("x-csrf-token")
    if not csrf_token:
        raise ValueError(
            "Missing CSRF token header (X-CSRF-Token). "
            "CSRF protection is required."
        )

    # Decode body if it's bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF‑8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be bytes or str")

    # Parse JSON safely
    try:
        payload = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return payload