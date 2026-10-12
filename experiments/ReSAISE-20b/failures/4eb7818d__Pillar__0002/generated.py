import json
from typing import Dict, Any

MAX_BODY_SIZE = 1_048_576  # 1 MiB


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        The request object containing headers and body. Expected keys:
            - "headers": mapping of header names to values
            - "body": raw request body as bytes or str

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not application/json,
        if the body exceeds MAX_BODY_SIZE, or if JSON decoding fails.
    """
    # Validate headers
    headers = request.get("headers", {})
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    # Allow for charset or other parameters
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type}. Expected application/json."
        )

    # Get body
    raw_body = request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body.")

    # Ensure body is bytes or str
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8 encoded.") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes.")

    # Protect against oversized payloads
    if len(raw_body.encode("utf-8")) > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds maximum allowed size of {MAX_BODY_SIZE} bytes.")

    # Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return parsed