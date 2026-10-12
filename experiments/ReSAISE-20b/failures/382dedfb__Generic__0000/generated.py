import json
from typing import Any, Dict

def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the incoming HTTP request for JSON content and parse its body.

    Parameters
    ----------
    incoming_req : dict
        Dictionary containing the HTTP request headers and body.
        Expected keys are:
            - "headers": a mapping of header names to values
            - "body": the raw request body (bytes or str)

    Returns
    -------
    dict
        The parsed JSON body.

    Raises
    ------
    ValueError
        If the `Content-Type` header is missing or not a JSON-compatible type.
        If the body cannot be decoded as valid JSON.
    """
    # Ensure required keys are present
    if not isinstance(incoming_req, dict):
        raise ValueError("Request must be a dictionary.")
    if "headers" not in incoming_req or "body" not in incoming_req:
        raise ValueError("Request must contain 'headers' and 'body' keys.")

    headers = incoming_req["headers"]
    body = incoming_req["body"]

    # Normalise header names to lowercase for case-insensitive lookup
    headers_normalised = {k.lower(): v for k, v in headers.items()}

    content_type = headers_normalised.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Content-Type must be application/json")

    # Convert body to string if it is bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF-8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dictionary)")

    return parsed