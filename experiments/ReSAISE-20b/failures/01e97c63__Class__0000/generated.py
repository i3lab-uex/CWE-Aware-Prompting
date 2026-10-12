import json
from typing import Dict, Any

def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse the JSON body of an HTTP request.

    Parameters
    ----------
    client_request : dict
        Dictionary containing the request headers and body. Expected keys:
            - 'headers': a mapping of header names to values.
            - 'body'   : the raw request body (bytes or str).

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the 'Content-Type' header is missing or not JSON-compatible.
        If the request body cannot be decoded as valid JSON.
    """
    # Retrieve headers and body
    headers = client_request.get("headers", {})
    body = client_request.get("body")

    if body is None:
        raise ValueError("Request body is missing.")

    # Normalize header names to lowercase for case‑insensitive lookup
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")

    # Accept common JSON MIME types
    json_types = {
        "application/json",
        "application/json; charset=utf-8",
        "application/ld+json",
        "application/vnd.api+json",
    }
    if not any(ct.lower().startswith(jt) for jt in json_types for ct in [content_type]):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Decode body to string if it's bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8 encoded text.") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a bytes or str instance.")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body.") from exc

    # Ensure the parsed value is a dictionary (object)
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dict).")

    return parsed