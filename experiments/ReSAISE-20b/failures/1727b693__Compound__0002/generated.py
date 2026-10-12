import json
from typing import Dict, Any

def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        A dictionary containing the request headers and body.
        Expected keys are:
            - "headers": a dict-like object with HTTP header names as keys
            - "body": the raw request body (bytes or str)

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the content type is not acceptable.
        If JSON decoding fails or the decoded payload is not a dict.
    """
    # Extract headers and body safely
    headers = input_data.get("headers", {})
    body   = input_data.get("body")

    if body is None:
        raise ValueError("Request body is missing.")

    # Normalise header names to lowercase for case‑insensitive lookup
    lower_headers = {k.lower(): v for k, v in headers.items()}

    # Accept common JSON content‑type variants
    ct = lower_headers.get("content-type", "").lower()
    acceptable_cts = {"application/json", "text/json"}
    if not any(ct.startswith(accept) for accept in acceptable_cts):
        raise ValueError(f"Unsupported Content-Type: {ct!r}. Expected application/json.")

    # Ensure body is a string; if bytes, decode using utf‑8
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError(f"Body must be bytes or str, got {type(body).__name__}.")

    # Parse JSON
    try:
        payload = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decode error: {exc}") from exc

    # Validate payload type
    if not isinstance(payload, dict):
        raise ValueError(f"JSON payload must be an object (dict), got {type(payload).__name__}.")

    return payload