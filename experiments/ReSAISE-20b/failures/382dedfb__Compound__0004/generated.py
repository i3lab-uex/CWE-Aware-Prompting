import json
from typing import Dict, Any

# Maximum allowed request body size (1 MB)
MAX_BODY_SIZE = 1 * 1024 * 1024


def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the Content-Type header and parse a JSON request body.

    Parameters
    ----------
    incoming_req : dict
        A dictionary containing the keys 'headers' (mapping of header names to values)
        and 'body' (the raw request body as a string or bytes).

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type is not a JSON-compatible value.
        If the body is larger than ``MAX_BODY_SIZE``.
        If the body cannot be parsed as JSON.
    """
    # Grab headers and body
    headers = incoming_req.get("headers", {})
    raw_body = incoming_req.get("body")

    # 1. Validate Content-Type
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept only application/json or variants with charset
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type}. Expected application/json"
        )

    # 2. Ensure body size is reasonable
    if isinstance(raw_body, (bytes, bytearray)):
        body_bytes = raw_body
    elif isinstance(raw_body, str):
        body_bytes = raw_body.encode("utf-8")
    else:
        raise ValueError("Request body must be a string or bytes")

    if len(body_bytes) > MAX_BODY_SIZE:
        raise ValueError("Request body exceeds maximum allowed size")

    # 3. Parse JSON safely
    try:
        parsed = json.loads(body_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    # 4. Ensure the result is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dictionary)")

    return parsed