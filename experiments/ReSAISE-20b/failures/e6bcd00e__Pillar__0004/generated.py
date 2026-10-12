import json
from typing import Dict, Any


def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    incoming_request : dict
        A dictionary containing HTTP headers and the request body.
        Expected keys:
            - 'headers': a dict of header names to values
            - 'body': the raw request body (str or bytes)

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not set to a JSON media type.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = incoming_request.get("headers", {})
    body = incoming_request.get("body")

    # Validate Content-Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")
    # Allow common JSON media types
    if "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # Ensure body is a string or bytes
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body contains invalid UTF‑8 encoding.") from exc
    elif not isinstance(body, str):
        raise ValueError(f"Body must be a string or bytes, got {type(body).__name__}.")

    # Parse JSON with strict mode to avoid non‑standard extensions
    try:
        parsed = json.loads(body, strict=True)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed