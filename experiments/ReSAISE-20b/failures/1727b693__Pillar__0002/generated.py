import json
from typing import Any, Dict


def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        A dictionary containing at least two keys:
            - 'headers': a mapping of request headers (case‑insensitive)
            - 'body'   : the raw request body as a string or bytes

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the content type is not 'application/json' (or a variant with charset),
        or if the body cannot be decoded as JSON.
    """
    # Ensure headers exist
    headers = input_data.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Missing or invalid headers in request data")

    # Retrieve content type header (case‑insensitive)
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = str(value).lower()
            break

    if not content_type or not content_type.startswith("application/json"):
        raise ValueError(
            "Unsupported Content-Type. Expected 'application/json'. "
            f"Received: {content_type!r}"
        )

    # Retrieve body
    raw_body = input_data.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Decode bytes to str if necessary
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes")

    # Parse JSON safely
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return parsed