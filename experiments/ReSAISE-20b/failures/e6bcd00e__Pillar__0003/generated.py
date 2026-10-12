import json
from typing import Dict, Any

# Maximum allowed size for JSON payload (1 MB)
MAX_JSON_PAYLOAD_SIZE = 1 * 1024 * 1024


def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-style incoming request.

    Parameters
    ----------
    incoming_request : dict
        A dictionary containing the HTTP headers and body of the incoming request.
        Expected keys are ``headers`` (a dict of header names to values) and
        ``body`` (the raw request payload, as a str or bytes).

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the ``Content-Type`` header is missing or not set to ``application/json``
        (case-insensitive, may include charset parameters).
        If the body is not a valid JSON string.
        If the payload exceeds :data:`MAX_JSON_PAYLOAD_SIZE`.
    """
    # Validate headers
    headers = incoming_request.get("headers", {})
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Ensure the MIME type is application/json
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'"
        )

    # Retrieve body
    body = incoming_request.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Convert bytes to str if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be a str or bytes object")

    # Enforce payload size limit to mitigate DoS attacks
    if len(body_str.encode("utf-8")) > MAX_JSON_PAYLOAD_SIZE:
        raise ValueError(f"JSON payload exceeds maximum allowed size of {MAX_JSON_PAYLOAD_SIZE} bytes")

    # Parse JSON safely
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    # Ensure the result is a dictionary (as expected by FastAPI models)
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed