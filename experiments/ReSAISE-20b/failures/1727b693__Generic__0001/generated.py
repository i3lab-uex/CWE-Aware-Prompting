import json
from typing import Dict, Any

def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    input_data : dict
        Dictionary containing at least two keys:
            * ``headers``: a mapping of HTTP headers.
            * ``body``   : the raw request body as bytes or string.

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the request Content-Type is not ``application/json`` (or a valid variant)
        or if the body cannot be decoded as JSON.
    """
    # Extract headers and body
    headers = input_data.get("headers", {})
    body = input_data.get("body")

    if body is None:
        raise ValueError("Request body missing.")

    # Normalize header keys to lowercase for case‑insensitive lookup
    headers_lower = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lower.get("content-type", "")
    # Accept standard JSON media type and optional charset
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. "
            "Only 'application/json' is accepted."
        )

    # Ensure body is a string before decoding
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Failed to decode body bytes: {exc}") from exc
    else:
        body_str = str(body)

    # Parse JSON with strict validation
    try:
        data = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(
            f"JSON payload must be an object (dict), got {type(data).__name__}."
        )

    return data