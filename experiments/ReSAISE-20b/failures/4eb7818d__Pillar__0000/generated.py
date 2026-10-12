import json
from typing import Dict, Any


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        The incoming request object. Expected to contain a 'body' key with either
        a JSON string or bytes, and optionally a 'headers' dict.

    Returns
    -------
    dict
        The decoded JSON payload as a dictionary.

    Raises
    ------
    ValueError
        If the request body is missing, not a string/bytes, or fails JSON decoding.
    """
    # Ensure the request has a body
    if "body" not in request:
        raise ValueError("Request missing 'body' key")

    body = request["body"]

    # Body must be bytes or str
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to decode body bytes") from exc

    if not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes")

    # Optionally, enforce a reasonable size limit (e.g., 1 MB)
    if len(body) > 1024 * 1024:
        raise ValueError("Request body too large")

    # Validate Content-Type header if present
    headers = request.get("headers", {})
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if content_type and "application/json" not in content_type.lower():
        raise ValueError("Content-Type must be application/json")

    # Parse JSON
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return payload