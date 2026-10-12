import json
from typing import Any, Dict

MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB limit to mitigate DoS attacks


def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a FastAPI request body that is expected to be JSON.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing the HTTP headers under 'headers' and the raw body
        string under 'body'.

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not application/json,
        if the body exceeds ``MAX_BODY_SIZE``,
        or if JSON decoding fails.
    """
    # Validate headers
    headers = incoming_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Invalid request: headers must be a dictionary")

    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Only allow application/json
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'"
        )

    # Validate body
    raw_body = incoming_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Ensure the body is a string (FastAPI returns str for body)
    if not isinstance(raw_body, str):
        raise ValueError("Request body must be a string")

    # Protect against large payloads (CWE-693: improper validation of input)
    if len(raw_body.encode("utf-8")) > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds maximum allowed size of {MAX_BODY_SIZE} bytes")

    # Parse JSON safely
    try:
        parsed = json.loads(raw_body, strict=True)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from None

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed