import json
from typing import Dict, Any

# Maximum allowed size for the JSON body (in bytes) to mitigate DoS attacks
MAX_JSON_SIZE = 10 * 1024 * 1024  # 10 MB


def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse a JSON request body from an incoming HTTP request.

    Parameters
    ----------
    client_request : dict
        A dictionary containing the HTTP request headers and body. Expected keys:
            - "headers": a mapping of header names to values.
            - "body": the raw request body, either as `str` or `bytes`.

    Returns
    -------
    dict
        The parsed JSON body.

    Raises
    ------
    ValueError
        If the Content-Type header does not indicate JSON, or if the body is
        malformed, too large, or cannot be parsed as JSON.
    """
    # --- 1. Retrieve headers and body ---------------------------------------
    headers = client_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    body = client_request.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # --- 2. Validate Content-Type ------------------------------------------
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not isinstance(content_type, str):
        raise ValueError("Content-Type header is missing or invalid")

    # Accept common JSON media types
    if not any(ct in content_type.lower()
               for ct in ("application/json", "text/json", "application/*+json")):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # --- 3. Enforce size limit ---------------------------------------------
    if isinstance(body, bytes):
        body_length = len(body)
    else:
        # Convert to string if not already
        body = str(body)
        body_length = len(body.encode("utf-8"))

    if body_length > MAX_JSON_SIZE:
        raise ValueError(f"JSON payload exceeds maximum allowed size "
                         f"of {MAX_JSON_SIZE} bytes")

    # --- 4. Parse JSON ------------------------------------------------------
    try:
        if isinstance(body, bytes):
            parsed = json.loads(body.decode("utf-8"))
        else:
            parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dictionary)")

    return parsed