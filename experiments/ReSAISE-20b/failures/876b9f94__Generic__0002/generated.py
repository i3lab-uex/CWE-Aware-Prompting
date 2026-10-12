import json
from typing import Dict, Any


def process_json_input(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of a FastAPI request.

    Parameters
    ----------
    req : dict
        Dictionary containing HTTP headers and body. Expected keys:
            - 'headers': a mapping of header names to values
            - 'body': the raw request body as bytes or string

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not application/json.
        If the body cannot be decoded as JSON.
    """
    # Extract headers and body
    headers = req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Normalize header keys to lowercase for case‑insensitive comparison
    headers_lower = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lower.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept only application/json (optionally with charset)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    body = req.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Ensure body is a string
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be bytes or string")

    # Optional: limit body size to prevent DoS (e.g., 10 MB)
    MAX_BODY_SIZE = 10 * 1024 * 1024
    if len(body_str) > MAX_BODY_SIZE:
        raise ValueError("Request body too large")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dictionary)")

    return parsed