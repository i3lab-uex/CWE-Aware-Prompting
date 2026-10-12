import json
from typing import Dict, Any

def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        Dictionary containing the request headers and body. Expected keys:
            - 'headers': a mapping of header names to values.
            - 'body': the raw request body (bytes or str).

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is not 'application/json'.
        If the body cannot be decoded as valid JSON.
    """
    # 1. Validate Content-Type header
    headers = input_data.get("headers", {})
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    # Accept only application/json (case‑insensitive, allow charset)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type!r}")

    # 2. Retrieve the body
    body = input_data.get("body")
    if body is None:
        raise ValueError("Missing request body.")

    # 3. Decode bytes to string if necessary
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8.") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError(f"Unsupported body type: {type(body).__name__}")

    # 4. Parse JSON safely
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    # 5. Ensure the result is a dictionary (JSON object)
    if not isinstance(parsed, dict):
        raise ValueError("Expected JSON object at top level.")

    return parsed