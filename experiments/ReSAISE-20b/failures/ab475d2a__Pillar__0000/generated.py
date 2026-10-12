import json
from typing import Dict, Any


def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req : dict
        A dictionary representing the request. Expected keys:
            - "headers": a mapping of header names to values.
            - "body": the raw request body (bytes or str).

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not 'application/json'.
        If JSON decoding fails.
    """
    # Ensure headers are present and case‑insensitive
    headers = req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    # Retrieve the Content-Type header (case‑insensitive)
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type; only 'application/json' is accepted.")

    # Get the body payload
    body = req.get("body")
    if body is None:
        raise ValueError("Request body is missing.")

    # Convert bytes to string if necessary
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF‑8: {exc}") from exc

    if not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes.")

    # Parse JSON
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return payload