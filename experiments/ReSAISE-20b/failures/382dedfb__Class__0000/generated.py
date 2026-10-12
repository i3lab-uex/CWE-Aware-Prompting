import json
from typing import Dict, Any

# Maximum allowed body size (in bytes) to guard against DOS attacks
MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that the incoming request contains a JSON body and parse it.

    Parameters
    ----------
    incoming_req : dict
        Dictionary that includes both the headers and body of the HTTP request.
        Expected keys are 'headers' (a dict) and 'body' (bytes or str).

    Returns
    -------
    dict
        The parsed JSON body.

    Raises
    ------
    ValueError
        If the content‑type is not a JSON compatible format,
        if the body exceeds ``MAX_BODY_SIZE``,
        or if the body is not valid JSON.
    """
    # Retrieve headers (case‑insensitive)
    headers = incoming_req.get("headers", {})
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    # Ensure Content‑Type is a JSON type
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Content-Type must be application/json")

    # Get body (bytes or str)
    body = incoming_req.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Guard against excessively large payloads
    if isinstance(body, bytes):
        size = len(body)
    else:
        size = len(body.encode("utf-8"))
    if size > MAX_BODY_SIZE:
        raise ValueError(f"Request body too large (>{MAX_BODY_SIZE} bytes)")

    # Convert to string if necessary
    body_str = body.decode("utf-8") if isinstance(body, bytes) else str(body)

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dictionary)")

    return parsed