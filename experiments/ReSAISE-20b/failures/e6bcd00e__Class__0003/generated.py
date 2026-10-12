import json
from typing import Dict, Any


def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing the HTTP headers and body of an incoming request.
        Expected keys are:
            - "headers": dict of header names to values
            - "body": raw request body (bytes or str)

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not application/json.
        If JSON decoding fails due to malformed data.

    Notes
    -----
    - The function does **not** perform any authentication or integrity checks.
      It only verifies that the payload is syntactically valid JSON and
      that the request declares the correct MIME type.
    - In a real-world application you would also want to enforce size limits,
      validate against a schema, and possibly verify digital signatures
      or authentication tokens to protect against CWE-345.
    """
    # Extract headers and body, normalizing header names to lowercase
    raw_headers = incoming_request.get("headers", {})
    headers = {k.lower(): v for k, v in raw_headers.items()}

    content_type = headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Only accept strict application/json; ignore charset parameters
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Retrieve body; it may be bytes or str
    raw_body = incoming_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Ensure the body is a string for json.loads
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes")

    # Attempt to parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    # Ensure the top-level object is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed