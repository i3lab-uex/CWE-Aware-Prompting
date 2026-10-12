import json
from typing import Dict, Any

def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req : dict
        A dictionary representing the HTTP request. It must contain at least
        a ``headers`` mapping and a ``body`` value (bytes or str).

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not application/json,
        or if the body cannot be decoded as valid JSON.
    """
    # Retrieve headers and body
    headers = req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")

    # Normalise header names to lowercase for case-insensitive lookup
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = str(value).lower()
            break

    if not content_type or "application/json" not in content_type:
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. Expected application/json."
        )

    body = req.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Ensure body is a string before decoding
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to decode body bytes as UTF-8: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError(f"Body must be bytes or str, got {type(body).__name__}")

    try:
        payload = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return payload