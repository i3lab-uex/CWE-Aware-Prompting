import json
from typing import Dict, Any

# List of acceptable JSON content types
ACCEPTABLE_CONTENT_TYPES = {
    "application/json",
    "application/ld+json",
    "application/vnd.api+json",
}

def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and parse the JSON body of an incoming request.

    Parameters
    ----------
    client_request : dict
        Dictionary containing the HTTP headers and body of a request.
        Expected keys are:
            - "headers": dict[str, str]   (header names case‑insensitive)
            - "body"  : bytes or str      (raw request payload)

    Returns
    -------
    dict
        Parsed JSON content.

    Raises
    ------
    ValueError
        If the request does not contain a valid JSON content type or if the body
        cannot be parsed as JSON.
    """
    # Retrieve headers and body from the request dictionary
    try:
        raw_headers = client_request["headers"]
        raw_body = client_request["body"]
    except KeyError as exc:
        raise ValueError("Request must contain 'headers' and 'body' keys.") from exc

    # Normalize header names to lowercase for case‑insensitive lookup
    headers = {k.lower(): v for k, v in raw_headers.items()}

    # Check Content-Type header
    content_type = headers.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")

    # Allow only known JSON content types
    if not any(content_type.lower().startswith(ct) for ct in ACCEPTABLE_CONTENT_TYPES):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Ensure body is a string (FastAPI typically provides str, but bytes may also occur)
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF‑8.") from exc

    # Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body.") from exc

    # Ensure the parsed content is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must represent an object (dictionary).")

    return parsed