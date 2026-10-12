import json
from typing import Dict, Any

def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict:
    """
    Validate that the incoming request contains a JSON body and parse it.

    Parameters
    ----------
    incoming_req : dict
        Dictionary that includes both the headers and body of the HTTP request.
        Expected keys:
            - "headers": a mapping of header names to values (case-insensitive)
            - "body"   : the raw request body as a string or bytes

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not a JSON-compatible type.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = incoming_req.get("headers", {})
    body = incoming_req.get("body")

    if body is None:
        raise ValueError("Request body is missing.")

    # Normalize header keys to lower-case for case-insensitive lookup
    headers_lower = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lower.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")

    # Accept common JSON media types
    json_media_types = {"application/json", "application/ld+json", "application/vnd.api+json"}
    # Strip parameters (e.g., charset) and compare
    media_type = content_type.split(";")[0].strip().lower()
    if media_type not in json_media_types:
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Decode body if bytes
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Failed to decode request body: {exc}") from exc

    if not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes.")

    # Parse JSON safely
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return parsed