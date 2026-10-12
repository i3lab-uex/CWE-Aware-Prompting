import json
from typing import Any, Dict

def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        A dictionary containing the keys ``headers`` and ``body``.  The
        ``headers`` value should be a mapping of header names to values,
        and ``body`` should be the raw request body as bytes or a string.

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the request Content-Type is not ``application/json`` or if the body
        cannot be decoded as JSON.
    """
    # Ensure we have headers and body keys
    if not isinstance(input_data, dict):
        raise ValueError("input_data must be a dictionary with 'headers' and 'body' keys")

    headers = input_data.get("headers", {})
    body   = input_data.get("body")

    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary")
    if body is None:
        raise ValueError("Missing request body")

    # Normalise header names to lower case for case‑insensitive lookup
    content_type = None
    for name, value in headers.items():
        if name.lower() == "content-type":
            content_type = str(value).lower()
            break

    if content_type is None or not content_type.startswith("application/json"):
        raise ValueError(
            "Unsupported Content-Type. Expected 'application/json', got "
            f"'{content_type or 'None'}'"
        )

    # Convert body to string if it's bytes
    if isinstance(body, (bytes, bytearray)):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Request body is not valid UTF‑8: {exc}") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Request body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed